# DPIA Screening Assessment — StudyVault Free Tier

**Date:** 15 April 2026
**Assessed by:** Tom Shaun
**Service:** StudyVault (studyvault.co.uk) — free tier

## Is a full DPIA required?

**No.** The free tier of StudyVault does not process personal data. A full DPIA is not required under UK GDPR Article 35.

## Reasoning

StudyVault is a GCSE revision website designed for students aged 14-16. The free tier has been deliberately designed to minimise data collection:

- **No accounts or registration.** Students use the site without signing up, providing an email address, or creating any form of identity.
- **No personal data collected.** We do not collect names, email addresses, phone numbers, IP addresses (beyond transient server logs), device identifiers, or any other personal information.
- **No cookies.** The site sets no cookies of any kind.
- **No advertising or third-party tracking.** No ad networks, no tracking pixels, no social media integrations.
- **All user data stored locally.** Subject preferences, lesson progress, quiz scores, and accessibility settings are stored in the browser's localStorage on the student's own device. This data never leaves the device and is not transmitted to our servers.
- **Anonymous analytics only.** Vercel Web Analytics collects aggregated, anonymous page view data with no personal identifiers and no cookies.

Because no personal data is processed, the conditions for a mandatory DPIA under Article 35(1) are not met. The ICO's screening checklist confirms that a DPIA is required when processing is "likely to result in a high risk to the rights and freedoms of natural persons" — this threshold is not reached when no personal data is processed.

## Children's Code consideration

Although StudyVault is likely to be accessed by children (GCSE students aged 14-16), the ICO's Age Appropriate Design Code (Children's Code) applies to services that process children's personal data. Since the free tier does not process personal data, the Code's 15 standards are met by design:

- **Data minimisation (Standard 8):** No personal data is collected.
- **Default settings (Standard 7):** The default is fully anonymous, local-only storage.
- **Profiling (Standard 12):** No user profiles are created.
- **Transparency (Standard 4):** The privacy policy clearly explains what is and is not collected, in plain language.

## When this assessment should be revisited

A full DPIA should be completed if any of the following change:

- Advertising is introduced (ad networks typically set identifiers)
- User accounts or cloud-based progress sync are added
- The school tier is expanded (teacher/student accounts involve personal data processing)
- Any form of personal data collection is introduced

## School tier note

The school tier involves teacher accounts (email + password via Supabase Auth) and may involve student progress tracking in future. A separate DPIA should be completed for the school tier before it processes student personal data at scale. This screening assessment covers the free tier only.
