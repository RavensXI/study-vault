# Fact-Check Report: Computer Science — Eduqas

**Subject slug:** `computer-science-eduqas`
**Lessons checked:** 29
**Date:** 2026-05-21

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH | 0 |
| MEDIUM | 1 |
| LOW | 1 |
| TOTAL ISSUES | 2 |

Most lessons are technically clean. The only issues are in the legislation lesson (Society, Ethics and the Law L2), which has one MEDIUM error in how it describes the Computer Misuse Act 1990 offence categories and penalties, and one LOW imprecision in how it characterises the relationship between RIPA 2000 and the Investigatory Powers Act 2016.

---

## Lesson-by-Lesson Results

### Unit: Hardware and Systems

#### L1 — The CPU and Von Neumann Architecture
**Result: PASS**

- Von Neumann described the stored-program architecture in 1945 — CORRECT. The First Draft of a Report on the EDVAC was distributed June 30, 1945.

#### L2 — Fetch-Decode-Execute and CPU Performance
**Result: PASS**

- Amdahl's Law: if 50% of a program must run sequentially, the maximum speedup is 2x. CORRECT — mathematically: S = 1/(0.5 + 0.5/∞) = 2. Gene Amdahl formulated this in 1967; the lesson does not name him but the description of the law is accurate.

#### L3 — Primary and Secondary Storage
**Result: PASS**

- CD capacity ~700 MB, DVD 4.7 GB (8.5 GB dual-layer), Blu-ray up to 50 GB — CORRECT.

#### L4 — Additional Hardware Components
No specific factual claims (no named inventors, dates, Acts, or protocol numbers).

#### L5 — Embedded Systems
No specific factual claims. The "30 billion embedded processors" figure is an illustrative estimate, not a precision claim.

---

### Unit: Networks, the Internet and Cybersecurity

#### L1 — Networks and Topologies
No specific factual claims. Topology descriptions are standard and accurate.

#### L2 — Network Hardware and Standards
**Result: PASS**

- IEEE 802.11ac operates on 5 GHz and supports speeds above 1 Gbps — CORRECT. The 802.11ac specification targets multi-station aggregate throughput of at least 1.1 Gbps. Single-link minimum is 500 Mbps; multi-station exceeds 1 Gbps.

#### L3 — The OSI 7-Layer Model and Protocols
No specific factual claims. OSI layer descriptions, HTTP at L7, TCP/UDP at L4, IP at L3, Ethernet at L2 — all standard and correct.

#### L4 — Packet Switching and Routing
No specific factual claims. No named inventors or specific dates cited.

#### L5 — The Internet: DNS, URLs and the Web Browser
No specific factual claims. DNS resolution and URL structure are correctly described.

#### L6 — Cybersecurity Threats and Defences
No specific factual claims. Threat and defence descriptions are general/definitional.

---

### Unit: Data Representation and Storage

#### L1 — Data Types and Number Systems
No specific factual claims. Binary/hex content is correct.

#### L2 — Signed Binary, Addition, Subtraction and Shifts
**Result: PASS**

- "Every mainstream CPU since the 1970s has used two's complement" — CORRECT.

#### L3 — Characters: ASCII and Unicode
**Result: PASS**

- ASCII approved June 17, 1963. Uses 7 bits, 128 codes (0–127). CORRECT.
- 'A' = 65, 'a' = 97, '0' = 48 — CORRECT (standard ASCII table values).
- Unicode currently defines over 140,000 characters — CORRECT (Unicode 15.1 defines 149,813 characters; codespace extends to 1,114,112).

#### L4 — Graphics: Pixels, Resolution and Colour Depth
No specific factual claims. 24-bit = 2^24 = 16,777,216 colours is correct. Bitmap formula is accurate.

#### L5 — Sound: Sampling and File Size
**Result: PASS**

- CD-quality audio = 44,100 Hz sample rate, 16-bit depth — CORRECT (Red Book standard).
- Nyquist theorem requires sample rate of at least twice the highest frequency — CORRECT.

#### L6 — Storage Units, Capacity and Compression
No specific factual claims. Binary prefix definitions (KiB = 1024 bytes), lossy/lossless format examples are all correct.

---

### Unit: Logic, Data Organisation and Operating Systems

#### L1 — Logical Operators and Truth Tables
No specific factual claims. AND, OR, NOT, XOR, NAND, NOR truth tables are all correct. NAND/NOR as universal gates is standard and accurate.

#### L2 — Boolean Algebra and Simplification
**Result: PASS**

- De Morgan's laws correctly stated: NOT(A AND B) = NOT A OR NOT B; NOT(A OR B) = NOT A AND NOT B.

#### L3 — Data Structures: Arrays, Records and File Design
No specific factual claims.

#### L4 — Operating Systems and Utility Software
No specific factual claims. NTFS/Windows, ext4/Linux, APFS/macOS attributions are correct.

---

### Unit: Algorithms, Programming and Software Development

#### L1 — Defining Algorithms: Pseudocode and Flowcharts
No specific factual claims.

#### L2 — Programming Constructs and Subroutines
No specific factual claims. Sequence/selection/iteration constructs are standard.

#### L3 — Searching: Linear and Binary
No specific factual claims. O(n) and O(log n) complexity claims are correct.

#### L4 — Sorting: Bubble and Merge
No specific factual claims. O(n²) bubble sort and O(n log n) merge sort are correct.

#### L5 — Validation, Verification and High-Level Languages
No specific factual claims.

#### L6 — IDE Tools, Translators and Errors
No specific factual claims. Compilation stages (lexical → syntax → semantic → code generation → optimisation) are correctly ordered.

---

### Unit: Society, Ethics and the Law

#### L1 — Ethical, Cultural, Environmental and Privacy Impacts
No specific factual claims requiring verification. The "~1% of global electricity" data centre figure is a widely cited estimate consistent with published research.

#### L2 — Legislation and Professional Standards
**Issues found: 1 MEDIUM, 1 LOW**

---

## Issues Detail

### MEDIUM — Computer Misuse Act 1990 s.1 described as a "summary offence" carrying "2 years"

**Lesson:** Society, Ethics and the Law L2  
**Lesson ID:** `ac495a73-e474-4186-8013-9aaa0d0a85f4`

**What the lesson says:**
> "Unauthorised access to computer material — hacking into a system you are not permitted to use, even if no data is taken. This is a summary offence, punishable by up to 2 years in prison."

**What is correct:**
Section 1 of the Computer Misuse Act 1990 is an **either-way offence** (made so by the Police and Justice Act 2006 — originally it was summary-only with a 6-month maximum). As it currently stands:
- **Summary conviction** (Magistrates' Court): maximum **12 months** imprisonment
- **On indictment** (Crown Court): maximum **2 years** imprisonment

Calling it "a summary offence, punishable by up to 2 years" is wrong on both counts: it is not summary-only, and 2 years is the indictment maximum, not the summary maximum.

**Why this matters:** Students who state in an exam that s.1 is "a summary offence carrying 2 years" will be factually incorrect. Mark schemes at GCSE level don't usually test penalty figures precisely, but the error conflates two trial modes and misrepresents the law.

**Suggested fix:**
> "Unauthorised access to computer material — hacking into a system you are not permitted to use, even if no data is taken. This is an either-way offence: tried in a Magistrates' Court it carries up to 12 months' imprisonment; tried in the Crown Court on indictment it carries up to 2 years' imprisonment."

**Source:** https://www.legislation.gov.uk/ukpga/1990/18/section/1

---

### LOW — RIPA 2000 described as merely "supplemented" by IPA 2016

**Lesson:** Society, Ethics and the Law L2  
**Lesson ID:** `ac495a73-e474-4186-8013-9aaa0d0a85f4`

**What the lesson says:**
> "RIPA was later supplemented by the Investigatory Powers Act 2016 (sometimes called the 'Snoopers' Charter'), which updated and extended the framework for bulk data collection and equipment interference by intelligence services."

**What is correct:**
The Investigatory Powers Act 2016 substantially **repealed and replaced** RIPA 2000's interception and communications data acquisition provisions — it did not merely "supplement" it. The word "supplemented" understates the scope of replacement. That said, significant portions of RIPA (covering covert surveillance and covert human intelligence sources) do remain in force and have not been repealed, so the full picture is nuanced. The GCSE-level description is not wholly wrong, but "supplemented" will leave students with the impression RIPA is still largely intact, which is misleading.

**Suggested fix:**
> "RIPA was later largely replaced — for interception and communications data — by the Investigatory Powers Act 2016 (sometimes called the 'Snoopers' Charter'), which also updated and extended surveillance powers; some covert surveillance provisions of RIPA remain in force."

**Source:** https://en.wikipedia.org/wiki/Investigatory_Powers_Act_2016

---

## Verified as Correct

| Claim | Lesson |
|-------|--------|
| Von Neumann architecture described in 1945 | Hardware L1 |
| Amdahl's Law: 50% sequential → max 2× speedup | Hardware L2 |
| CD/DVD/Blu-ray capacity figures | Hardware L3 |
| 802.11ac = 5 GHz, >1 Gbps multi-station | Networks L2 |
| ASCII approved 1963, 7-bit, A=65, a=97, 0=48 | Data Rep L3 |
| Unicode >140,000 characters | Data Rep L3 |
| CD audio: 44,100 Hz, 16-bit | Data Rep L5 |
| Nyquist theorem: sample rate ≥ 2× highest frequency | Data Rep L5 |
| De Morgan's laws (both forms) | Logic L2 |
| Computer Misuse Act 1990 — year and three offences | Society L2 |
| Copyright, Designs and Patents Act 1988 — year | Society L2 |
| Data Protection Act 2018 / UK GDPR — year and rights | Society L2 |
| FOI Act 2000 — 20 working day deadline | Society L2 |

---

`FACT_CHECK_DONE: subject=computer-science-eduqas lessons=29 high=0 medium=1 low=1`
