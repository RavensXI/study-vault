# Fact-Check: Electronics Eduqas (20 lessons)

**Date:** 2026-05-21
**Severity counts:** HIGH: 0 | MEDIUM: 0 | LOW: 1

---

## Summary

The Electronics Eduqas lesson set is technically sound. All specific verifiable claims — component values, IC pin assignments, timing formulae, standard codes, and historical attributions — were checked against authoritative sources (datasheets, IEC standards, IEEE/Wikipedia references) and found to be correct. One LOW-severity note was raised for an LED forward voltage approximation.

---

## Lesson-by-Lesson Findings

### L1 — Electronic Systems and Sub-Systems
No specific verifiable claims (named persons, dates, ICs, standards, numerical values). Content is descriptive. **No findings.**

---

### L2 — Circuit Symbols, Voltage and Current Rules
No specific verifiable claims requiring external verification. Kirchhoff's Voltage Law and Current Law are correctly stated. **No findings.**

---

### L3 — Ohm's Law, Power and Energy in Circuits
No specific verifiable claims. All three power equations (P=IV, P=I²R, P=V²/R) and E=Pt are standard and correct. **No findings.**

---

### L4 — Resistors in Series and Parallel; the E24 Series

**E24 values listed:** 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91
**Verdict: CORRECT.** Matches IEC 60063 exactly.

**Resistor colour code** (digit assignments, multipliers, tolerances including gold=±5%, silver=±10%, none=±20%)
**Verdict: CORRECT.** Matches IEC 60062.

---

### L5 — Sensing Circuits and Voltage Dividers

**[LOW] LED forward voltage — red ≈ 2V, blue/white ≈ 3V**
The red LED value (~2V) is fine (typical range 1.6–2.2V). Blue/white LEDs have a typical range of 3.0–3.6V; quoting "3V" is at the bottom of this range. This is the conventional GCSE teaching approximation and is consistent with what Eduqas data sheets typically provide in exams, so it is not a factual error at this level. However, if students encounter actual blue LEDs in practical work they may find forward voltages of 3.2–3.5V. Flagged as LOW for awareness only.

---

### L6 — Transistor and MOSFET Switching Circuits

**npn transistor V_BE ≈ 0.7V when on**
**Verdict: CORRECT.** Standard silicon BJT value; universally used as the GCSE approximation.

---

### L7 — Voltage Comparators
No specific verifiable claims beyond op-amp comparator function (correctly described). **No findings.**

---

### L8 — Diodes, Half-Wave Rectification and Zener Voltage Regulation

**Silicon diode forward voltage ≈ 0.7V; stays nearly constant over a wide range of currents**
**Verdict: CORRECT.** Accepted approximation, confirmed by all standard references.

---

### L9 — Logic Gates, Truth Tables and Boolean Algebra

**Boolean algebra attributed to George Boole, described as using only 0s and 1s**
**Verdict: CORRECT.** George Boole (1815–1864) developed the algebra in his 1847 and 1854 works. The binary 0/1 characterisation for digital applications is correct.

**NAND gate described as a universal gate**
**Verdict: CORRECT.** Standard result in digital logic.

---

### L10 — Designing Logic Systems and NAND-Only Implementations

**CMOS 4011 = four two-input NAND gates; CMOS 4001 = four two-input NOR gates**
**Verdict: CORRECT.** Confirmed from datasheets for both ICs.

**4011 pinout: pin 14 = V_DD, pin 7 = V_SS, 14-pin DIL package**
**Verdict: CORRECT.** Standard pinout for the CD4011. Confirmed from Texas Instruments and Nexperia datasheets.

**Pins numbered anticlockwise from pin 1 (notch/dot marks pin 1, top left)**
**Verdict: CORRECT.** Universal DIP/DIL pin-numbering convention — counterclockwise from the notch end.

---

### L11 — Amplifiers: Gain, Bandwidth and Clipping

**Bandwidth defined as the range between frequencies where gain falls to 70% of maximum (half-power / −3 dB points)**
**Verdict: CORRECT.** 0.707 × max voltage gain = 70%, corresponding to the −3 dB half-power point. Standard engineering definition.

**Audio bandwidth for full human hearing: 20 Hz to 20 kHz**
**Verdict: CORRECT.** Standard accepted range.

---

### L12 — Inverting and Non-Inverting Op-Amp Circuits
No specific verifiable claims beyond standard op-amp gain formulae (G = −Rf/R1 and G = 1 + Rf/R1), which are correct. **No findings.**

---

### L13 — Summing Amplifiers and Audio Mixer Systems
No specific verifiable claims. Audio chain order (source → preamp → summer → power amp → speaker) is correct. **No findings.**

---

### L14 — RC Time Delays and the 555 Monostable

**555 monostable formula T = 1.1 × R × C; capacitor charges to 2/3 Vcc**
**Verdict: CORRECT.** T = 1.1RC is the standard formula. The 1.1 factor comes from the 2/3 Vcc upper threshold of the internal comparator. Confirmed from LM555 datasheet.

**Trigger on pin 2 below 1/3 Vcc**
**Verdict: CORRECT.** Lower comparator threshold is 1/3 Vcc. Confirmed.

**555 output can source or sink up to 200 mA**
**Verdict: CORRECT.** LM555 datasheet specifies 200 mA maximum output current.

**555 described as an 8-pin IC containing comparator, bistable latch, discharge transistor, and voltage divider**
**Verdict: CORRECT.** The 555 timer contains two comparators, three 5kΩ resistors (voltage divider), an SR bistable latch, and an NPN discharge transistor on pin 7.

---

### L15 — 555 Astable Oscillators and Mark-Space Ratio

**Astable formulae: f = 1.44/(R1+2R2)C; T_ON = 0.7×(R1+R2)×C; T_OFF = 0.7×R2×C**
**Verdict: CORRECT.** All standard formulae for the 555 astable. Confirmed.

**Standard 555 astable cannot achieve 50% duty cycle unless R1 = 0 Ω**
**Verdict: CORRECT.** T_ON always exceeds T_OFF when R1 > 0 because the capacitor charges through both R1 and R2 but discharges through R2 only.

---

### L16 — D-Type Flip-Flops, Latches and Up-Counters

**D-type flip-flop is rising-edge triggered; Q copies D only at rising clock edge**
**Verdict: CORRECT.** Standard behaviour of the positive-edge-triggered D-type flip-flop.

---

### L17 — Binary, BCD and Decade Counters with 7-Segment Displays

**4017 produces 10 sequential HIGH outputs (Q0–Q9); pin 15 = MR (master reset)**
**Verdict: CORRECT.** CD4017 is a 16-pin IC; pin 15 is the active-HIGH master reset. Confirmed from datasheet.

**4017 modulo rule: connecting Q_N to MR gives modulo N (states 0 to N−1)**
**Verdict: CORRECT.** When Q_N fires the reset, that state is only a brief glitch; the counter counts N stable states.

**7-segment digit patterns (0–9) in the segment table**
**Verdict: CORRECT.** All 10 patterns verified against the standard encoding as documented by Wikipedia's seven-segment display character representations article.

---

### L18 — Schmitt Inverters and Interfacing Analogue to Digital
No specific verifiable claims (Schmitt trigger dual-threshold behaviour is correctly described). **No findings.**

---

### L19 — Microcontrollers and Flowchart Programming

**PIC = Peripheral Interface Controller**
**Verdict: CORRECT.** The original expansion of PIC was "Peripheral Interface Controller." Microchip no longer uses the acronym, but this expansion is historically accurate.

---

### L20 — Microcontroller Applications and System Evaluation

**ABS pulses brake hydraulics at around 15 times per second**
**Verdict: CORRECT.** Published ABS modulation frequency range is 5–15 Hz; 15 Hz is the upper end of the commonly cited range.

**Airbag: entire sequence from impact to full inflation takes around 30 milliseconds**
**Verdict: CORRECT.** Front airbags are fully inflated within approximately 20–30 ms from crash onset. "Around 30 ms" is within the published range.

---

## Verdict Table

| # | Lesson | Claim | Severity |
|---|--------|-------|----------|
| 1 | L5 Sensing Circuits | Blue/white LED forward voltage "3V" is at the low end of real range (3.0–3.6V) | LOW |

---

## Conclusion

20 lessons reviewed. No HIGH or MEDIUM issues found. One LOW note on LED forward voltage approximation (blue/white "3V" vs real range of 3.0–3.6V) — this is the standard GCSE teaching value and consistent with Eduqas exam data, so no content change is required.

FACT_CHECK_DONE: subject=electronics-eduqas lessons=20 high=0 medium=0 low=1
