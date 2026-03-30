const { supabase } = require('../pipeline/_lib/supabase');

module.exports = async (req, res) => {
  const slug = req.query.subject;
  if (!slug) {
    return res.status(400).send('Missing ?subject= parameter');
  }

  // Find the school-specific subject first (bespoke), fall back to generic
  let schoolId = req.query.school || null;
  let subjectQuery = supabase
    .from('subjects')
    .select('id, name, exam_board, slug');

  if (schoolId) {
    subjectQuery = subjectQuery.eq('slug', slug).eq('school_id', schoolId);
  } else {
    subjectQuery = subjectQuery.eq('slug', slug).is('school_id', null);
  }

  let { data: subject } = await subjectQuery.single();

  // Fall back to any subject with this slug
  if (!subject) {
    const fallback = await supabase
      .from('subjects')
      .select('id, name, exam_board, slug')
      .eq('slug', slug)
      .limit(1)
      .single();
    subject = fallback.data;
  }

  if (!subject) {
    return res.status(404).send('Subject not found');
  }

  // Get all units
  const { data: units } = await supabase
    .from('units')
    .select('id, name, slug, sort_order')
    .eq('subject_id', subject.id)
    .order('sort_order');

  if (!units || units.length === 0) {
    return res.status(404).send('No units found');
  }

  const unitIds = units.map(u => u.id);

  // Get all lessons with related_media (podcast URL is inside related_media)
  const { data: lessons } = await supabase
    .from('lessons')
    .select('title, description, lesson_number, unit_id, related_media, created_at')
    .in('unit_id', unitIds)
    .order('lesson_number');

  if (!lessons || lessons.length === 0) {
    return res.status(404).send('No lessons found');
  }

  // Extract podcast URLs from related_media
  function getPodcastUrl(relMedia) {
    if (!Array.isArray(relMedia)) return null;
    for (var i = 0; i < relMedia.length; i++) {
      if ((relMedia[i].category || '').toLowerCase() === 'podcasts') {
        var items = relMedia[i].items || [];
        for (var j = 0; j < items.length; j++) {
          if (items[j].title === 'Lesson Podcast' && items[j].url && items[j].url !== '#') {
            return items[j].url;
          }
        }
      }
    }
    return null;
  }

  const siteUrl = 'https://www.studyvault.co.uk';
  const showTitle = 'StudyVault: ' + subject.name + ' (' + subject.exam_board + ')';
  const showDesc = 'GCSE ' + subject.name + ' revision podcasts from StudyVault. Covering the full ' +
    subject.exam_board + ' specification across ' + units.length + ' units.';
  const imageUrl = siteUrl + '/images/subject-' + slug + '.jpg';
  const feedUrl = siteUrl + '/api/podcast/feed?subject=' + slug;

  // Build RSS XML
  let items = '';
  let episodeNum = 0;
  for (const u of units) {
    const unitLessons = lessons.filter(l => l.unit_id === u.id);
    for (const l of unitLessons) {
      const podcastUrl = getPodcastUrl(l.related_media);
      if (!podcastUrl) continue;

      episodeNum++;
      const pubDate = new Date(l.created_at || '2026-01-01').toUTCString();
      const episodeTitle = u.name + ' \u2014 ' + l.title;
      const desc = l.description || l.title;
      const lessonUrl = siteUrl + '/lesson/' + slug + '/' + u.slug + '/' + l.lesson_number;

      items += `
    <item>
      <title>${escXml(episodeTitle)}</title>
      <description>${escXml(desc)}</description>
      <link>${lessonUrl}</link>
      <guid isPermaLink="false">${slug}-${u.slug}-${l.lesson_number}</guid>
      <pubDate>${pubDate}</pubDate>
      <enclosure url="${escXml(podcastUrl)}" type="audio/mpeg" length="0"/>
      <itunes:episode>${episodeNum}</itunes:episode>
      <itunes:title>${escXml(episodeTitle)}</itunes:title>
      <itunes:summary>${escXml(desc)}</itunes:summary>
    </item>`;
    }
  }

  if (episodeNum === 0) {
    return res.status(404).send('No podcast episodes found for this subject');
  }

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${escXml(showTitle)}</title>
    <link>${siteUrl}/browse/${slug}</link>
    <description>${escXml(showDesc)}</description>
    <language>en-gb</language>
    <itunes:author>StudyVault</itunes:author>
    <itunes:owner>
      <itunes:name>StudyVault</itunes:name>
      <itunes:email>studyvault.info@gmail.com</itunes:email>
    </itunes:owner>
    <itunes:image href="${imageUrl}"/>
    <itunes:category text="Education"/>
    <itunes:explicit>false</itunes:explicit>
    <atom:link href="${escXml(feedUrl)}" rel="self" type="application/rss+xml"/>
    ${items}
  </channel>
</rss>`;

  res.setHeader('Content-Type', 'application/rss+xml; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=3600');
  return res.send(xml);
};

function escXml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
