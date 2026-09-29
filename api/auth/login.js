module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { code } = req.body || {};

  // --- Student school codes: RETIRED (1 Sep 2026) ---
  // School sign-in is SSO (Microsoft / Google) with a school-email fallback.
  // The old landing page at /index.html still carried the code form, so a
  // student with last year's code could open a school session and reach
  // bespoke content outside the identity model. Refuse every code here so no
  // client, old or new, can mint a student session from a shared secret.
  if (code) {
    return res.status(410).json({
      error: 'School codes have been retired. Sign in with your school account instead.',
    });
  }

  // --- Admin password login: RETIRED (29 Sep 2026) ---
  // Admin is Tom's own account with a two-factor code (api/_lib/admin-auth.js); sign in at
  // /teacher/login. TEACHER_PASSWORD was retired on 6 Sep 2026.
  return res.status(410).json({
    error: 'The admin password has been retired. Sign in with your account and code at /teacher/login.',
  });
};
