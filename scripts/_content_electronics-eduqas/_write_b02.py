"""
Write batch b02 lesson JSONs with correct escaping.
Run: python scripts/_content_electronics-eduqas/_write_b02.py
"""
import json, os

OUT_DIR = os.path.join(os.path.dirname(__file__), "lessons")
os.makedirs(OUT_DIR, exist_ok=True)

# ── KaTeX helper: backslash is just a Python backslash in string literals here.
# json.dumps will escape them to \\ automatically.

# ─────────────────────────────────────────────
# LESSON 8: Diodes, Half-Wave Rectification and Zener Voltage Regulation
# ─────────────────────────────────────────────
L8 = {
  "_lesson_id": "1a7a7e2f-46ef-413f-9a9c-67ce84455904",
  "_lesson_number": 8,
  "_unit_slug": "discovering-electronics",
  "_lesson_slug": "diodes-half-wave-rectification-and-zener-voltage-regulation",
  "description": "I-V characteristics of silicon diodes, flyback protection, and zener voltage regulators.",
  "content_html": (
    '<h2 data-narration-id="n1">How Diodes Control Current Direction</h2>\n'
    '<p data-narration-id="n2">Diodes are two-terminal semiconductor devices that allow current to flow in one direction only. '
    'They sit at the heart of rectifier circuits and protection sub-systems, making them one of the most widely-used '
    'components in electronic design. In this lesson you will meet three roles the diode plays: passing current in a '
    'circuit, protecting inductive loads from voltage spikes, and maintaining a fixed output voltage in a regulator.</p>\n\n'
    '<h2 data-narration-id="n3">The I-V Characteristic of a Silicon Diode</h2>\n'
    '<p data-narration-id="n4">A <dfn class="term" data-def="A semiconductor device that permits conventional current to flow in one direction only, from anode to cathode.">silicon diode</dfn> '
    'has an anode (positive terminal) and a cathode (negative terminal). When the anode is more positive than the cathode, '
    'the diode is <dfn class="term" data-def="The condition in which the anode of a diode is at a higher potential than the cathode, allowing current to flow.">forward biased</dfn>. '
    'Current does not flow immediately; instead, the applied voltage must overcome the <strong>forward voltage drop</strong> before significant current passes. '
    'For a silicon diode this threshold is approximately 0.7&nbsp;V. Below 0.7&nbsp;V the diode behaves almost like an open circuit; '
    'above 0.7&nbsp;V it conducts freely and the voltage across it stays close to 0.7&nbsp;V regardless of how much current flows.</p>\n'
    '<p data-narration-id="n5">When the anode is more negative than the cathode the diode is <strong>reverse biased</strong>. '
    'Virtually no current flows &mdash; the diode blocks it. This one-way behaviour is what makes diodes useful for rectification and protection.</p>\n\n'
    '<div class="key-fact" data-narration-id="n6" data-revision-tip="Cover this and write down the forward voltage drop of a silicon diode, then explain what happens to that voltage as current through the diode doubles.">\n'
    '  <div class="key-fact-label">Key Fact</div>\n'
    '  <p>A forward-biased silicon diode drops approximately <strong>0.7&nbsp;V</strong> across it when conducting. '
    'This value stays nearly constant over a wide range of currents &mdash; it does not increase significantly as current rises.</p>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n7">Protection Diodes for Inductive Loads</h2>\n'
    '<p data-narration-id="n8">When a <dfn class="term" data-def="A component such as a relay coil, solenoid or motor whose magnetic field stores energy that is released as a voltage spike when current is switched off.">inductive load</dfn> '
    'is switched off, the collapsing magnetic field induces a large reverse voltage spike. This spike can exceed the breakdown voltage '
    'of a transistor switch and destroy it in microseconds. A <strong>flyback diode</strong> (also called a freewheeling or protection diode) '
    'is connected in reverse bias across the inductive load. During normal operation the diode is reverse biased and does not conduct. '
    'When the load is switched off and the spike appears, the diode becomes forward biased and provides a low-resistance path that safely dissipates the stored energy.</p>\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>Which loads need a flyback diode &mdash; and which do not</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    '    <p data-narration-id="n9">A flyback diode is <strong>only needed for electromagnetic (inductive) loads</strong>: relay coils, solenoids, and motors. These devices store energy in a magnetic field.</p>\n'
    '    <p data-narration-id="n10">A flyback diode is <strong>not needed for resistive loads</strong> such as lamps, heaters, or resistors. '
    'Resistors dissipate energy immediately and produce no voltage spike when switched off. '
    'A common exam error is placing a protection diode around a lamp &mdash; examiners specifically penalise this because it shows a misunderstanding of why the diode is there.</p>\n'
    '    <p data-narration-id="n11">Signal path for a relay circuit with flyback protection: '
    'Supply (+) &rarr; Transistor collector &rarr; Relay coil &rarr; Supply (&minus;). '
    'Flyback diode: cathode to collector end of relay coil, anode to the supply (&minus;) end &mdash; so it is reverse biased during normal operation.</p>\n'
    '  </div></div>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n12">Half-Wave Rectification</h2>\n'
    '<p data-narration-id="n13">Mains electricity is alternating current (AC) &mdash; the voltage repeatedly swings positive then negative. '
    'Many electronic circuits require direct current (DC). A single diode converts AC to a pulsating DC by blocking the negative half-cycles '
    'and allowing only the positive half-cycles to pass. This is called '
    '<dfn class="term" data-def="The conversion of alternating current to a pulsating direct current by allowing only the positive (or negative) half-cycles of the AC waveform to pass through a single diode.">half-wave rectification</dfn>.</p>\n'
    '<p data-narration-id="n14">The output of a half-wave rectifier is a series of positive pulses separated by gaps where the negative half-cycles were removed. '
    'The peak output voltage is the AC peak voltage minus the 0.7&nbsp;V diode forward drop. '
    'This pulsating DC is usually smoothed by a capacitor to give a steadier supply, though smoothing is a Component 2 topic and is not examined in this unit.</p>\n\n'
    '<div class="key-fact" data-narration-id="n15" data-revision-tip="Sketch the shape of the output waveform from a half-wave rectifier from memory &mdash; show which half-cycles are present and which are absent, and mark the 0.7 V diode drop.">\n'
    '  <div class="key-fact-label">Key Fact</div>\n'
    '  <p>In a half-wave rectifier, the diode passes the <strong>positive half-cycles</strong> and blocks the negative half-cycles. '
    'The output waveform shows repeated positive humps with gaps between them, not a continuous signal.</p>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n16">Zener Diodes and Voltage Regulation</h2>\n'
    '<p data-narration-id="n17">A <dfn class="term" data-def="A heavily doped semiconductor diode designed to operate in reverse breakdown at a precise voltage, used to maintain a stable output voltage in a regulator circuit.">zener diode</dfn> '
    'is a special type of diode that is deliberately operated in reverse breakdown. It is connected in reverse bias across the output of a power supply. '
    r'When the reverse voltage reaches the zener&rsquo;s <strong>breakdown voltage</strong> (also called the zener voltage, \(V_Z\)), '
    r'the diode conducts in reverse and clamps the voltage at exactly \(V_Z\). '
    'Zener diodes are available in standard ratings &mdash; common values include 3.3&nbsp;V, 5.1&nbsp;V, 5.6&nbsp;V, 6.2&nbsp;V, 9.1&nbsp;V, 12&nbsp;V and 15&nbsp;V.</p>\n\n'
    '<h2 data-narration-id="n18">How the Zener Regulator Works</h2>\n'
    r'<p data-narration-id="n19">The regulator circuit consists of a series resistor \(R_S\) connected between the unregulated supply \(V_{in}\) '
    'and the zener diode (cathode up to the supply, anode to 0&nbsp;V). The output is taken across the zener. '
    r'The series resistor drops the &ldquo;spare&rdquo; voltage \((V_{in} - V_Z)\) and limits the current through the zener to a safe value.</p>'
    '\n'
    r'<p data-narration-id="n20">The crucial point &mdash; and the most common exam misconception &mdash; is this: <strong>if \(V_{in}\) rises, the output voltage across the zener stays at \(V_Z\)</strong>. '
    'The extra voltage is absorbed by the series resistor. The zener achieves regulation by automatically increasing its conduction current to accommodate the higher input, '
    r'keeping \(V_{out} = V_Z\) constant. The output does <em>not</em> change when the supply fluctuates &mdash; that is the entire purpose of regulation.</p>'
    '\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>Worked example: sizing a zener regulator</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    '    <p data-narration-id="n21">A 5.1&nbsp;V zener diode is used to regulate a 9&nbsp;V unregulated supply. The maximum zener current allowed is 40&nbsp;mA. Calculate the minimum series resistance required.</p>\n'
    r'    <p data-narration-id="n22">Step 1 &mdash; find the voltage across the series resistor: $$V_{R_S} = V_{in} - V_Z = 9 - 5.1 = 3.9 \text{ V}$$</p>'
    '\n'
    r'    <p data-narration-id="n23">Step 2 &mdash; apply Ohm&rsquo;s law. Use the maximum allowed current to find the minimum resistance: $$R_S = \frac{V_{R_S}}{I_{Z(max)}} = \frac{3.9}{0.040} = 97.5 \text{ }\Omega$$</p>'
    '\n'
    r'    <p data-narration-id="n24">The nearest standard E24 value at or above 97.5&nbsp;&Omega; is <strong>100&nbsp;&Omega;</strong>, which keeps the zener current within its rating. Note: never use the zener power rating to calculate current in a regulator question &mdash; use \(I = V/R\) with the series resistor.</p>'
    '\n'
    '  </div></div>\n'
    '</div>\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>Common errors to avoid</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    '    <p data-narration-id="n25"><strong>Error 1 &mdash; adding a flyback diode to a lamp:</strong> Protection diodes are for electromagnetic loads only. A lamp is resistive; it stores no energy in a magnetic field. Adding a diode around it scores no marks and shows a conceptual error.</p>\n'
    r'    <p data-narration-id="n26"><strong>Error 2 &mdash; thinking \(V_{out}\) changes when \(V_{in}\) changes:</strong> The whole purpose of a zener regulator is that \(V_{out} = V_Z\) stays constant. If \(V_{in}\) increases, more current flows through \(R_S\), but \(V_{out}\) remains unchanged.</p>'
    '\n'
    '    <p data-narration-id="n27"><strong>Error 3 &mdash; drawing the half-wave rectifier output incorrectly:</strong> Only positive half-cycles appear at the output. The negative half-cycles are absent (not inverted). The positive humps are separated by flat periods at 0&nbsp;V, not by negative humps.</p>\n'
    '  </div></div>\n'
    '</div>'
  ),
  "exam_tip_html": (
    '<p data-narration-id="n28">On questions about the zener voltage regulator, examiners regularly award marks for stating that the output voltage stays constant when the input voltage increases &mdash; make this your opening sentence in any &lsquo;explain how the circuit works&rsquo; question. '
    'For half-wave rectifier output sketches, draw positive humps only and leave the negative half-cycle intervals flat at 0&nbsp;V (not inverted). '
    'For protection-diode questions, always start by identifying whether the load is inductive (relay, solenoid, motor) or resistive (lamp) before deciding whether a diode is needed.</p>'
  ),
  "conclusion_html": (
    '<h3 data-narration-id="n29">Key Takeaways</h3>\n'
    '<ul>\n'
    '  <li data-narration-id="n30">A silicon diode has a forward voltage drop of 0.7&nbsp;V and conducts in one direction only; reverse bias blocks current flow.</li>\n'
    '  <li data-narration-id="n31">A flyback protection diode is placed in reverse bias across inductive loads (relay coils, solenoids, motors) to suppress voltage spikes when the load is switched off &mdash; it is not needed for resistive loads such as lamps.</li>\n'
    r'  <li data-narration-id="n32">A zener diode operates in reverse breakdown to clamp the output voltage at its rated \(V_Z\); if the input voltage rises, the output stays constant &mdash; the extra voltage drops across the series resistor.</li>'
    '\n</ul>'
  ),
  "practice_questions": [
    {
      "text": "Which one of the following correctly describes a forward-biased silicon diode?\nA) Current flows freely from cathode to anode\nB) The voltage across the diode is approximately 0.7 V\nC) The diode blocks all current flow\nD) The diode requires at least 3 V before it conducts",
      "type": "1 mark — Multiple Choice",
      "marks": "B) The voltage across the diode is approximately 0.7 V [1 mark]"
    },
    {
      "text": "A student designs a transistor switch circuit to control a relay coil. State whether a flyback protection diode should be connected across the relay coil. Give a reason for your answer.",
      "type": "2 marks — State / Define",
      "marks": "Yes, a flyback diode is needed. [1 mark]\nThe relay coil is an inductive load; when switched off, the collapsing magnetic field produces a reverse voltage spike that could damage the transistor. The diode provides a safe path to dissipate this energy. [1 mark for correct reason]"
    },
    {
      "text": "A half-wave rectifier has an AC input with a peak voltage of 12 V. Calculate the peak output voltage of the rectifier. Show your working.",
      "type": "2 marks — Calculation: Single Step",
      "marks": "Peak output = 12 - 0.7 = 11.3 V [1 mark for correct subtraction, 1 mark for correct answer with unit]"
    },
    {
      "text": "A zener voltage regulator uses a 6.2 V zener diode. The unregulated input supply is 12 V and the maximum zener current must not exceed 50 mA.\n(a) Calculate the voltage across the series resistor.\n(b) Calculate the minimum value of series resistance needed.",
      "type": "4 marks — Calculation: Multi-Step",
      "marks": "(a) Voltage across series resistor = 12 - 6.2 = 5.8 V [1 mark]\n(b) R = V / I = 5.8 / 0.050 = 116 ohms [1 mark for correct substitution, 1 mark for answer]\nNearest standard E24 value at or above 116 ohms is 120 ohms [1 mark]"
    },
    {
      "text": "A student builds a zener regulator with a 5.1 V zener diode. The input voltage is increased from 9 V to 12 V. Describe and explain the effect on the output voltage.",
      "type": "4 marks — Describe Circuit Operation",
      "marks": "The output voltage remains at 5.1 V (unchanged). [1 mark]\nThe zener diode operates in reverse breakdown and clamps the output at its rated breakdown voltage. [1 mark]\nThe increase in input voltage causes the voltage across the series resistor to increase. [1 mark]\nThe additional current drawn through the series resistor increases, but the zener maintains a constant output voltage. [1 mark]"
    },
    {
      "text": "A circuit uses a transistor switch to drive a 9 V DC motor. The transistor has a maximum collector current of 200 mA and the motor requires 150 mA to run. Analyse whether a flyback protection diode is needed, and describe where it should be placed in the circuit. Justify your answer with reference to the type of load and the risk to the transistor.",
      "type": "8 marks — Extended Response: Circuit Analysis and Evaluation",
      "marks": "Mastering: Correctly identifies the motor as an inductive load that stores energy in its magnetic field. States clearly that when the transistor switches off, the collapsing field induces a back-EMF that appears as a reverse voltage spike across the transistor. Explains that the flyback diode must be connected in reverse bias across the motor (cathode to the positive supply rail, anode to the collector) so it is non-conducting during normal operation but conducts to clamp the spike when the motor is switched off. Notes that without the diode the spike could exceed the transistor breakdown voltage and destroy it. Conclusion states the diode is necessary and positions it correctly.\nSecure: Identifies the motor as inductive, states a voltage spike occurs on switch-off, explains the diode placement correctly, and gives a reason why protection is needed.\nDeveloping: Correctly identifies the motor needs a protection diode but placement or explanation of the spike mechanism is incomplete.\nEmerging: States a diode is needed but without correct reasoning about the load type or the spike."
    }
  ],
  "knowledge_checks": [
    {
      "type": "mcq",
      "q": "What is the approximate forward voltage drop across a conducting silicon diode?",
      "options": ["0.3 V", "0.7 V", "1.4 V", "3.3 V"],
      "correct": 1
    },
    {
      "type": "mcq",
      "q": "A zener regulator has a 9.1 V zener diode. The input supply rises from 12 V to 15 V. What happens to the output voltage?",
      "options": ["It rises to 12.1 V", "It stays at 9.1 V", "It falls to 6 V", "It equals the input voltage minus 0.7 V"],
      "correct": 1
    },
    {
      "type": "fill",
      "q": "A flyback protection diode is needed across a relay coil because the coil is an _____ load that produces a voltage spike when switched off.",
      "options": ["resistive", "capacitive", "inductive", "optical"],
      "correct": 2
    },
    {
      "type": "fill",
      "q": "In a half-wave rectifier, the diode allows only the _____ half-cycles of the AC input to reach the output.",
      "options": ["negative", "both", "positive", "alternating"],
      "correct": 2
    },
    {
      "type": "match",
      "q": "Match each term to its correct description:",
      "left": ["Forward voltage drop", "Zener voltage", "Half-wave rectification"],
      "right": ["The voltage at which a zener diode conducts in reverse breakdown", "Converting AC to pulsating DC using a single diode", "The 0.7 V drop across a conducting silicon diode"],
      "order": [2, 0, 1]
    }
  ],
  "flashcard_questions": [
    {"q": "What is the forward voltage drop of a conducting silicon diode?", "a": "Approximately 0.7 V."},
    {"q": "In which direction does conventional current flow through a diode?", "a": "From anode to cathode (positive to negative terminal)."},
    {"q": "What is reverse bias in a diode?", "a": "When the cathode is at a higher potential than the anode, blocking current flow."},
    {"q": "Why must a flyback diode be placed across a relay coil?", "a": "To provide a safe path for the voltage spike produced when the coil magnetic field collapses."},
    {"q": "Does a lamp require a flyback protection diode when switched off?", "a": "No — a lamp is a resistive load and produces no voltage spike."},
    {"q": "Which three types of electromagnetic load require a flyback protection diode?", "a": "Relay coils, solenoids, and motors."},
    {"q": "What does half-wave rectification convert AC into?", "a": "A pulsating DC signal with only positive half-cycles present."},
    {"q": "A half-wave rectifier has a peak AC input of 10 V. What is the peak output voltage?", "a": "9.3 V (10 minus the 0.7 V diode forward drop)."},
    {"q": "What is the purpose of a zener diode in a regulator circuit?", "a": "To maintain a constant output voltage equal to its breakdown (zener) voltage."},
    {"q": "A zener regulator input voltage increases. What happens to the output voltage?", "a": "It stays constant at the zener voltage; extra voltage drops across the series resistor."},
    {"q": "In a zener regulator, which component drops the excess voltage above the zener voltage?", "a": "The series resistor."},
    {"q": "How is the minimum series resistance in a zener regulator calculated?", "a": "R = (Vin minus Vz) divided by Iz max, using Ohm's law."}
  ],
  "glossary_terms": [
    {"term": "silicon diode", "definition": "A semiconductor device that permits conventional current to flow in one direction only, from anode to cathode."},
    {"term": "forward biased", "definition": "The condition in which the anode of a diode is at a higher potential than the cathode, allowing current to flow."},
    {"term": "inductive load", "definition": "A component such as a relay coil, solenoid or motor whose magnetic field stores energy that is released as a voltage spike when current is switched off."},
    {"term": "half-wave rectification", "definition": "The conversion of alternating current to a pulsating direct current by allowing only the positive (or negative) half-cycles of the AC waveform to pass through a single diode."},
    {"term": "zener diode", "definition": "A heavily doped semiconductor diode designed to operate in reverse breakdown at a precise voltage, used to maintain a stable output voltage in a regulator circuit."}
  ],
  "hero_keywords": ["silicon diode electronics component", "electronic circuit board", "semiconductor components"],
  "hero_image_caption": "Silicon diodes and components on an electronics circuit board"
}

# ─────────────────────────────────────────────
# LESSON 9: Logic Gates, Truth Tables and Boolean Algebra
# ─────────────────────────────────────────────
L9 = {
  "_lesson_id": "15402a2e-52be-4d47-8cf9-d81a172885f5",
  "_lesson_number": 9,
  "_unit_slug": "discovering-electronics",
  "_lesson_slug": "logic-gates-truth-tables-and-boolean-algebra",
  "description": "NOT, AND, OR, NAND and NOR gates: truth tables, Boolean expressions and tied-input configurations.",
  "content_html": (
    '<h2 data-narration-id="n1">Two-State Logic: The Language of Digital Electronics</h2>\n'
    '<p data-narration-id="n2">Every digital circuit, from a simple alarm to a microprocessor, is built from components that work with just two voltage levels. '
    'Logic 1 (HIGH) represents a voltage near the supply rail; Logic 0 (LOW) represents a voltage near 0&nbsp;V. '
    'This two-state system is called <dfn class="term" data-def="A digital system that uses only two voltage levels — Logic 1 (HIGH) and Logic 0 (LOW) — to represent and process information.">binary logic</dfn>. '
    'Because there are only two states, every circuit decision can be described mathematically using '
    '<dfn class="term" data-def="A form of algebra using only the values 0 and 1, used to describe and simplify digital logic circuits.">Boolean algebra</dfn> &mdash; '
    'a branch of mathematics developed by George Boole that uses only 0s and 1s.</p>\n'
    '<p data-narration-id="n3">A logic gate is a small integrated circuit with one or two inputs and a single output. '
    'The output depends entirely on the combination of inputs at that moment. '
    'The relationship between inputs and output is described in a '
    '<dfn class="term" data-def="A table that lists every possible combination of input values for a logic gate or circuit, together with the resulting output for each combination.">truth table</dfn> '
    'and captured in a Boolean expression. You need to know five gates for your exam: NOT, AND, OR, NAND and NOR.</p>\n\n'
    '<h2 data-narration-id="n4">The NOT Gate</h2>\n'
    '<p data-narration-id="n5">The NOT gate (or inverter) has one input and one output. It simply inverts the input: a Logic 1 input produces a Logic 0 output, and vice versa. '
    r'The Boolean expression uses a bar (overline) to denote inversion: if the input is A, the output is \(\overline{A}\).</p>'
    '\n\n'
    '<table data-narration-id="n6">\n'
    '  <caption>NOT gate truth table</caption>\n'
    '  <thead><tr><th>A (input)</th><th>Q (output)</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr><td>0</td><td>1</td></tr>\n'
    '    <tr><td>1</td><td>0</td></tr>\n'
    '  </tbody>\n'
    '</table>\n\n'
    '<h2 data-narration-id="n7">The AND Gate</h2>\n'
    '<p data-narration-id="n8">The AND gate has two (or more) inputs. The output is Logic 1 only when <strong>all</strong> inputs are Logic 1. '
    'If any input is 0, the output is 0. '
    r'The Boolean expression uses a dot (or no symbol) to represent AND: \(Q = A \cdot B\) or simply \(Q = AB\).</p>'
    '\n\n'
    '<table data-narration-id="n9">\n'
    '  <caption>AND gate truth table</caption>\n'
    '  <thead><tr><th>A</th><th>B</th><th>Q = A &middot; B</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr><td>0</td><td>0</td><td>0</td></tr>\n'
    '    <tr><td>0</td><td>1</td><td>0</td></tr>\n'
    '    <tr><td>1</td><td>0</td><td>0</td></tr>\n'
    '    <tr><td>1</td><td>1</td><td>1</td></tr>\n'
    '  </tbody>\n'
    '</table>\n\n'
    '<h2 data-narration-id="n10">The OR Gate</h2>\n'
    '<p data-narration-id="n11">The OR gate output is Logic 1 when <strong>at least one</strong> input is Logic 1. '
    'Only when all inputs are 0 is the output 0. '
    r'The Boolean expression uses a plus sign: \(Q = A + B\).</p>'
    '\n\n'
    '<table data-narration-id="n12">\n'
    '  <caption>OR gate truth table</caption>\n'
    '  <thead><tr><th>A</th><th>B</th><th>Q = A + B</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr><td>0</td><td>0</td><td>0</td></tr>\n'
    '    <tr><td>0</td><td>1</td><td>1</td></tr>\n'
    '    <tr><td>1</td><td>0</td><td>1</td></tr>\n'
    '    <tr><td>1</td><td>1</td><td>1</td></tr>\n'
    '  </tbody>\n'
    '</table>\n\n'
    '<h2 data-narration-id="n13">The NAND Gate</h2>\n'
    '<p data-narration-id="n14">The <dfn class="term" data-def="A logic gate whose output is the inverse of an AND gate: the output is Logic 0 only when all inputs are Logic 1.">NAND gate</dfn> '
    'is an AND gate followed by a NOT. Its output is Logic 0 only when <strong>all</strong> inputs are Logic 1 &mdash; it is 1 in every other case. '
    r'The Boolean expression is \(Q = \overline{A \cdot B}\).</p>'
    '\n\n'
    '<table data-narration-id="n15">\n'
    '  <caption>NAND gate truth table</caption>\n'
    '  <thead><tr><th>A</th><th>B</th><th>Q</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr><td>0</td><td>0</td><td>1</td></tr>\n'
    '    <tr><td>0</td><td>1</td><td>1</td></tr>\n'
    '    <tr><td>1</td><td>0</td><td>1</td></tr>\n'
    '    <tr><td>1</td><td>1</td><td>0</td></tr>\n'
    '  </tbody>\n'
    '</table>\n\n'
    '<div class="key-fact" data-narration-id="n16" data-revision-tip="Cover this table and write out the NAND truth table from memory for inputs 00, 01, 10, 11 &mdash; remember it is the exact opposite of AND.">\n'
    '  <div class="key-fact-label">Key Fact</div>\n'
    '  <p>The NAND gate is the exact inverse of AND. It is the most important gate in electronics because any logic function can be built from NAND gates alone &mdash; making it a <strong>universal gate</strong>.</p>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n17">The NOR Gate</h2>\n'
    '<p data-narration-id="n18">The <dfn class="term" data-def="A logic gate whose output is the inverse of an OR gate: the output is Logic 1 only when all inputs are Logic 0.">NOR gate</dfn> '
    'is an OR gate followed by a NOT. Its output is Logic 1 only when <strong>all</strong> inputs are Logic 0. '
    r'The Boolean expression is \(Q = \overline{A + B}\).</p>'
    '\n\n'
    '<table data-narration-id="n19">\n'
    '  <caption>NOR gate truth table</caption>\n'
    '  <thead><tr><th>A</th><th>B</th><th>Q</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr><td>0</td><td>0</td><td>1</td></tr>\n'
    '    <tr><td>0</td><td>1</td><td>0</td></tr>\n'
    '    <tr><td>1</td><td>0</td><td>0</td></tr>\n'
    '    <tr><td>1</td><td>1</td><td>0</td></tr>\n'
    '  </tbody>\n'
    '</table>\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>NAND configured as a NOT gate (tied input)</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    '    <p data-narration-id="n20">A NAND gate can act as a NOT gate if both inputs are connected together or if one input is tied permanently to Logic 1. '
    'When both inputs equal A, the truth table becomes: if A=0, output=1; if A=1, output=0 &mdash; identical to a NOT gate.</p>\n'
    r'    <p data-narration-id="n21">This is a frequently-examined configuration. If you see a NAND gate symbol where the two inputs share the same signal, or where one input is connected to the supply rail (Logic 1), treat it as a NOT gate. Writing its output as \(\overline{A \cdot A} = \overline{A}\) confirms the equivalence.</p>'
    '\n'
    r'    <p data-narration-id="n22">A common exam error: treating a NAND gate with one input at Logic 1 as if it were still a two-input NAND. When input B is permanently 1, the gate simplifies to \(Q = \overline{A \cdot 1} = \overline{A}\). The second input drops out of the expression entirely.</p>'
    '\n'
    '  </div></div>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n23">Writing Boolean Expressions</h2>\n'
    '<p data-narration-id="n24">A Boolean expression describes the output of a logic circuit in terms of its inputs. '
    r'For a circuit with three inputs A, B and C passing through an AND gate and an OR gate, the expression might be \(Q = A \cdot B + C\). '
    'Boolean algebra follows operator precedence: NOT is evaluated first, then AND (multiplication), then OR (addition). Brackets override this order just as in ordinary algebra.</p>\n'
    '<p data-narration-id="n25">For this course, expressions are kept to a maximum of three inputs. '
    r'A typical sum-of-products expression for three inputs might look like \(Q = A \cdot B \cdot C + A \cdot \overline{B} \cdot C\). '
    'You are not required to simplify Boolean expressions &mdash; being able to write them from a truth table and from a circuit is the key skill.</p>\n\n'
    '<div class="key-fact" data-narration-id="n26" data-revision-tip="Write the Boolean operator symbols for NOT, AND and OR from memory, then use them to write the expression for a three-input AND gate followed by a NOT gate.">\n'
    '  <div class="key-fact-label">Key Fact</div>\n'
    r'  <p>Boolean notation: NOT uses a bar over the variable (\(\overline{A}\)); AND uses a dot or no symbol (\(A \cdot B\) or \(AB\)); OR uses a plus sign (\(A + B\)). Operator precedence: NOT first, then AND, then OR.</p>'
    '\n</div>\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>Building a truth table for a three-input logic circuit</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    r'    <p data-narration-id="n27">A three-input truth table has \(2^3 = 8\) rows (one for every combination of 0s and 1s). Always list them in binary counting order: 000, 001, 010, 011, 100, 101, 110, 111. This guarantees you do not miss any combination.</p>'
    '\n'
    r'    <p data-narration-id="n28">To fill in the output column, evaluate the Boolean expression for each row by substituting the values of A, B and C. For \(Q = A \cdot B + C\): when A=1, B=0, C=1, \(Q = 1 \cdot 0 + 1 = 0 + 1 = 1\). Work methodically one row at a time; rushing is where most errors creep in.</p>'
    '\n'
    '  </div></div>\n'
    '</div>'
  ),
  "exam_tip_html": (
    '<p data-narration-id="n29">For truth table questions, always list all input combinations in binary counting order (start at 000 or 00 and count up) so you cannot accidentally miss a row &mdash; missing a row drops you from full to partial marks. '
    'For Boolean expression questions, use correct notation: a dot or no symbol for AND, a plus sign for OR, and an overline (described in words as &lsquo;bar A&rsquo; or &lsquo;NOT A&rsquo;) for inversion. '
    r'If you see a NAND gate with both inputs connected to the same signal, or with one input permanently at Logic 1, write its output as \(\overline{A}\) &mdash; it behaves as a NOT gate.</p>'
  ),
  "conclusion_html": (
    '<h3 data-narration-id="n30">Key Takeaways</h3>\n'
    '<ul>\n'
    r'  <li data-narration-id="n31">The five gates to know are NOT (\(\overline{A}\)), AND (\(AB\)), OR (\(A+B\)), NAND (\(\overline{AB}\)) and NOR (\(\overline{A+B}\)). NAND output is 0 only when all inputs are 1; NOR output is 1 only when all inputs are 0.</li>'
    '\n'
    '  <li data-narration-id="n32">A truth table lists every input combination (in binary order) and the resulting output. '
    'A three-input circuit has 8 rows; a four-input circuit has 16 rows.</li>\n'
    r'  <li data-narration-id="n33">A NAND gate with both inputs tied together (or one input permanently at Logic 1) behaves as a NOT gate, giving output \(\overline{A}\). This is a core exam configuration &mdash; do not treat it as a two-input NAND.</li>'
    '\n</ul>'
  ),
  "practice_questions": [
    {
      "text": "Which one of the following best describes the output of a NOR gate?\nA) Logic 1 only when at least one input is Logic 1\nB) Logic 0 only when all inputs are Logic 1\nC) Logic 1 only when all inputs are Logic 0\nD) Logic 0 only when all inputs are Logic 0",
      "type": "1 mark — Multiple Choice",
      "marks": "C) Logic 1 only when all inputs are Logic 0 [1 mark]"
    },
    {
      "text": "State the Boolean expression for the output of a two-input NAND gate with inputs A and B.",
      "type": "2 marks — State / Define",
      "marks": "Q = NOT(A AND B), shown as Q with overline(AB). [1 mark for correct inputs identified, 1 mark for correct inversion shown]"
    },
    {
      "text": "Complete the truth table for the logic expression Q = A AND B OR C (Q = AB + C).\n\nA | B | C | Q\n0 | 0 | 0 | ?\n0 | 0 | 1 | ?\n0 | 1 | 0 | ?\n0 | 1 | 1 | ?\n1 | 0 | 0 | ?\n1 | 0 | 1 | ?\n1 | 1 | 0 | ?\n1 | 1 | 1 | ?",
      "type": "3 marks — Complete the Truth Table",
      "marks": "Correct output column: 0, 1, 0, 1, 0, 1, 1, 1\n[3 marks: deduct 1 mark for each pair of rows containing an error, minimum 0]"
    },
    {
      "text": "A NAND gate has input A connected to a logic signal and input B permanently connected to Logic 1.\n(a) Write the Boolean expression for the output Q in its simplified form.\n(b) Name the logic function this NAND gate now performs.",
      "type": "4 marks — Describe Circuit Operation",
      "marks": "(a) Q = NOT(A AND 1) = NOT A = overline(A) [2 marks: 1 for correct substitution of B=1, 1 for correct simplification]\n(b) NOT gate (inverter) [2 marks]"
    },
    {
      "text": "Design a logic sub-system that outputs Logic 1 when input A is Logic 1 AND input B is Logic 0. Draw the truth table for your circuit, write the Boolean expression, and identify which gate(s) are needed.",
      "type": "5 marks — Design a Sub-System",
      "marks": "Truth table (4 rows) showing A=1, B=0 as the only row giving Q=1. [1 mark]\nBoolean expression: Q = A AND NOT B = A . overline(B). [1 mark]\nNeed a NOT gate on input B, then an AND gate combining A and the NOT-B signal. [2 marks: 1 for identifying NOT gate, 1 for identifying AND gate]\nCorrect gate count or circuit description. [1 mark]"
    },
    {
      "text": "A student claims that the output of a NAND gate and an AND gate are identical. Evaluate this claim and explain the difference between the two gates, using truth tables and Boolean expressions to support your answer.",
      "type": "8 marks — Extended Response: Circuit Analysis and Evaluation",
      "marks": "Mastering: Clearly refutes the claim with a complete AND truth table and a complete NAND truth table, showing that the output columns are exact inverses of each other. Uses correct Boolean notation (Q = AB for AND, Q = overline(AB) for NAND). Explains that NAND is AND followed by inversion. Notes the practical significance: NAND is a universal gate from which any logic function can be realised, while AND alone is not universal. Conclusion explicitly contrasts the two.\nSecure: Produces both truth tables correctly, identifies the outputs are inverted, gives correct Boolean expressions. May omit the universal gate discussion.\nDeveloping: At least one truth table correct; Boolean expression for one gate correct; partial explanation of the difference.\nEmerging: Attempts a truth table or Boolean expression but with errors; minimal explanation."
    }
  ],
  "knowledge_checks": [
    {
      "type": "mcq",
      "q": "What is the output of an AND gate when input A = 1 and input B = 0?",
      "options": ["0", "1", "Depends on the supply voltage", "Neither 0 nor 1"],
      "correct": 0
    },
    {
      "type": "mcq",
      "q": "A NAND gate has both inputs permanently connected together to signal A. Which gate does it now behave as?",
      "options": ["AND gate", "OR gate", "NOT gate", "NOR gate"],
      "correct": 2
    },
    {
      "type": "fill",
      "q": "The Boolean expression for a two-input OR gate with inputs A and B is Q = A _____ B.",
      "options": ["· (dot)", "+ (plus)", "overline", "÷"],
      "correct": 1
    },
    {
      "type": "fill",
      "q": "A three-input truth table has _____ rows, one for every possible combination of inputs.",
      "options": ["4", "6", "8", "16"],
      "correct": 2
    },
    {
      "type": "match",
      "q": "Match each logic gate to its rule for a Logic 1 output:",
      "left": ["AND gate", "OR gate", "NOR gate"],
      "right": ["Output is 1 only when all inputs are 0", "Output is 1 when at least one input is 1", "Output is 1 only when all inputs are 1"],
      "order": [2, 1, 0]
    }
  ],
  "flashcard_questions": [
    {"q": "What is the output of a NOT gate when the input is Logic 1?", "a": "Logic 0."},
    {"q": "What is the Boolean symbol for the AND operation?", "a": "A dot (.) or no symbol between variables, e.g. A.B or AB."},
    {"q": "What is the Boolean symbol for the OR operation?", "a": "A plus sign (+), e.g. A + B."},
    {"q": "When does an AND gate output Logic 1?", "a": "Only when all inputs are Logic 1."},
    {"q": "When does a NAND gate output Logic 0?", "a": "Only when all inputs are Logic 1."},
    {"q": "When does a NOR gate output Logic 1?", "a": "Only when all inputs are Logic 0."},
    {"q": "How many rows does a truth table with two inputs have?", "a": "4 rows (2 squared = 4)."},
    {"q": "How many rows does a truth table with three inputs have?", "a": "8 rows (2 cubed = 8)."},
    {"q": "A NAND gate has input B permanently tied to Logic 1. What does the output simplify to?", "a": "NOT A, because NOT(A AND 1) = NOT A."},
    {"q": "What is Boolean algebra?", "a": "A form of algebra using only 0 and 1, used to describe digital logic circuits."},
    {"q": "What is operator precedence in Boolean algebra?", "a": "NOT first, then AND, then OR (brackets override this order)."},
    {"q": "What is a truth table?", "a": "A table listing every input combination and the resulting logic output."}
  ],
  "glossary_terms": [
    {"term": "binary logic", "definition": "A digital system that uses only two voltage levels — Logic 1 (HIGH) and Logic 0 (LOW) — to represent and process information."},
    {"term": "Boolean algebra", "definition": "A form of algebra using only the values 0 and 1, used to describe and simplify digital logic circuits."},
    {"term": "truth table", "definition": "A table that lists every possible combination of input values for a logic gate or circuit, together with the resulting output for each combination."},
    {"term": "NAND gate", "definition": "A logic gate whose output is the inverse of an AND gate: the output is Logic 0 only when all inputs are Logic 1."},
    {"term": "NOR gate", "definition": "A logic gate whose output is the inverse of an OR gate: the output is Logic 1 only when all inputs are Logic 0."}
  ],
  "hero_keywords": ["logic circuit board digital electronics", "computer chip microchip", "digital electronics gates"],
  "hero_image_caption": "Digital logic gates and truth tables on a circuit board"
}

# ─────────────────────────────────────────────
# LESSON 10: Designing Logic Systems and NAND-Only Implementations
# ─────────────────────────────────────────────
L10 = {
  "_lesson_id": "8daca76e-54cb-4154-a3c0-d8b17455b4b2",
  "_lesson_number": 10,
  "_unit_slug": "discovering-electronics",
  "_lesson_slug": "designing-logic-systems-and-nand-only-implementations",
  "description": "Design logic circuits from a written spec and convert any gate system to NAND gates only.",
  "content_html": (
    '<h2 data-narration-id="n1">From Problem Statement to Logic Circuit</h2>\n'
    '<p data-narration-id="n2">Logic design starts with a written specification &mdash; a statement describing exactly when the output should be Logic 1. '
    'Your job is to translate that statement into a truth table, extract a Boolean expression, and select the gates to build it. '
    'This three-step pipeline is tested in nearly every exam paper and is the foundation of all digital design work.</p>\n'
    '<p data-narration-id="n3">Once you can design with standard gates, you will learn the most important conversion skill in this unit: '
    'replacing every gate in a circuit with <dfn class="term" data-def="Replacing every standard logic gate in a circuit with an equivalent combination of NAND gates, so the circuit uses only NAND gates throughout.">NAND-only implementation</dfn>. '
    'This matters because NAND gates are universal &mdash; any logic function can be built from them. '
    'In practice, a designer who needs only one type of IC can buy a single 4-NAND chip (such as the CMOS 4011) and implement any function without stocking multiple gate types.</p>\n\n'
    '<h2 data-narration-id="n4">Step 1 &mdash; Design from a Specification</h2>\n'
    '<p data-narration-id="n5">Consider a burglar alarm that should activate (output = 1) when the door sensor (A) is 1 <strong>and</strong> the motion sensor (B) is 1, '
    '<strong>or</strong> when the panic button (C) is pressed (1). '
    r'The Boolean expression is \(Q = A \cdot B + C\). '
    r'The truth table has 8 rows (three inputs, \(2^3 = 8\) combinations). Rows where A=1 and B=1, or C=1, give Q=1.</p>'
    '\n'
    '<p data-narration-id="n6">The gate realisation needs an AND gate (inputs A and B) feeding into an OR gate alongside input C. '
    'This is a standard <dfn class="term" data-def="A Boolean expression written as the OR of one or more AND terms, each AND term being a product of input variables or their complements.">sum of products</dfn> form. '
    'Most combinational logic specifications can be written as a sum of products, making the gate selection straightforward.</p>\n\n'
    '<div class="key-fact" data-narration-id="n7" data-revision-tip="Cover this and write down the three-step logic design process: from specification to truth table to Boolean expression to gate circuit.">\n'
    '  <div class="key-fact-label">Key Fact</div>\n'
    '  <p>The three steps for logic design: (1) write the truth table from the specification; (2) write the Boolean expression from the rows where Q=1; '
    '(3) select the gates that match the expression. Every logic design question on the exam follows this pipeline.</p>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n8">NAND Equivalents for Each Gate</h2>\n'
    '<p data-narration-id="n9">The conversion to NAND-only is systematic. There is a known NAND equivalent for every standard gate. '
    'Learn these four equivalents and the conversion becomes mechanical:</p>\n\n'
    '<table data-narration-id="n10">\n'
    '  <caption>NAND equivalents for standard logic gates</caption>\n'
    '  <thead><tr><th>Standard gate</th><th>NAND-only equivalent</th><th>Boolean check</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr>\n'
    '      <td>NOT (A)</td>\n'
    '      <td>One NAND gate with both inputs tied to A</td>\n'
    r'      <td>\(\overline{A \cdot A} = \overline{A}\)</td>'
    '\n    </tr>\n'
    '    <tr>\n'
    '      <td>AND (A, B)</td>\n'
    '      <td>One NAND followed by a tied-input NOT-NAND on its output</td>\n'
    r'      <td>\(\overline{\overline{A \cdot B}} = A \cdot B\)</td>'
    '\n    </tr>\n'
    '    <tr>\n'
    '      <td>OR (A, B)</td>\n'
    '      <td>NOT-NAND each input separately, then combine with a third NAND</td>\n'
    r'      <td>\(\overline{\overline{A} \cdot \overline{B}} = A + B\)</td>'
    '\n    </tr>\n'
    '    <tr>\n'
    '      <td>NOR (A, B)</td>\n'
    '      <td>OR-equivalent (three NANDs) followed by a tied-input NOT-NAND</td>\n'
    r'      <td>\(\overline{A + B}\)</td>'
    '\n    </tr>\n'
    '  </tbody>\n'
    '</table>\n\n'
    '<div class="key-fact" data-narration-id="n11" data-revision-tip="Close this page and draw the NAND-only equivalents for NOT, AND and OR from memory &mdash; label each input and show where both inputs of the NOT-NAND connect.">\n'
    '  <div class="key-fact-label">Key Fact</div>\n'
    '  <p>The three most important NAND equivalents: NOT = one NAND with inputs tied together; AND = NAND followed by a tied-input NAND on its output; '
    'OR = NOT-NAND each input separately, then combine with a third NAND.</p>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n12">The Conversion Algorithm &mdash; Three Steps</h2>\n'
    '<p data-narration-id="n13">When the exam asks you to convert a circuit to NAND only, follow this exact sequence:</p>\n'
    '<p data-narration-id="n14"><strong>Step 1 &mdash; Redraw with NAND equivalents.</strong> Replace each gate in the original circuit with its NAND equivalent from the table above. '
    'The intermediate circuit will now contain only NAND gates &mdash; but it may have more gates than necessary.</p>\n'
    '<p data-narration-id="n15"><strong>Step 2 &mdash; Identify back-to-back (double inversion) pairs.</strong> Scan the circuit for any point where a NAND output connects directly into '
    'the &ldquo;both-inputs-tied&rdquo; (NOT-configured) NAND input. '
    r'Two inversions in a row cancel out: \(\overline{\overline{X}} = X\). Mark these pairs.</p>'
    '\n'
    '<p data-narration-id="n16"><strong>Step 3 &mdash; Cancel the back-to-back pairs.</strong> Remove both back-to-back NANDs and connect the wire directly. '
    'This simplifies the circuit and reduces gate count. The resulting circuit is the minimal NAND-only implementation.</p>\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>Worked example: converting AND-OR to NAND-only</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    r'    <p data-narration-id="n17">Original circuit: AND gate (inputs A, B) feeding an OR gate alongside input C. Boolean: \(Q = AB + C\).</p>'
    '\n'
    '    <p data-narration-id="n18">Step 1 &mdash; Replace the AND gate with NAND(A,B) followed by a tied-input NAND on its output. '
    'Replace the OR gate with a NOT-NAND on each of its inputs, then combine those outputs with a third NAND. '
    'Intermediate circuit has 5 NAND gates.</p>\n'
    '    <p data-narration-id="n19">Step 2 &mdash; The output of the tied-input NAND after the AND gate feeds directly into the tied-input NAND '
    'on the OR-equivalent side. These two are back-to-back &mdash; double inversion identified.</p>\n'
    '    <p data-narration-id="n20">Step 3 &mdash; Cancel: remove those two back-to-back NANDs and connect the NAND(A,B) output directly to the input of the final NAND. '
    r'Final circuit uses <strong>3 NAND gates</strong>: NAND(A,B), NOT-NAND(C,C), NAND of those two results. Boolean check: \(\overline{\overline{AB} \cdot \overline{C}} = AB + C\) &mdash; correct by De Morgan.</p>'
    '\n'
    '  </div></div>\n'
    '</div>\n\n'
    '<h2 data-narration-id="n21">Double Inversion and De Morgan&rsquo;s Theorem</h2>\n'
    '<p data-narration-id="n22"><dfn class="term" data-def="The principle that two consecutive NOT operations cancel each other: double inversion of a signal returns the original value.">Double inversion</dfn> '
    'is the key simplification step. Any time a signal passes through two inverters in a row (or two tied-input NANDs), both can be removed. '
    'This is the step that students most commonly miss in the exam &mdash; they draw a correct but bloated NAND circuit with redundant gate pairs still in place.</p>\n'
    r'<p data-narration-id="n23">De Morgan&rsquo;s theorem states \(\overline{A} \cdot \overline{B} = \overline{A + B}\), which rearranges to show that NAND of the complements equals the NOR, and \(\overline{\overline{A} \cdot \overline{B}} = A + B\), confirming the OR equivalent. '
    'You do not need to prove De Morgan in the exam &mdash; apply it to verify your NAND conversion is correct.</p>'
    '\n\n'
    '<h2 data-narration-id="n24">Logic ICs: The CMOS 4000 Series</h2>\n'
    '<p data-narration-id="n25">In practice, logic gates are packaged as '
    '<dfn class="term" data-def="A family of CMOS integrated circuits, numbered 4000 onwards, containing two to four logic gates in a single package.">CMOS 4000 series ICs</dfn>. '
    'Each IC package contains several identical gates sharing a power supply pin (V<sub>DD</sub>) and a ground pin (V<sub>SS</sub>). '
    'The 4011 contains four two-input NAND gates; the 4001 contains four two-input NOR gates. '
    'When using these ICs, unused inputs must be tied to Logic 0 or Logic 1 (not left floating) to prevent unpredictable switching.</p>\n\n'
    '<div class="collapsible">\n'
    '  <button class="collapsible-toggle" aria-expanded="false">\n'
    '    <span>Reading a CMOS 4000 series pin diagram</span>\n'
    '    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
    '  </button>\n'
    '  <div class="collapsible-content"><div class="collapsible-inner">\n'
    '    <p data-narration-id="n26">A 14-pin dual in-line (DIL) package has 7 pins on each side. The notch or dot marks pin 1 (top left). Pins are numbered anticlockwise from pin 1. '
    'For a quad 2-input NAND (4011): pin 14 is V<sub>DD</sub> (supply), pin 7 is V<sub>SS</sub> (ground). '
    'The four gates share these supply pins &mdash; you only need to connect V<sub>DD</sub> and V<sub>SS</sub> once for all four gates.</p>\n'
    '    <p data-narration-id="n27">In exam questions showing a pinout, identify the gate inputs and outputs by their pin numbers. '
    'A question might ask you to state which pins to connect to implement a specific logic function using available gates on the IC. '
    'Always check that you are using a gate that is on the IC &mdash; examiners have penalised students who used the wrong gate type for the IC shown.</p>\n'
    '  </div></div>\n'
    '</div>'
  ),
  "exam_tip_html": (
    '<p data-narration-id="n28">NAND-only conversion is worth 6 marks on the paper and is consistently the weakest-answered question every year. '
    'Use the three-step method every time: (1) replace each gate with its NAND equivalent; (2) mark back-to-back NANDs (double inversions); (3) cancel them. '
    'Drawing a bloated 5-gate answer when the correct answer is 3 gates drops you to a partial mark band. '
    'For logic design questions, write the truth table before attempting the Boolean expression &mdash; students who jump straight to the expression miss rows and get the wrong gate combination.</p>'
  ),
  "conclusion_html": (
    '<h3 data-narration-id="n29">Key Takeaways</h3>\n'
    '<ul>\n'
    '  <li data-narration-id="n30">Logic design follows three steps: write the truth table from the specification, extract the Boolean expression from the rows where Q=1, then select gates. Most expressions can be written in sum-of-products form.</li>\n'
    '  <li data-narration-id="n31">Any standard gate can be replaced with NAND gates: NOT = tied-input NAND; AND = NAND then NOT-NAND; OR = two NOT-NANDs feeding a NAND. After substitution, cancel back-to-back (double-inversion) NAND pairs.</li>\n'
    '  <li data-narration-id="n32">Logic ICs used in this course are CMOS 4000 series. Unused inputs must be tied to a defined logic level &mdash; never left floating. The supply pin V<sub>DD</sub> and ground pin V<sub>SS</sub> are shared by all gates in the package.</li>\n'
    '</ul>'
  ),
  "practice_questions": [
    {
      "text": "Which one of the following is the correct NAND-only equivalent of a NOT gate?\nA) A NAND gate with inputs A and B\nB) A NAND gate with both inputs tied together to signal A\nC) Two NAND gates in series, each with separate inputs\nD) A NAND gate with input A and input B permanently at Logic 0",
      "type": "1 mark — Multiple Choice",
      "marks": "B) A NAND gate with both inputs tied together to signal A [1 mark]"
    },
    {
      "text": "State what is meant by 'double inversion' in a NAND-only circuit and explain why back-to-back NAND pairs can be removed.",
      "type": "2 marks — State / Define",
      "marks": "Double inversion is when a signal passes through two NOT operations (inverters) in succession. [1 mark]\nTwo inversions cancel because NOT(NOT(X)) = X, so the signal is unchanged and the two gates add no function to the circuit. [1 mark]"
    },
    {
      "text": "A logic system has the Boolean expression Q = A AND B OR C (Q = AB + C).\n(a) Complete the truth table for this expression.\n(b) Identify the gates needed to implement this circuit directly.",
      "type": "4 marks — Calculation: Multi-Step",
      "marks": "(a) Correct 8-row truth table with Q = 0, 1, 0, 1, 0, 1, 1, 1 for rows 000 through 111 [2 marks: 1 mark for 5 or more correct rows, 2 marks for all 8 correct]\n(b) One AND gate (inputs A and B) and one OR gate combining the AND output with C [2 marks: 1 per gate correctly identified]"
    },
    {
      "text": "Convert the following circuit to a NAND-only implementation. The circuit consists of an AND gate (inputs A, B) whose output feeds an OR gate alongside input C. Show all steps: NAND equivalents, identification of double inversions, and the simplified circuit.",
      "type": "6 marks — Convert to NAND-Only Implementation",
      "marks": "Step 1 — Replace AND(A,B) with NAND(A,B) followed by tied-input NAND; replace OR with NOT-NANDs on each input then a combining NAND. [2 marks for correct equivalents shown]\nStep 2 — Identifies the tied-input NAND on the AND output is back-to-back with the tied-input NAND on the C-input side of the OR equivalent. [1 mark]\nStep 3 — Cancels the back-to-back pair, resulting in three NAND gates: NAND(A,B), NAND(C,C), NAND of those two outputs. [2 marks for correct simplified circuit]\nBoolean verification or correct gate count stated. [1 mark]"
    },
    {
      "text": "Design a logic sub-system for a greenhouse alarm that outputs Logic 1 when the temperature sensor (T) is Logic 1 OR the humidity sensor (H) is Logic 1, but NOT when both are Logic 1 simultaneously. Write the truth table, Boolean expression, and specify the required gates.",
      "type": "5 marks — Design a Sub-System",
      "marks": "Truth table (4 rows): TH=00 Q=0; TH=01 Q=1; TH=10 Q=1; TH=11 Q=0. [1 mark]\nBoolean expression: Q = T.NOT(H) + NOT(T).H (exclusive OR expression). [1 mark]\nGates required: two NOT gates (one on T, one on H), two AND gates for each product term, one OR gate combining them. [2 marks: 1 per correct gate type identified]\nAlternatively accepts XOR gate with justification. [1 mark]"
    },
    {
      "text": "A student converts a two-gate circuit (AND then OR) to NAND-only but does not cancel the back-to-back NAND pairs. Their final circuit has five NAND gates. A second student correctly cancels the double inversions and produces a three-gate circuit. Both circuits produce the same outputs. Evaluate which design is preferable for use in a real electronic product and explain why, with reference to IC gate count, cost, and any practical wiring considerations.",
      "type": "8 marks — Extended Response: Circuit Analysis and Evaluation",
      "marks": "Mastering: Clearly argues the three-gate design is preferable on multiple grounds. Each additional NAND gate requires IC pins; five gates may require a second IC while three gates fit on one 4011 with a spare gate. Fewer ICs means lower cost, smaller PCB footprint, fewer solder joints, and higher reliability. Notes that unused gates on a CMOS IC must have their inputs tied to a defined level, adding wiring complexity when a second IC is needed. Conclusion explicitly links fewer gates to lower cost and more reliable product.\nSecure: Identifies that fewer gates may fit on one IC versus two, gives a cost or reliability argument, mentions unused inputs needing to be tied. May omit PCB footprint or solder joint detail.\nDeveloping: Correctly states the three-gate design uses fewer components and is cheaper, but explanation of IC count or practical wiring is incomplete.\nEmerging: States the three-gate design is better without technical justification."
    }
  ],
  "knowledge_checks": [
    {
      "type": "mcq",
      "q": "How many NAND gates are needed to build a NAND-only equivalent of a two-input AND gate?",
      "options": ["1", "2", "3", "4"],
      "correct": 1
    },
    {
      "type": "mcq",
      "q": "What should be done with unused inputs on a CMOS 4000 series logic IC?",
      "options": ["Left unconnected (floating)", "Connected to the output of another gate", "Tied to Logic 0 or Logic 1", "Connected together in pairs"],
      "correct": 2
    },
    {
      "type": "fill",
      "q": "When converting to NAND-only, back-to-back NAND pairs can be removed because two consecutive _____ cancel each other out.",
      "options": ["AND operations", "inversions (NOT operations)", "OR operations", "supply connections"],
      "correct": 1
    },
    {
      "type": "fill",
      "q": "The CMOS 4011 IC contains four two-input _____ gates in a single 14-pin package.",
      "options": ["NOR", "OR", "NAND", "AND"],
      "correct": 2
    },
    {
      "type": "match",
      "q": "Match each standard gate to its NAND-only equivalent description:",
      "left": ["NOT gate", "AND gate", "OR gate"],
      "right": ["Two NOT-NANDs on each input, outputs combined by a third NAND", "One NAND with both inputs tied to the same signal", "One NAND followed by a tied-input NAND on its output"],
      "order": [1, 2, 0]
    }
  ],
  "flashcard_questions": [
    {"q": "What are the three steps of the logic design process?", "a": "Write truth table, extract Boolean expression, select gates."},
    {"q": "What is sum-of-products form in Boolean algebra?", "a": "Output written as OR of AND terms, e.g. Q = AB + C."},
    {"q": "How do you build a NOT gate from a single NAND gate?", "a": "Tie both inputs of the NAND together to the same signal A."},
    {"q": "How many NAND gates are needed to make an AND gate?", "a": "Two: one NAND(A,B) followed by a tied-input NAND on its output."},
    {"q": "How many NAND gates are needed to make an OR gate?", "a": "Three: a NOT-NAND on each input, then a third NAND combining them."},
    {"q": "What is double inversion?", "a": "Two consecutive NOT operations on the same signal, which cancel to give the original."},
    {"q": "Why can back-to-back NAND pairs be removed in a NAND-only circuit?", "a": "Because NOT(NOT(X)) = X: the two inversions cancel each other."},
    {"q": "What is the CMOS 4011 IC?", "a": "A 14-pin IC containing four two-input NAND gates."},
    {"q": "What must be done with unused gate inputs on a CMOS 4000 series IC?", "a": "Tied to a defined logic level (Logic 0 or Logic 1) — never left floating."},
    {"q": "Why is a NAND gate described as a universal gate?", "a": "Because any logic function can be built using only NAND gates."},
    {"q": "On a 14-pin CMOS IC, which pins are power supply (V_DD) and ground (V_SS)?", "a": "Pin 14 is V_DD (supply); pin 7 is V_SS (ground)."},
    {"q": "What does De Morgan's theorem say about NOT(A) AND NOT(B)?", "a": "NOT(A) AND NOT(B) = NOT(A OR B): the NAND of complements equals the NOR."}
  ],
  "glossary_terms": [
    {"term": "NAND-only implementation", "definition": "Replacing every standard logic gate in a circuit with an equivalent combination of NAND gates, so the circuit uses only NAND gates throughout."},
    {"term": "sum of products", "definition": "A Boolean expression written as the OR of one or more AND terms, each AND term being a product of input variables or their complements."},
    {"term": "double inversion", "definition": "The principle that two consecutive NOT operations cancel each other: double inversion of a signal returns the original value."},
    {"term": "CMOS 4000 series ICs", "definition": "A family of CMOS integrated circuits, numbered 4000 onwards, containing two to four logic gates in a single package."}
  ],
  "hero_keywords": ["integrated circuit chip logic gates", "CMOS microchip electronics", "digital logic circuit board"],
  "hero_image_caption": "CMOS integrated circuit chip containing logic gates on a circuit board"
}

# ── Write all three ──
for lesson, fname in [
    (L8, "diodes-half-wave-rectification-and-zener-voltage-regulation.json"),
    (L9, "logic-gates-truth-tables-and-boolean-algebra.json"),
    (L10, "designing-logic-systems-and-nand-only-implementations.json"),
]:
    path = os.path.join(OUT_DIR, fname)
    text = json.dumps(lesson, indent=2, ensure_ascii=False)
    # Verify it round-trips
    json.loads(text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Written & verified: {fname} ({len(text)} chars)")

print("All done.")
