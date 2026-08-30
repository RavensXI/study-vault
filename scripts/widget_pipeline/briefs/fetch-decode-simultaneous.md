# Widget brief: Decode is simultaneous interpretation, not a separate visible step

Cluster id: `fetch-decode-simultaneous`  |  serves 4 lessons

## The one thing the widget must make concrete

In the fetch-execute cycle, decoding is a simultaneous interpretation of the fetched instruction rather than a separate sequential step in time.

## The lessons it will sit in

### 1. [computer-science-aqa] CPU Architecture and the Fetch-Execute Cycle — `/lesson/computer-science-aqa/computer-systems/2`
Triage: Students think the fetch-execute cycle happens sequentially in time with visible steps, rather than understanding that decode is a *simultaneous interpretation* of the fetched instruction, and that all three stages overlap in a pipelined CPU—or at minimum, that decode is not a separate physical journey but a logical parsing.

> What Is the CPU? The CPU is the component that carries out every instruction a program contains. It processes data, performs calculations, makes comparisons and controls the flow of information between all other parts of the system. Without the CPU, no program can run. Most CPUs follow the design principles of Von Neumann architecture , named after the mathematician John von Neumann whose work in the 1940s described storing both instructions and data in the same memory. This is the foundation of the vast majority of computers made since then, from desktop PCs to smartphones. Key Fact The main components inside the CPU are: the ALU (performs arithmetic and logic operations), the control unit (directs data flow and manages the fetch-execute cycle), the clock (generates timing pulses), registers (small, fast storage locations inside the CPU) and the bus (a collection of wires for transmitti...

### 2. [computer-science-eduqas] The CPU and Von Neumann Architecture — `/lesson/computer-science-eduqas/hardware-and-systems/1`
Triage: Students think the fetch-decode-execute cycle happens as a linear sequence they can fully visualize in their head, when in reality multiple registers are being used simultaneously in parallel, with the PC already moving ahead while the CIR is still executing.

> What Is the CPU? The CPU is the brain of any computer system. It carries out the instructions that make up every program you run &mdash; from loading a webpage to running a game. Without the CPU, no processing can happen. Every calculation, decision and data movement passes through this single chip. The design that almost every modern CPU is built on was described by mathematician John von Neumann in 1945. Von Neumann architecture states that a program&rsquo;s instructions and its data should be stored in the same memory, and that the CPU should fetch each instruction in sequence, decode it, and then execute it. This idea &mdash; so straightforward it seems obvious now &mdash; was revolutionary at the time and remains the foundation of almost every computer built today. Key Fact A CPU contains two main sub-units: the Control Unit (CU) , which manages the fetch-decode-execute cycle, and t...

### 3. [computer-science-eduqas] Fetch-Decode-Execute and CPU Performance — `/lesson/computer-science-eduqas/hardware-and-systems/2`
Triage: Students believe the FDE cycle is a simple linear sequence and don't understand that multiple registers hold different parts of the same instruction simultaneously, or that the PC increments *during* fetch before the instruction is even decoded.

> The Fetch-Decode-Execute Cycle Every program your computer runs &mdash; from a simple calculator to a complex video game &mdash; is ultimately a list of instructions stored in memory. The Fetch-Decode-Execute (FDE) cycle is the process a CPU uses to work through those instructions, one at a time, billions of times per second. Understanding the cycle also means understanding exactly which register does what during each stage. Stage 1 &mdash; Fetch The cycle begins with the CPU needing to retrieve the next instruction from main memory (RAM). Here is the sequence of register operations during the fetch stage: The Program Counter (PC) holds the address of the next instruction. This address is copied into the Memory Address Register (MAR) . The PC is immediately incremented so it points to the address of the instruction after that &mdash; ready for the following cycle. The CPU sends the addre...

### 4. [computer-science] CPU Architecture & the Fetch-Execute Cycle — `/lesson/computer-science/computer-systems/1`
Triage: Students think the fetch-execute cycle is a linear sequence they can understand by reading steps in order, without grasping that the Program Counter, MAR, MDR, and Accumulator are simultaneously holding different things and changing at precise moments in a loop.
