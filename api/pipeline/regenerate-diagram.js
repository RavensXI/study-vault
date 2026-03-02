const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');
const crypto = require('crypto');

// Cloudflare R2 config (S3-compatible)
const R2_ACCOUNT_ID = process.env.R2_ACCOUNT_ID;
const R2_ACCESS_KEY_ID = process.env.R2_ACCESS_KEY_ID;
const R2_SECRET_ACCESS_KEY = process.env.R2_SECRET_ACCESS_KEY;
const R2_BUCKET = 'studyvault-images';
const R2_PUBLIC_URL = 'https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev';

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_MODEL = 'gemini-3.1-flash-image-preview';
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=`;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { lesson_id, prompt } = req.body;

  if (!lesson_id) {
    return res.status(400).json({ error: 'Missing lesson_id' });
  }
  if (!prompt || !prompt.trim()) {
    return res.status(400).json({ error: 'Missing prompt' });
  }

  // Validate env vars
  if (!GEMINI_API_KEY) {
    return res.status(500).json({ error: 'GEMINI_API_KEY not configured' });
  }
  if (!R2_ACCOUNT_ID || !R2_ACCESS_KEY_ID || !R2_SECRET_ACCESS_KEY) {
    return res.status(500).json({ error: 'R2 credentials not configured' });
  }

  // 1. Fetch lesson data
  const { data: lesson, error: lessonError } = await supabase
    .from('lessons')
    .select('id, title, diagrams, content_html, unit_id')
    .eq('id', lesson_id)
    .single();

  if (lessonError || !lesson) {
    return res.status(404).json({ error: 'Lesson not found' });
  }

  // Get unit + subject info for the R2 path
  const { data: unit } = await supabase
    .from('units')
    .select('slug, subject_id, subjects(slug)')
    .eq('id', lesson.unit_id)
    .single();

  const subjectSlug = unit?.subjects?.slug || 'unknown';
  const unitSlug = unit?.slug || 'unknown';

  try {
    // 2. Call Gemini API to generate the diagram
    const geminiPayload = {
      contents: [{
        parts: [{
          text: prompt.trim() + '\n\nGenerate the image only. No text response needed.'
        }]
      }],
      generationConfig: {
        responseModalities: ['IMAGE', 'TEXT'],
        temperature: 1.0,
      }
    };

    const geminiResp = await fetch(GEMINI_URL + GEMINI_API_KEY, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(geminiPayload),
    });

    if (!geminiResp.ok) {
      const errBody = await geminiResp.text();
      console.error('Gemini API error:', geminiResp.status, errBody);
      return res.status(502).json({ error: 'Gemini API error: ' + geminiResp.status });
    }

    const geminiData = await geminiResp.json();

    // Extract the image from the response
    let imageBase64 = null;
    let imageMime = 'image/jpeg';

    const candidates = geminiData.candidates || [];
    for (const candidate of candidates) {
      const parts = (candidate.content && candidate.content.parts) || [];
      for (const part of parts) {
        if (part.inlineData && part.inlineData.data) {
          imageBase64 = part.inlineData.data;
          imageMime = part.inlineData.mimeType || 'image/jpeg';
          break;
        }
      }
      if (imageBase64) break;
    }

    if (!imageBase64) {
      return res.status(502).json({ error: 'Gemini did not return an image. Try rephrasing your prompt.' });
    }

    // 3. Upload to R2
    const imageBuffer = Buffer.from(imageBase64, 'base64');
    const ext = imageMime.includes('png') ? 'png' : 'jpg';
    const hash = crypto.createHash('md5').update(imageBuffer).digest('hex').substring(0, 8);
    const filename = `diagram_generated_${hash}.${ext}`;
    const r2Key = `${subjectSlug}/${unitSlug}/${filename}`;

    // Use S3-compatible API via AWS SDK (available in Vercel Node runtime)
    const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

    const s3 = new S3Client({
      region: 'auto',
      endpoint: `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
      credentials: {
        accessKeyId: R2_ACCESS_KEY_ID,
        secretAccessKey: R2_SECRET_ACCESS_KEY,
      },
    });

    await s3.send(new PutObjectCommand({
      Bucket: R2_BUCKET,
      Key: r2Key,
      Body: imageBuffer,
      ContentType: imageMime,
    }));

    const publicUrl = `${R2_PUBLIC_URL}/${r2Key}`;

    // 4. Update lesson's diagrams array in Supabase
    const existingDiagrams = lesson.diagrams || [];
    const newDiagram = {
      url: publicUrl,
      alt: 'Generated diagram for ' + lesson.title,
    };

    // If there are existing diagrams, replace the first one; otherwise add
    let updatedDiagrams;
    if (existingDiagrams.length > 0) {
      updatedDiagrams = [newDiagram, ...existingDiagrams.slice(1)];
    } else {
      updatedDiagrams = [newDiagram];
    }

    // Also update the content_html to include/replace the diagram figure
    let updatedHtml = lesson.content_html || '';
    const figureHtml = '<figure class="diagram"><img src="' + publicUrl + '" alt="' + newDiagram.alt + '"><figcaption>' + newDiagram.alt + '</figcaption></figure>';

    // Check if there's an existing diagram figure to replace
    const diagramFigureRegex = /<figure class="diagram">[\s\S]*?<\/figure>/;
    if (diagramFigureRegex.test(updatedHtml)) {
      updatedHtml = updatedHtml.replace(diagramFigureRegex, figureHtml);
    }
    // If no existing diagram figure in HTML, don't inject — let it stay in the diagrams array only

    const updates = {
      diagrams: updatedDiagrams,
    };
    // Only update content_html if we actually replaced something
    if (diagramFigureRegex.test(lesson.content_html || '')) {
      updates.content_html = updatedHtml;
    }

    const { error: updateError } = await supabase
      .from('lessons')
      .update(updates)
      .eq('id', lesson_id);

    if (updateError) {
      console.error('Supabase update error:', updateError);
      return res.status(500).json({ error: 'Diagram generated but failed to save: ' + updateError.message });
    }

    return res.status(200).json({
      status: 'ok',
      lesson_id,
      diagram_url: publicUrl,
      diagrams: updatedDiagrams,
    });

  } catch (err) {
    console.error('Diagram regeneration error:', err);
    return res.status(500).json({ error: 'Internal error: ' + err.message });
  }
};
