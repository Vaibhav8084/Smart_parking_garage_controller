# Smart Parking Garage Controller | COA Real-Time Logic Simulator

An interactive, browser-based hardware and digital logic simulator designed for **Computer Organization and Architecture (COA)** coursework.

This application provides a real-time hardware simulation of a **3-bit synchronous up/down state register datapath**, hardwired control logic, status condition flags (`FULL`, `EMPTY`), gate actuators, and a **CD4511 BCD-to-7-segment decoder**.

---

## 🌟 Features Included

1. **Physical Parking Facility Simulation (2D Canvas):**
   - 7 marked parking spots (`Bay 01` to `Bay 07`).
   - Animated barrier gate arms that open/close smoothly at $90^\circ$ angles based on logic state.
   - Live animated cars arriving, parking in vacant spots, and driving out through exit gate.
   - Large physical entrance totem pole with a real-time glowing Common-Cathode 7-Segment display and LED message banner.
   - Synthesized Web Audio sound effects (barrier gate motor, sensor ding, alert buzzer, chime) with zero external audio assets.

2. **Virtual Breadboard & Live IC View:**
   - Dual breadboard chassis with authentic tie-point grid holes, $+5\text{V}$ power rails, and $\text{GND}$ rails.
   - Real standard DIP IC chips:
     - `74HC74` (Dual D Flip-Flop, chips U2 and U3 for 3-bit state register $S_2, S_1, S_0$)
     - `74HC08` (Quad 2-Input AND Gate for status flag decoding)
     - `74HC32` (Quad 2-Input OR Gate for gate drivers)
     - `74HC04` (Hex Inverter)
     - `74HC86` (Quad 2-Input XOR Gate for D-flip-flop toggle excitation $D = Q \oplus T$)
     - `CD4511` (BCD to 7-Segment Decoder/Driver)
   - Color-coded virtual wires with live logic levels: Green (5V HIGH) and Slate (0V LOW).
   - **Interactive Live Pin Inspector**: Hover over any IC pin or breadboard node to see its pin number, IC name, internal function, net name, and live voltage level ($5.0\text{V}$ or $0.0\text{V}$).

3. **Digital Logic Schematic & Live Signal Propagation:**
   - Full gate-level datapath with IEEE logic symbols.
   - Live logic state visualization ($1$ vs $0$) flowing through wires and gates.

4. **Finite State Machine (FSM) & Dynamic State Table:**
   - Circular FSM state transition graph with nodes $000_2$ to $111_2$.
   - Live state highlighting showing current node and transition paths.
   - Synchronous state excitation table with the active state row dynamically highlighted in real-time.

5. **Digital Logic Analyzer (Oscilloscope Waveform Capture):**
   - Real-time 8-channel digital logic analyzer:
     - `CH1: IN_SW`, `CH2: OUT_SW`, `CH3: COUNT_CLK`, `CH4: S0 (LSB)`, `CH5: S1`, `CH6: S2 (MSB)`, `CH7: FULL_FLAG`, `CH8: ENTRY_GATE`.
   - Real-time scrolling digital waveform trace with Pause and Clear controls.

6. **Computer Organization & Architecture (COA) Educational Analysis:**
   - Detailed mapping between the parking garage controller and general-purpose microprocessors:
     - Program Counter (PC) & State Accumulator
     - ALU Increment/Decrement Datapath
     - Status Condition Codes (Zero Flag / Overflow Flag)
     - Hardwired Control Matrix vs Microcode
     - Memory-Mapped I/O and Peripheral Decoders

7. **Automated Verification & Test Suite:**
   - One-click runner for all 7 required hardware test cases with automated pass/fail assertions:
     1. System Power-On / Preset Reset
     2. Normal Single Car Entry
     3. Fill to Full Capacity (7 Cars)
     4. Blocked Entry Attempt at Full Capacity
     5. Normal Exit from Full State
     6. Simultaneous Entry and Exit (Net Delta = 0)
     7. Emergency Override Mode

---

## 🚀 How to Run the Website

### Option 1: Double-Click (Zero Installation Required)
Simply open `index.html` in any modern web browser (Chrome, Edge, Firefox, Safari). Everything works immediately with pure HTML5, CSS3, and JavaScript!

### Option 2: Run via Node.js
From the project folder:
```bash
node server.js
```
Then open: [http://localhost:3000](http://localhost:3000)

---

## ⌨️ Keyboard Shortcuts
- <kbd>I</kbd> : Car Enters Garage (`IN_SW`)
- <kbd>O</kbd> : Car Leaves Garage (`OUT_SW`)
- <kbd>R</kbd> : System Preset / Reset (`RST_SW`)
- <kbd>E</kbd> : Toggle Emergency Override (`EMERG_SW`)
