# Widget brief: Voltage divider output direction depends on sensor's position

Cluster id: `voltage-divider-output-direction-depends-on-position`  |  serves 1 lessons

## The one thing the widget must make concrete

Whether output voltage rises or falls as a sensor's quantity increases depends on whether the sensor is the top or bottom resistor in the divider.

## The lessons it will sit in

### 1. [electronics-eduqas] Sensing Circuits and Voltage Dividers — `/lesson/electronics-eduqas/discovering-electronics/5`
Triage: Students believe that putting a sensor in a voltage divider always makes the output voltage rise when the sensor's physical quantity increases (e.g., output always goes up when it gets brighter or hotter), without realizing that the sensor's position—R1 (top) vs R2 (bottom)—completely reverses this relationship.

> From Sensor to Signal A sensor on its own produces a change in resistance, not a change in voltage. To turn a varying resistance into a varying voltage that a comparator or logic gate can read, you use a voltage divider . This is the most common input circuit in electronics and it appears on virtually every exam paper. How a Voltage Divider Works Two resistors, R1 and R2, are placed in series across a supply voltage \(V_{in}\). The output voltage \(V_{out}\) is taken from the junction between them and is given by: $$V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}$$ If R2 is much larger than R1, most of the supply voltage appears across R2, so \(V_{out}\) is high. If R2 is much smaller than R1, most of the voltage is dropped across R1 and \(V_{out}\) is low. Replacing one of the resistors with a sensor (LDR, thermistor, etc.) makes \(V_{out}\) change with the physical quantity being sensed....
