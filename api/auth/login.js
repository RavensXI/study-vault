module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { password } = req.body || {};
  if (!password) {
    return res.status(400).json({ error: 'Password required' });
  }

  // Check admin password
  if (process.env.ADMIN_PASSWORD && password === process.env.ADMIN_PASSWORD) {
    return res.json({ role: 'admin' });
  }

  // Check teacher password
  if (process.env.TEACHER_PASSWORD && password === process.env.TEACHER_PASSWORD) {
    return res.json({ role: 'teacher' });
  }

  return res.status(401).json({ error: 'Incorrect password' });
};
