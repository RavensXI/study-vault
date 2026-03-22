const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL || 'https://baipckgywpnwapobwtsy.supabase.co',
  process.env.SUPABASE_SERVICE_KEY
);

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { token, name, password } = req.body || {};

  if (!token || !name || !password) {
    return res.status(400).json({ error: 'Token, name, and password are required' });
  }

  if (password.length < 8) {
    return res.status(400).json({ error: 'Password must be at least 8 characters' });
  }

  // --- Validate the invitation token ---
  const { data: invitation, error: invError } = await supabase
    .from('teacher_invitations')
    .select('*')
    .eq('token', token)
    .single();

  if (invError || !invitation) {
    return res.status(400).json({ error: 'Invalid invitation token' });
  }

  if (invitation.accepted_at) {
    return res.status(400).json({ error: 'This invitation has already been used' });
  }

  if (invitation.expires_at && new Date(invitation.expires_at) < new Date()) {
    return res.status(400).json({ error: 'This invitation has expired' });
  }

  const { email, school_id, subject_ids } = invitation;

  // --- Create the Supabase Auth user ---
  const { data: createData, error: createError } = await supabase.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
  });

  if (createError) {
    // User might already exist (e.g. previously deleted and re-invited)
    if (createError.message && createError.message.includes('already been registered')) {
      return res.status(409).json({ error: 'An account with this email already exists. Try logging in instead.' });
    }
    return res.status(500).json({ error: createError.message || 'Failed to create account' });
  }

  const userId = createData.user.id;

  // --- Update the profile (auth trigger auto-creates the row) ---
  // Small delay to let the trigger fire
  const { error: profileError } = await supabase
    .from('profiles')
    .upsert({
      id: userId,
      full_name: name.trim(),
      role: 'teacher',
      school_id,
    }, { onConflict: 'id' });

  if (profileError) {
    console.error('Profile update error:', profileError);
    // Non-fatal — account is created, profile can be fixed later
  }

  // --- Create teacher_subjects rows ---
  if (subject_ids && subject_ids.length > 0) {
    const subjectRows = subject_ids.map(sid => ({
      teacher_id: userId,
      subject_id: sid,
    }));

    const { error: subjectError } = await supabase
      .from('teacher_subjects')
      .insert(subjectRows);

    if (subjectError) {
      console.error('Teacher subjects insert error:', subjectError);
      // Non-fatal — subjects can be assigned later
    }
  }

  // --- Mark invitation as accepted ---
  await supabase
    .from('teacher_invitations')
    .update({ accepted_at: new Date().toISOString(), accepted_by: userId })
    .eq('id', invitation.id);

  // --- Sign the user in to get a session ---
  const { data: signInData, error: signInError } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (signInError || !signInData.session) {
    // Account was created but auto-login failed — user can log in manually
    return res.status(201).json({
      message: 'Account created successfully. Please log in.',
      profile: { id: userId, name: name.trim(), role: 'teacher', school_id },
    });
  }

  // Fetch subjects for the response
  const { data: teacherSubjects } = await supabase
    .from('teacher_subjects')
    .select('subject_id, subjects(id, name, slug)')
    .eq('teacher_id', userId);

  const subjects = (teacherSubjects || []).map(ts => ts.subjects).filter(Boolean);

  return res.status(201).json({
    session: {
      access_token: signInData.session.access_token,
      refresh_token: signInData.session.refresh_token,
      expires_at: signInData.session.expires_at,
    },
    profile: {
      id: userId,
      name: name.trim(),
      role: 'teacher',
      school_id,
    },
    subjects,
  });
};
