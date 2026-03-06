const { requireTeacher } = require('./_lib/auth');

const UNSPLASH_API = 'https://api.unsplash.com/search/photos';
const UNSPLASH_ACCESS_KEY = process.env.UNSPLASH_ACCESS_KEY;

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const query = req.query.q;
  if (!query) {
    return res.status(400).json({ error: 'Missing query parameter q' });
  }

  if (!UNSPLASH_ACCESS_KEY) {
    return res.status(500).json({ error: 'UNSPLASH_ACCESS_KEY not configured' });
  }

  try {
    const url = `${UNSPLASH_API}?query=${encodeURIComponent(query)}&orientation=landscape&per_page=8`;
    const resp = await fetch(url, {
      headers: { 'Authorization': `Client-ID ${UNSPLASH_ACCESS_KEY}` },
    });

    if (!resp.ok) {
      const text = await resp.text();
      return res.status(resp.status).json({ error: `Unsplash API error: ${text}` });
    }

    const data = await resp.json();
    const results = (data.results || [])
      .filter(p => p.width > 800 && p.height > 400 && p.width > p.height)
      .slice(0, 8)
      .map(p => ({
        thumb: p.urls.small,
        url: p.urls.regular,
        full: p.urls.full,
        title: p.description || p.alt_description || query,
        photographer: (p.user && p.user.name) || 'Unknown',
        download_location: p.links && p.links.download_location,
      }));

    return res.status(200).json({ results });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
};
