# Widget brief: Sampling is repeated measurement at fixed intervals

Cluster id: `sampling-repeated-measurement`  |  serves 4 lessons

## The one thing the widget must make concrete

Digital sampling involves the ADC repeatedly measuring wave height at fixed intervals; missing intervals loses information, it isn't a single one-off action.

## The lessons it will sit in

### 1. [computer-science] Representing Images & Sound — `/lesson/computer-science/computer-systems/7`
Triage: Students think sampling is a simple one-to-one recording of sound height at points, not realizing that the original wave shape between samples is permanently lost and must be reconstructed by the computer.

> How Computers Store Pictures A computer can only hold data as binary &mdash; long strings of 0s and 1s &mdash; so a photograph must be turned into numbers before it can be saved. The most common way to do this is with a bitmap image, which is simply a grid of tiny coloured squares. Each square is a pixel (short for &lsquo;picture element&rsquo;), the smallest element of a digital image. Every pixel is given a binary code that stands for its colour, so the whole picture becomes a long list of colour codes that the computer reads row by row to rebuild the image. Key Fact Colour depth is the number of bits used to store the colour of each pixel. With a colour depth of \(n\) bits, an image can use \(2^n\) different colours &mdash; every extra bit doubles the number of colours available. Colour Depth The colour depth of an image is the number of bits used to represent the colour of a single p...

### 2. [computer-science-eduqas] Sound: Sampling and File Size — `/lesson/computer-science-eduqas/data-representation-storage/5`
Triage: Students think sampling is a single action that happens once, rather than understanding that the ADC repeatedly measures the wave height at fixed intervals, and that missing those intervals means losing information about what the wave did in between.

> From Sound Waves to Digital Data Sound in the real world is an analogue signal &mdash; a continuous wave of air pressure that varies smoothly over time. Computers can only store discrete binary values, so to record sound digitally, the continuous wave must be converted into a series of snapshots. This process is called sampling . An analogue-to-digital converter (ADC) is the hardware component that performs sampling. It reads the amplitude (height) of the sound wave at a fixed rate and stores each reading as a binary number. On playback, a digital-to-analogue converter (DAC) reconstructs the wave from those stored numbers. The reconstructed wave is an approximation &mdash; how close it is to the original depends on how often measurements are taken and how precisely each one is stored. Sample Rate (Sampling Frequency) The sample rate (or sampling frequency) is the number of samples taken ...

### 3. [computer-science-edexcel] Characters, Images and Sound — `/lesson/computer-science-edexcel/data/3`
Triage: Students think sampling is a single snapshot of sound, rather than understanding that samples are discrete points that must be frequent enough to reconstruct the wave shape—they don't grasp how gaps between samples create aliasing or how sample rate directly determines what frequencies can be captured.

> How Computers Store Text A computer stores everything as binary &mdash; including the letters you type. To do this, every character must be assigned a unique number, which is then stored as its binary equivalent. A character set is the agreed list that maps each character to its code. Without a shared standard, a file created on one system would display differently on another. 7-Bit ASCII ASCII (American Standard Code for Information Interchange) uses 7 bits per character, allowing \(2^7 = 128\) unique codes (0 to 127). These 128 characters cover upper-case letters, lower-case letters, the digit characters 0&ndash;9, punctuation marks and control characters such as &ldquo;new line&rdquo;. The key principle is that codes are sequential within each group . Upper-case A&nbsp;=&nbsp;65, B&nbsp;=&nbsp;66, up to Z&nbsp;=&nbsp;90. Lower-case a&nbsp;=&nbsp;97, b&nbsp;=&nbsp;98, up to z&nbsp;=&nb...

### 4. [computer-science-aqa] Representing Images and Sound — `/lesson/computer-science-aqa/data-representation/3`
Triage: Students think sampling captures the entire shape of a sound wave, when it actually captures only isolated points that are then reconnected—missing peaks and valleys between samples.
