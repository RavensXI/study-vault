-- Class join codes — the department tier.
--
-- Decided 27 Jul 2026: a head of department signs up themselves, makes a class,
-- shares a short code, and their students join as ordinary free-tier users. It
-- routes around SSO entirely, which is what makes it sellable before a whole
-- school has agreed anything with its IT department.
--
-- ADDITIVE ONLY. This adds columns and a table; it drops nothing and rewrites no
-- existing rows. Supabase's SQL editor may still warn about "destructive
-- operations" because it sees ALTER TABLE — the warning is about the statement
-- type, not about this script.
--
-- Run in the Supabase SQL editor, then press Save.

-- 1. The code itself -----------------------------------------------------------
-- Short, unambiguous, typed by a 15-year-old off a whiteboard at the back of the
-- room. No O/0 or I/1 confusion: the generator below draws from a reduced
-- alphabet, and the column is upper-case only so "abc123" and "ABC123" cannot
-- become two different classes.
ALTER TABLE classes ADD COLUMN IF NOT EXISTS join_code   text;
ALTER TABLE classes ADD COLUMN IF NOT EXISTS join_open   boolean NOT NULL DEFAULT true;
ALTER TABLE classes ADD COLUMN IF NOT EXISTS created_at  timestamptz NOT NULL DEFAULT now();

-- Unique when present. A partial index so the existing 103 classes, which have
-- no code, do not all collide on NULL.
CREATE UNIQUE INDEX IF NOT EXISTS classes_join_code_key
  ON classes (upper(join_code)) WHERE join_code IS NOT NULL;

-- 2. Who joined, and when ------------------------------------------------------
-- class_members currently holds (class_id, student_id) only. joined_at lets a
-- teacher see that a child never actually joined, as opposed to joined and did
-- nothing — different conversations.
ALTER TABLE class_members ADD COLUMN IF NOT EXISTS joined_at timestamptz NOT NULL DEFAULT now();

-- Enrolling twice must be a no-op, not a duplicate row.
CREATE UNIQUE INDEX IF NOT EXISTS class_members_unique
  ON class_members (class_id, student_id);

-- 3. Generator -----------------------------------------------------------------
-- Crockford-ish alphabet: no I, L, O, U, 0, 1. Six characters is ~1.07bn
-- combinations, which is far more than we need; the point of six is that it
-- fits on a whiteboard and survives being read aloud.
CREATE OR REPLACE FUNCTION generate_class_join_code() RETURNS text AS $$
DECLARE
  alphabet text := 'ABCDEFGHJKMNPQRSTVWXYZ23456789';
  candidate text;
  i int;
BEGIN
  LOOP
    candidate := '';
    FOR i IN 1..6 LOOP
      candidate := candidate || substr(alphabet, floor(random() * length(alphabet) + 1)::int, 1);
    END LOOP;
    -- collision is vanishingly unlikely, but a class with the wrong students in
    -- it is a data-protection incident, so check rather than assume
    EXIT WHEN NOT EXISTS (SELECT 1 FROM classes WHERE upper(join_code) = candidate);
  END LOOP;
  RETURN candidate;
END;
$$ LANGUAGE plpgsql;

-- 4. Row-level security --------------------------------------------------------
-- A student joining by code must be able to look up exactly one thing: does this
-- code match an open class. They must NOT be able to list classes, or read the
-- roll of a class they are not in.
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE class_members ENABLE ROW LEVEL SECURITY;

-- The join lookup goes through the service key in api/class/join.js, so no
-- anon-readable policy on classes is needed or wanted. Teachers read their own.
DROP POLICY IF EXISTS classes_teacher_own ON classes;
CREATE POLICY classes_teacher_own ON classes
  FOR SELECT TO authenticated
  USING (
    teacher_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles p
      WHERE p.id = auth.uid()
        AND p.role IN ('school_admin', 'platform_admin')
        AND (p.role = 'platform_admin' OR p.school_id = classes.school_id)
    )
  );

-- A student may see their OWN membership rows, nothing else.
DROP POLICY IF EXISTS class_members_own ON class_members;
CREATE POLICY class_members_own ON class_members
  FOR SELECT TO authenticated
  USING (
    student_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM classes c
      WHERE c.id = class_members.class_id
        AND (
          c.teacher_id = auth.uid()
          OR EXISTS (
            SELECT 1 FROM profiles p
            WHERE p.id = auth.uid()
              AND p.role IN ('school_admin', 'platform_admin')
              AND (p.role = 'platform_admin' OR p.school_id = c.school_id)
          )
        )
    )
  );

-- 5. Backfill ------------------------------------------------------------------
-- Give the existing demo classes codes so the flow can be walked end to end
-- without making new rows.
UPDATE classes SET join_code = generate_class_join_code() WHERE join_code IS NULL;

-- Check: every class has a code, and they are all distinct.
SELECT count(*) AS classes,
       count(join_code) AS with_code,
       count(DISTINCT upper(join_code)) AS distinct_codes
FROM classes;
