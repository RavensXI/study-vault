const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');
const JSZip = require('jszip');
const { parseStringPromise } = require('xml2js');

/**
 * Extract text from XML nodes by walking the tree for text elements.
 * Works for both PPTX (<a:t>) and DOCX (<w:t>) formats.
 */
function extractTextFromXml(obj, tagNames) {
  const texts = [];

  function walk(node) {
    if (!node || typeof node !== 'object') return;

    for (const tag of tagNames) {
      if (node[tag]) {
        const items = Array.isArray(node[tag]) ? node[tag] : [node[tag]];
        for (const item of items) {
          const text = typeof item === 'string' ? item : (item._ || '');
          if (text.trim()) texts.push(text);
        }
      }
    }

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

/**
 * Parse a single PPTX file buffer into structured text.
 */
async function parsePptx(buffer, filename) {
  const zip = await JSZip.loadAsync(buffer);
  const slides = [];

  for (const [name, file] of Object.entries(zip.files)) {
    const slideMatch = name.match(/^ppt\/slides\/slide(\d+)\.xml$/);
    if (!slideMatch) continue;

    const slideNumber = parseInt(slideMatch[1]);
    const xml = await file.async('string');
    const parsed = await parseStringPromise(xml);
    const text = extractTextFromXml(parsed, ['a:t']);

    let notes = '';
    const notesPath = `ppt/notesSlides/notesSlide${slideNumber}.xml`;
    if (zip.files[notesPath]) {
      const notesXml = await zip.files[notesPath].async('string');
      const notesParsed = await parseStringPromise(notesXml);
      notes = extractTextFromXml(notesParsed, ['a:t']);
    }

    slides.push({ slideNumber, text: text.trim(), notes: notes.trim() });
  }

  slides.sort((a, b) => a.slideNumber - b.slideNumber);

  const lines = slides.map(s => {
    let content = `--- Slide ${s.slideNumber} ---\n${s.text}`;
    if (s.notes) content += `\n[Speaker Notes: ${s.notes}]`;
    return content;
  });

  return `=== FILE: ${filename} (${slides.length} slides) ===\n\n` + lines.join('\n\n');
}

/**
 * Parse a single DOCX file buffer into text.
 */
async function parseDocx(buffer, filename) {
  const zip = await JSZip.loadAsync(buffer);
  const docFile = zip.files['word/document.xml'];
  if (!docFile) return `=== FILE: ${filename} ===\n\n(No document.xml found)`;

  const xml = await docFile.async('string');
  const parsed = await parseStringPromise(xml);
  const text = extractTextFromXml(parsed, ['w:t']);

  return `=== FILE: ${filename} ===\n\n${text}`;
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

  const { data: job, error: jobError } = await supabase
    .from('upload_jobs')
    .select('*')
    .eq('id', job_id)
    .single();

  if (jobError || !job) {
    return res.status(404).json({ error: 'Upload job not found' });
  }

  await supabase.from('upload_jobs').update({ current_phase: 'parsing' }).eq('id', job_id);

  try {
    const folderPrefix = job.ppt_storage_path;

    // List all files in the upload folder
    const { data: fileList, error: listError } = await supabase.storage
      .from('pipeline-uploads')
      .list(folderPrefix);

    if (listError || !fileList || fileList.length === 0) {
      throw new Error('No files found in upload folder');
    }

    const allText = [];
    let totalSlides = 0;
    let filesParsed = 0;

    for (const fileEntry of fileList) {
      const fileName = fileEntry.name;
      const ext = fileName.split('.').pop().toLowerCase();

      // Only parse supported formats
      if (!['pptx', 'docx'].includes(ext)) continue;

      const filePath = folderPrefix + '/' + fileName;
      const { data: fileData, error: fileError } = await supabase.storage
        .from('pipeline-uploads')
        .download(filePath);

      if (fileError || !fileData) {
        allText.push(`=== FILE: ${fileName} ===\n\n(Download failed: ${fileError?.message || 'unknown error'})`);
        continue;
      }

      const buffer = Buffer.from(await fileData.arrayBuffer());

      if (ext === 'pptx') {
        const text = await parsePptx(buffer, fileName);
        allText.push(text);
        // Count slides from the output
        const slideCount = (text.match(/--- Slide \d+ ---/g) || []).length;
        totalSlides += slideCount;
      } else if (ext === 'docx') {
        const text = await parseDocx(buffer, fileName);
        allText.push(text);
      }

      filesParsed++;
    }

    if (filesParsed === 0) {
      throw new Error('No .pptx or .docx files found to parse. Upload PowerPoint or Word files.');
    }

    const extractedText = allText.join('\n\n\n');

    await supabase.from('upload_jobs').update({
      extracted_text: extractedText,
      current_phase: 'parsed',
    }).eq('id', job_id);

    return res.status(200).json({
      job_id,
      status: 'parsed',
      files_parsed: filesParsed,
      slide_count: totalSlides,
      char_count: extractedText.length,
      preview: extractedText.substring(0, 500),
    });
  } catch (err) {
    console.error('Parse error:', err);
    await supabase.from('upload_jobs').update({
      current_phase: 'failed',
      error_message: err.message,
    }).eq('id', job_id);
    return res.status(500).json({ error: 'Failed to parse files', detail: err.message });
  }
};
