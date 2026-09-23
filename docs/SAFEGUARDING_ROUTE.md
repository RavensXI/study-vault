# The safeguarding route

Built 23 September 2026. It tells a school's Designated Safeguarding Lead (DSL) when a
pupil may have disclosed something in what they typed on StudyVault.

## What it checks

Everything a pupil writes in their own words:

| Where | How |
|---|---|
| Exam answers (lesson practice questions, AI-marked practice pages) | always checked |
| Messages to the lesson tutor | always checked |
| Typed flashcard answers | checked when a word filter finds a worrying word |
| The dashboard search box | checked when a word filter finds a worrying word |

The check runs beside the marking, on the same London servers (Amazon Bedrock,
eu-west-2), so no pupil's words leave the UK. It uses a small, fast model (Claude Haiku 4.5).
It asks one question: is the writer telling us that they, or another child, may be
at risk of harm? It answers "concern", "unsure" or "no". "Concern" and "unsure" both
act. It is told not to flag academic content (An Inspector Calls, Macbeth, war poetry,
History answers about violence, creative writing) or ordinary exam stress.

Tested on 57 hand-written messages (`scripts/safeguarding/cases.json`): all 14 concerns
caught, none of the 30 academic or ordinary messages flagged, 2 of the 13 borderline ones
flagged "unsure" ("I cried in the toilets today", "my mate got beaten up").

## What happens when it flags

1. **The pupil** sees a support panel: Childline 0800 1111, Shout (text SHOUT to 85258),
   999 if in danger, and "a teacher or another adult you trust can help too". A pupil
   at a school with a lead is also told: "your school's safeguarding lead may be told,
   so that someone can help". Nobody is ever promised confidentiality.
   The marker's or tutor's own reply is replaced by a fixed line that points to the
   panel. In testing, the marker wrote its own crisis advice and gave a wrong Childline
   number, so a model-written helpline number never reaches a pupil.
2. **If the pupil is signed in and in a class at a school with a lead set up**, the
   concern is stored in `safeguarding_alerts`: the pupil, the time, where they wrote it,
   the question, their exact words, and why it was flagged.
3. **The lead and any deputies are emailed**: "A possible safeguarding concern was
   flagged at <school> on <time>. Sign in to review it." The email never contains the
   pupil's name or words. At most one email per school per 15 minutes while concerns
   are unreviewed.
4. **The lead reviews it** at https://www.studyvault.co.uk/teacher/safeguarding, adds a
   note if they want, and marks it reviewed. The page reminds them to record it in the
   school's own system (CPOMS, MyConcern). StudyVault is not the record.

Free-tier pupils, pupils who are not signed in, and staff accounts get the support panel
only. Nothing is stored and nobody is emailed, because there is nobody to send it to.

## Who can see a concern

Only people whose StudyVault account email is the school's `lead_email` or one of its
`deputy_emails`. Not the pupil's teachers, not school admins, not the admin password.
The table has row-level security on with no policies, so only the server can read it.

## What a school must give us

In `schools.settings.safeguarding`:

```json
{ "lead_name": "Bev Worthington", "lead_email": "b.worthington@unity.lancs.sch.uk", "deputy_emails": [] }
```

The lead (and each deputy) needs a StudyVault staff account on that email address to open
the review page. Onboarding must ask for the lead and at least one deputy, and schools
must confirm them once a year (onboarding checklist, to build).

## Retention

A concern is deleted 90 days after it is marked reviewed (the daily cron,
`api/cron/weekly-digest.js`). Unreviewed concerns are never deleted.

## Known limits

- A pupil is only linked to their school if they are signed in and in a class there.
  Until school Microsoft sign-in is approved, that means pupils who joined a class with a
  class code.
- The check reads one piece of text at a time. It does not see a pattern across a
  pupil's week.
- Nothing is checked in bug reports or subject requests (not pupil-to-school text).
- If the email service fails, the concern is still stored and shown on the review page.

## Files

- `api/_lib/safeguard.js`: the check, the word filter, who the pupil is, storing, the email
- `api/ai-mark.js`, `api/tutor.js`, `api/flashcards/judge.js`, `api/finder.js`: call it
- `js/safeguard-support.js`: the sign-in header and the support panel
- `teacher/safeguarding.html`, `api/teacher/safeguarding.js`: the review page
- `supabase/migrations/20260923200000_safeguarding_alerts.sql`: the table
- `scripts/safeguarding/`: `test_check.js` (the 57 messages), `test_route.js` (end to end
  through the real handlers), `browser_check.py` (every page in a browser),
  `setup_fixtures.js` (Unity's contacts, the test school)

## Test school

"Safeguarding Test School" (slug `safeguarding-test`). Lead: Tom
(t.shaun@unity.lancs.sch.uk), so Tom can open the review page with his own login.
Test pupil, test teacher (not a lead) and a test deputy: logins in
`scripts/safeguarding/fixtures.json` (not committed).
