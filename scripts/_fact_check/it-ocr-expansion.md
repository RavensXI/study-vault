# Fact-Check Report — it-ocr Expansion (L9–L12)

**Checked:** 2026-05-09  
**Expansion scope:** L9–L12 only — L1–L8 covered in prior pass (see `it-ocr.json`)  
**Lessons checked:** 4  
**Findings:** HIGH 0 · MEDIUM 2 · LOW 1  
**Ship status:** CLEAR — no HIGH findings. Two MEDIUM findings require editorial fixes before the lessons are promoted from `pending_review`.

---

## Summary

All four expansion lessons (L9–L12) were checked against authoritative sources. Claim categories verified:

- **Display technology** (capacitive touchscreen, LCD, OLED, e-ink): one MEDIUM finding on capacitive definition (see MEDIUM-1)
- **Operating system history** (Linux, macOS, Unix, Chrome OS, Windows, iOS, Android): one MEDIUM and one LOW finding (see MEDIUM-2, LOW-1)
- **Internet of Everything (IoE) definition and pillars**: PASS — device-to-device / M2M and human-to-device definitions correct; IoE four-pillar framing (People, Process, Data, Things) consistent with Cisco's canonical definition
- **Interaction methods** (gesture, keyboard, mouse, touch, voice): PASS — all five methods correctly defined with accurate advantages/disadvantages; voice assistant examples not date-cited so no date-accuracy risk
- **Audience demographics and accessibility**: PASS — motor/visual/hearing/cognitive accessibility framing correct; age-device associations (tablets for children, smartphones for teens/young adults) consistent with ONS/Ofcom data; no specific statistics cited so no stat-fabrication risk
- **UK Equality Act 2010 accessibility**: Not explicitly cited in these four lessons — no finding raised
- **Hardware (RAM vs storage, processing power)**: PASS — RAM correctly defined as temporary/volatile; storage correctly defined as persistent; the RAM vs storage distinction is accurate
- **Digital platforms (database, mobile app, spreadsheet, website)**: PASS — all four platform types correctly characterised

---

## Findings

### MEDIUM-1 — L9 (Hardware Considerations for Designing Interfaces)

**Lesson ID:** `babbf45b-3d9e-4318-a943-685285fb1f0c`

**Claim (dfn tooltip):** "A touch-sensitive LCD or OLED screen that detects **finger pressure** or electrical charge, enabling direct interaction without a separate input device."

**Issue:** Pressure detection is the operating principle of *resistive* touchscreens, not capacitive ones. Capacitive touchscreens detect changes in electrostatic capacitance caused by the electrical conductivity of a finger — they require no pressure and will not respond to a non-conductive object such as a gloved finger. The inclusion of "finger pressure" in the definition could lead students to confuse capacitive and resistive technologies, which are contrasted in tech/IT education. The main prose of the lesson does not repeat this error, but the `dfn` tooltip is the definition students will see on hover during revision.

**Correct version:** Remove "finger pressure" from the definition. The corrected tooltip: *"A touch-sensitive display that detects the electrical conductivity of a finger touching its surface (via changes in capacitance) to register touch. A light touch is sufficient — physical pressure is not needed. Used in smartphones, tablets and kiosks."*

**Fix required:** Edit the `dfn` tooltip for "capacitive touchscreen" in the `content_html` of L9.

**Source:** https://newhavendisplay.com/blog/capacitive-vs-resistive-touch/

---

### MEDIUM-2 — L10 (Operating Systems and Digital Platforms)

**Lesson ID:** `354e675f-7fa4-4c3b-b2df-34af32694fd0`

**Claim:** "Unix is the historical foundation from which both Linux and macOS evolved."

**Issue:** macOS genuinely evolved from Unix: Apple acquired NeXT in 1997, and NeXTSTEP was based on BSD — a direct Unix derivative. macOS's kernel (XNU) incorporates FreeBSD components and macOS is a certified UNIX system. However, Linux is **not** a Unix derivative. Linus Torvalds wrote the Linux kernel from scratch in 1991 as an independent reimplementation. His original 1991 announcement explicitly stated the kernel contained no Minix (or Unix) code. Linux is *Unix-like* and POSIX-compatible — designed to behave compatibly with Unix — but did not genealogically "evolve from" Unix. Describing both as having "evolved from Unix" gives students an inaccurate mental model of Linux's origin.

**Correct version:** *"macOS evolved from Unix via Apple's acquisition of NeXT, whose BSD-based operating system forms macOS's foundation. Linux is a separately written, Unix-inspired operating system created by Linus Torvalds in 1991 — it is Unix-like and POSIX-compatible but was not derived from Unix source code."*

**Fix required:** Edit the sentence about Unix in L10 `content_html`. The dfn tooltip for Unix currently reads "it forms the foundation for both Linux and macOS" — this also needs updating to distinguish direct descent (macOS) from reimplementation (Linux).

**Source:** https://en.wikipedia.org/wiki/Linux_kernel; https://en.wikipedia.org/wiki/MacOS

---

### LOW-1 — L10 (Operating Systems and Digital Platforms)

**Lesson ID:** `354e675f-7fa4-4c3b-b2df-34af32694fd0`

**Claim:** "Its HCI is almost entirely browser-based: apps run in Chrome tabs rather than as locally installed programs."

**Issue:** Accurate for Chrome OS at launch (2011) and in its early years, but Chrome OS has supported Android apps from the Google Play Store since 2016 and native Linux application containers (Crostini) since 2018. Modern Chromebooks can run locally installed Android and Linux apps alongside web applications. The statement "apps run in Chrome tabs rather than as locally installed programs" is outdated for devices running current Chrome OS. At OCR GCSE level the browser-first characterisation is the expected specification answer, so this is unlikely to cost exam marks, but the absolute wording is technically inaccurate.

**Recommended correction:** Soften to: *"apps run primarily through the Chrome browser and web-based applications, though modern Chromebooks also support Android apps from Google Play."*

**Source:** https://en.wikipedia.org/wiki/ChromeOS

---

## Clean lessons (0 findings)

| # | Lesson |
|---|--------|
| L11 | Choosing Devices and Distribution Channels for an Audience |
| L12 | User Interaction Methods and Digital Interactivity |

---

## Verified claims (PASS)

| Category | Verdict |
|---|---|
| Capacitive touchscreen: electrical charge detection principle | PASS (prose only — tooltip has MEDIUM error above) |
| OLED: each pixel generates its own light, deeper blacks, no backlight | PASS |
| LCD: requires backlight, cost-effective, less energy-efficient than OLED | PASS |
| E-ink: reflects ambient light, ultra-low power, ideal for outdoor/reading | PASS |
| RAM: temporary, volatile, affects interface responsiveness | PASS |
| Storage: permanent, holds files and apps between sessions | PASS |
| macOS Human Interface Guidelines (HIG) | PASS — HIG exists and is Apple's official design standard |
| iOS closed ecosystem, App Store approval required | PASS |
| Android open-source, multiple manufacturers, Google Play Store | PASS |
| Chrome OS: Chromebook, school use, browser-centric | PASS (with LOW caveat above) |
| Windows: dominant in business/education | PASS |
| Ubuntu: user-friendly Linux distribution | PASS |
| Unix: enterprise servers, academic systems, command-line primary | PASS |
| IoE device-to-device (M2M): automated, no human involvement | PASS |
| IoE human-to-device: person directly controls connected device | PASS |
| Gesture, keyboard, mouse, touch, voice: all five interaction methods | PASS — advantages and disadvantages accurate |
| Voice: unreliable in noisy environments, privacy (always-listening) | PASS |
| Haptic feedback: vibration-based tactile feedback for accessibility | PASS |
| Smartboard screen size 55–86 inches | PASS — consistent with industry spec |
| Smartphone screen size 5–7 inches | PASS |
| Smartwatch screen size 1–2 inches | PASS |
| Age demographics: tablets for children, smartphones for teens | PASS — consistent with Ofcom CMR data |
| Location demographic: urban vs rural broadband/5G access | PASS |
