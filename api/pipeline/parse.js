const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');
const JSZip = require('jszip');
const { parseStringPromise } = require('xml2js');

/**
 * Extract all text content from a PPTX slide XML.
 * Walks the XML tree looking for <a:t> elements (text runs).
 */
function extractTextFromXml(obj) {
  const texts = [];

  function walk(node) {
    if (!node || typeof node !== 'object') return;

    // <a:t> elements contain the actual text
    if (node['a:t']) {
      const items = Array.isArray(node['a:t']) ? node['a:t'] : [node['a:t']];
      for (const item of items) {
        const text = typeof item === 'string' ? item : (item._ || '');
        if (text.trim()) texts.push(text);
      }
    }

    // Recurse into all child elements
    for (const key of Object.keys(node)) {
      const val = node[key];
      if (Array.isArray(val)) {
        for (const child of val) walk(child);
      } else if (typeof val === 'object') {
        walk(val);
      }
    }
  }

  walk(obj);
  return texts.join(' ');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { job_id } = req.body;
  if (!job_id) {
    return res.status(400).json({ error: 'Missing job_id' });
  }

  // Fetch the upload job
  const { data: job, error: jobError } = await supabase
    .from('upload_jobs')
    .select('*')
    .eq('id', job_id)
    .single();

  if (jobError || !job) {
    return res.status(404).json({ error: 'Upload job not found' });
  }

  // Update phase
  await supabase.from('upload_jobs').update({ current_phase: 'parsing' }).eq('id', job_id);

  try {
    // Download PPTX from Supabase Storage
    const { data: fileData, error: fileError } = await supabase.storage
      .from('pipeline-uploads')
      .download(job.ppt_storage_path);

    if (fileError || !fileData) {
      throw new Error(`Failed to download PPT: ${fileError?.message || 'file not found'}`);
    }

    // Convert Blob to Buffer
    const buffer = Buffer.from(await fileData.arrayBuffer());

    // Parse PPTX (it's a ZIP archive)
    const zip = await JSZip.loadAsync(buffer);
    const slides = [];

    // Extract text from each slide
    for (const [name, file] of Object.entries(zip.files)) {
      const slideMatch = name.match(/^ppt\/slides\/slide(\d+)\.xml$/);
      if (!slideMatch) continue;

      const slideNumber = parseInt(slideMatch[1]);
      const xml = await file.async('string');
      const parsed = await parseStringPromise(xml);
      const text = extractTextFromXml(parsed);

      // Also try to get speaker notes
      let notes = '';
      const notesPath = `ppt/notesSlides/notesSlide${slideNumber}.xml`;
      if (zip.files[notesPath]) {
        const notesXml = await zip.files[notesPath].async('string');
        const notesParsed = await parseStringPromise(notesXml);
        notes = extractTextFromXml(notesParsed);
      }

      slides.push({
        slideNumber,
        text: text.trim(),
        notes: notes.trim(),
      });
    }

    // Sort by slide number
    slides.sort((a, b) => a.slideNumber - b.slideNumber);

    // Build structured extracted text
    const extractedText = slides
      .map(s => {
        let content = `--- Slide ${s.slideNumber} ---\n${s.text}`;
        if (s.notes) content += `\n[Speaker Notes: ${s.notes}]`;
        return content;
      })
      .join('\n\n');

    // Update the upload job with extracted text
    await supabase.from('upload_jobs').update({
      extracted_text: extractedText,
      current_phase: 'parsed',
    }).eq('id', job_id);

    return res.status(200).json({
      job_id,
      status: 'parsed',
      slide_count: slides.length,
      char_count: extractedText.length,
      preview: extractedText.substring(0, 500),
    });
  } catch (err) {
    console.error('Parse error:', err);
    await supabase.from('upload_jobs').update({
      current_phase: 'failed',
      error_message: err.message,
    }).eq('id', job_id);
    return res.status(500).json({ error: 'Failed to parse PPTX', detail: err.message });
  }
};
