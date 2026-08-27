# Widget brief: Transistor: small current controls larger current

Cluster id: `transistor-current-amplification`  |  serves 2 lessons

## The one thing the widget must make concrete

A transistor uses a small base/gate current to actively control a much larger collector/drain current, unlike a simple mechanical on/off switch.

## The lessons it will sit in

### 1. [electronics-eduqas] Transistor and MOSFET Switching Circuits — `/lesson/electronics-eduqas/discovering-electronics/6`
Triage: Students think a transistor simply passes through or blocks current like a mechanical switch, rather than understanding that a *small* base current must actively control a much *larger* collector current, and that this relationship is non-negotiable (the base current must exceed IC/hFE or the transistor won't saturate).

> Switching High Currents from Low-Power Signals A logic gate or comparator output can drive only a few milliamperes &mdash; not nearly enough to light a lamp, spin a motor or click a relay. A transistor or MOSFET acts as a current amplifier and electronic switch, letting a small control signal turn a much larger load current on or off. Examiners report this is poorly understood every year, so this lesson builds the skill in both directions: forward (given a signal, will the device switch?) and backward (given a required load current, what control signal do I need?). The npn Bipolar Transistor as a Switch An npn transistor has three terminals: base (B), collector (C) and emitter (E). In a switching circuit: The load (lamp, relay coil, etc.) is connected between the positive supply and the collector. The emitter connects to 0 V (ground). A base resistor connects the control signal to the ba...

### 2. [engineering-aqa] Programmable Systems: Microcontrollers and Interfacing — `/lesson/engineering-aqa/engineering-systems/6`
Triage: Students think the microcontroller's output pin directly powers the motor/actuator, or that a transistor simply 'turns on' without understanding that a small signal controls a much larger current flow through a separate path.

> What Is a Microcontroller? A microcontroller is a small computer on a single chip. It contains a processor (to execute instructions), memory (to store the program and data) and a set of input and output connections &mdash; all on one integrated circuit. Microcontrollers run a program that reads sensor inputs, makes decisions and drives output devices. They replace large banks of discrete logic gates, making control systems compact, flexible and reprogrammable. Common microcontroller families include the PIC (Peripheral Interface Controller &mdash; widely used in industrial and automotive applications) and development boards such as the BBC micro:bit and Arduino (used in school workshops and rapid prototyping). For the purposes of this specification, the key rule is that a microcontroller is limited to three inputs and three outputs within an engineered system &mdash; this keeps the desig...
