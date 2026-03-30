const { supabase } = require('../pipeline/_lib/supabase');

module.exports = async (req, res) => {
  const slug = req.query.subject;
  if (!slug) {
    return res.status(400).send('Missing ?subject= parameter');
  }

  // Resolve school — accept UUID or school code
  let schoolId = req.query.school || null;
  if (schoolId && !/^[0-9a-f-]{36}$/.test(schoolId)) {
    // Treat as school code — look up the school
    const { data: schools } = await supabase
      .from('schools')
      .select('id, settings')
      .limit(100);
    const match = (schools || []).find(s =>
      s.settings && s.settings.student_code === schoolId.toLowerCase().trim()
    );
    schoolId = match ? match.id : null;
  }

  // Find subject — school-specific first, then generic
  let subject = null;
  if (schoolId) {
    const { data } = await supabase
      .from('subjects')
      .select('id, name, exam_board, slug')
      .eq('slug', slug)
      .eq('school_id', schoolId)
      .single();
    subject = data;
  }
  if (!subject) {
    const { data } = await supabase
      .from('subjects')
      .select('id, name, exam_board, slug')
      .eq('slug', slug)
      .is('school_id', null)
      .single();
    subject = data;
  }
  if (!subject) {
    const { data } = await supabase
      .from('subjects')
      .select('id, name, exam_board, slug')
      .eq('slug', slug)
      .limit(1)
      .single();
    subject = data;
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

  // Build RSS XML — assign sequential pubDates so podcast apps order correctly
  // Episode 1 = oldest date, last episode = newest. Apps show newest first by default.
  let allEpisodes = [];
  for (const u of units) {
    const unitLessons = lessons.filter(l => l.unit_id === u.id);
    for (const l of unitLessons) {
      const podcastUrl = getPodcastUrl(l.related_media);
      if (!podcastUrl) continue;
      allEpisodes.push({ unit: u, lesson: l, podcastUrl });
    }
  }

  let items = '';
  let episodeNum = 0;
  for (const ep of allEpisodes) {
    const u = ep.unit;
    const l = ep.lesson;

      episodeNum++;
      // Sequential dates: episode 1 = base date, each subsequent +1 day
      const baseDate = new Date('2026-01-01T12:00:00Z');
      baseDate.setDate(baseDate.getDate() + (episodeNum - 1));
      const pubDate = baseDate.toUTCString();
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
      <enclosure url="${escXml(ep.podcastUrl)}" type="audio/mpeg" length="0"/>
      <itunes:episode>${episodeNum}</itunes:episode>
      <itunes:title>${escXml(episodeTitle)}</itunes:title>
      <itunes:summary>${escXml(desc)}</itunes:summary>
    </item>`;
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
