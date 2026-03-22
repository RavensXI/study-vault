const { createClient } = require('@supabase/supabase-js');
const crypto = require('crypto');

const supabase = createClient(
  process.env.SUPABASE_URL || 'https://baipckgywpnwapobwtsy.supabase.co',
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Check if the request is from an admin.
 * Accepts either ADMIN_PASSWORD header or a Supabase JWT for a platform_admin user.
 */
async function requireAdmin(req) {
  // 1. Check X-Admin-Password header
  const adminPw = req.headers['x-admin-password'];
  if (adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD) {
    return true;
  }

  // 2. Check Supabase JWT for platform_admin role
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error } = await supabase.auth.getUser(token);
    if (!error && user) {
      const { data: profile } = await supabase
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();
      if (profile && profile.role === 'platform_admin') {
        return true;
      }
    }
  }

  return false;
}

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Admin-Password');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Auth check
  const isAdmin = await requireAdmin(req);
  if (!isAdmin) {
    return res.status(401).json({ error: 'Admin authentication required' });
  }

  const { email, school_id, subject_ids } = req.body || {};

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  if (!school_id) {
    return res.status(400).json({ error: 'School ID is required' });
  }

  // Validate the school exists
  const { data: school, error: schoolError } = await supabase
    .from('schools')
    .select('id, name, slug')
    .eq('id', school_id)
    .single();

  if (schoolError || !school) {
    return res.status(400).json({ error: 'Invalid school ID' });
  }

  // Validate subject_ids if provided
  if (subject_ids && subject_ids.length > 0) {
    const { data: validSubjects } = await supabase
      .from('subjects')
      .select('id')
      .in('id', subject_ids);

    const validIds = (validSubjects || []).map(s => s.id);
    const invalid = subject_ids.filter(id => !validIds.includes(id));
    if (invalid.length > 0) {
      return res.status(400).json({ error: `Invalid subject IDs: ${invalid.join(', ')}` });
    }
  }

  // Check for existing pending invitation for this email + school
  const { data: existing } = await supabase
    .from('teacher_invitations')
    .select('id, token')
    .eq('email', email.trim().toLowerCase())
    .eq('school_id', school_id)
    .is('accepted_at', null)
    .gt('expires_at', new Date().toISOString())
    .limit(1);

  if (existing && existing.length > 0) {
    // Return the existing invitation rather than creating a duplicate
    const signupUrl = `${getBaseUrl(req)}/teacher/signup?token=${existing[0].token}`;
    return res.json({
      invitation_id: existing[0].id,
      signup_url: signupUrl,
      note: 'An active invitation already exists for this email and school',
    });
  }

  // Generate a secure token
  const token = crypto.randomBytes(32).toString('hex');

  // Invitation expires in 7 days
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + 7);

  // Create the invitation
  const { data: invitation, error: insertError } = await supabase
    .from('teacher_invitations')
    .insert({
      email: email.trim().toLowerCase(),
      school_id,
      subject_ids: subject_ids || [],
      token,
      expires_at: expiresAt.toISOString(),
    })
    .select('id')
    .single();

  if (insertError) {
    console.error('Invitation insert error:', insertError);
    return res.status(500).json({ error: 'Failed to create invitation' });
  }

  const signupUrl = `${getBaseUrl(req)}/teacher/signup?token=${token}`;

  return res.status(201).json({
    invitation_id: invitation.id,
    signup_url: signupUrl,
    email: email.trim().toLowerCase(),
    school: school.name,
    expires_at: expiresAt.toISOString(),
  });
};

/**
 * Derive the base URL from the request (works on both localhost and Vercel).
 */
function getBaseUrl(req) {
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  return `${proto}://${host}`;
}
