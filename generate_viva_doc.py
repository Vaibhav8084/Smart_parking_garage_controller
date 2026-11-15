# Script to generate the comprehensive Word Document (.docx) for the COA Smart Parking Garage Project
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styling constants
    COLOR_PRIMARY = RGBColor(14, 116, 144)    # Deep Cyan / Teal #0E7490
    COLOR_SECONDARY = RGBColor(30, 41, 59)   # Slate Navy #1E293B
    COLOR_TEXT = RGBColor(51, 65, 85)        # Charcoal Text #334155
    COLOR_MUTED = RGBColor(100, 116, 139)    # Muted Gray #64748B
    HEX_PRIMARY = "0E7490"
    HEX_LIGHT_BG = "F8FAFC"
    HEX_CALLOUT_BG = "F0FDF4"
    HEX_CALLOUT_BORDER = "16A34A"
    HEX_WARN_BG = "FEF2F2"
    HEX_WARN_BORDER = "DC2626"
    HEX_TABLE_HEADER = "1E293B"

    # Set Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_TEXT
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Helper: Set Cell Shading
    def set_cell_background(cell, hex_color):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    # Helper: Set Table Borders
    def set_table_borders(table, color="CBD5E1"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # Helper: Callout Box
    def add_callout(text, title=None, is_warning=False):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.9)

        bg_color = HEX_WARN_BG if is_warning else HEX_CALLOUT_BG
        border_color = HEX_WARN_BORDER if is_warning else HEX_CALLOUT_BORDER
        set_cell_background(cell, bg_color)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.1)
        p.paragraph_format.right_indent = Inches(0.1)

        if title:
            run_title = p.add_run(f"📌 {title}\n")
            run_title.bold = True
            run_title.font.size = Pt(11)
            run_title.font.color.rgb = RGBColor(185, 28, 28) if is_warning else RGBColor(21, 128, 61)

        run_text = p.add_run(text)
        run_text.font.size = Pt(10)
        run_text.font.italic = False
        run_text.font.color.rgb = COLOR_SECONDARY
        doc.add_paragraph() # Spacing

    # Helper: Add Heading 1
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_PRIMARY
        return h

    # Helper: Add Heading 2
    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_SECONDARY
        return h

    # Helper: Add Heading 3
    def add_h3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_PRIMARY
        return h

    # ---------------------------------------------------------
    # COVER / HEADER TITLE
    # ---------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(2)
    run_main_title = title_p.add_run("Smart Parking Garage Controller")
    run_main_title.bold = True
    run_main_title.font.size = Pt(24)
    run_main_title.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Digital Logic Design, Breadboard Implementation, and COA Lab Viva Defense Guide\n"
                           "Course: Computer Organization and Architecture (COA) | Academic Project")
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = COLOR_MUTED

    # Meta bar
    meta_table = doc.add_table(rows=1, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    for i, w in enumerate([Inches(2.3), Inches(2.3), Inches(2.3)]):
        meta_table.rows[0].cells[i].width = w
        set_cell_background(meta_table.rows[0].cells[i], HEX_LIGHT_BG)
    set_table_borders(meta_table)

    meta_table.rows[0].cells[0].paragraphs[0].add_run("Author: Vaibhav Sharma\nReg No / ID: 8084").font.size = Pt(9.5)
    meta_table.rows[0].cells[1].paragraphs[0].add_run("Target Simulator: Tinkercad\nPhysical Scale: 7/8 Spaces").font.size = Pt(9.5)
    meta_table.rows[0].cells[2].paragraphs[0].add_run("Repository & Live Demo:\nGitHub & Vercel Deployed").font.size = Pt(9.5)
    doc.add_paragraph()

    # ---------------------------------------------------------
    # SECTION 1: WHAT HAVE I DONE IN THIS PROJECT?
    # ---------------------------------------------------------
    add_h1("1. Project Executive Summary: What Have I Done?")
    
    p = doc.add_paragraph()
    p.add_run("In this project, I have designed, engineered, simulated, and deployed a complete ")
    p.add_run("Smart Parking Garage Controller").bold = True
    p.add_run(" as a specialized hardware application of ")
    p.add_run("Computer Organization and Architecture (COA)").bold = True
    p.add_run(". Rather than writing high-level software code (such as a Python or C program running on an operating system), this system is implemented entirely at the ")
    p.add_run("digital logic gate and register transfer level").bold = True
    p.add_run(", using discrete 74HC-series Integrated Circuits (ICs), D-type flip-flops, steering logic gates, and a BCD-to-7-segment decoder driver.")

    p2 = doc.add_paragraph()
    p2.add_run("Key Capabilities Engineered into the System:\n").bold = True
    features = [
        ("3-Bit Synchronous Up/Down Datapath: ", "Maintains real-time occupancy and available spaces (0 to 7 spaces). The register updates synchronously on positive clock transitions generated by entry and exit sensor pulses."),
        ("Automated Entry & Exit Barrier Gate Control: ", "Directs hardware barrier servos/LEDs. The entry gate automatically unlocks/opens when an entering car arrives AND the garage is not full; it forcefully stays locked (RED) when zero spaces remain."),
        ("Condition Status Flags (FULL & EMPTY Detectors): ", "Hardware logic gates continuously monitor the 3-bit state bus. When state = 000_2, the FULL condition code asserts (analogous to the CPU Zero Flag). When state = 111_2, the EMPTY flag asserts."),
        ("Hazard & Simultaneous Event Filtration: ", "If two vehicles trigger both entry and exit sensors at the exact same instant, the combinational control matrix suppresses the count clock (net count change = 0) while permitting both gate barrier actuators to open safely."),
        ("High-Priority Emergency Evacuation Override: ", "A master toggle switch that immediately bypasses normal counter limits and boundary inhibits, forcing all entry and exit gates continuously open for rapid evacuation."),
        ("Asynchronous Hardware Preset / Reset: ", "An active-low reset line connected directly to the asynchronous PRESET pins of the flip-flops, immediately re-initializing the garage to full capacity (111_2 = 7 available spots) regardless of clock state."),
        ("Real-Time BCD-to-7-Segment Display Subsystem: ", "Uses a CD4511 decoder IC driving a physical Common-Cathode 7-segment display, dynamically showing available bays from '7' down to '0' without requiring microprocessors.")
    ]
    for bold_prefix, text in features:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        bp.add_run(bold_prefix).bold = True
        bp.add_run(text)

    add_callout(
        "Why 7 spaces instead of 8? A 3-bit binary register naturally holds 2^3 = 8 discrete states (000_2 to 111_2). "
        "By setting State 000_2 = 'FULL' (0 available spaces) and State 111_2 = 'EMPTY' (7 available spaces), the single 7-segment display "
        "directly reflects available parking spaces from 7 down to 0 without requiring complex arithmetic subtractor units or multi-digit BCD logic. "
        "This minimizes breadboard IC footprint while demonstrating every fundamental COA concept.",
        "Engineering Design Choice: Scale & Simplification"
    )

    # ---------------------------------------------------------
    # SECTION 2: CORE CONCEPTS & THEORETICAL FOUNDATIONS
    # ---------------------------------------------------------
    add_h1("2. Core Concepts & Theoretical Foundations")

    add_h2("2.1 Number Systems, Binary Codes & Display Formats")
    p = doc.add_paragraph()
    p.add_run("At the foundation of this project is the representation of numerical quantities across different digital domains:")
    
    num_concepts = [
        ("Binary Positional Representation: ", "The counter register holds the state as a 3-bit unsigned binary vector: S = (S2, S1, S0), where Decimal Value = (S2 * 2^2) + (S1 * 2^1) + (S0 * 2^0) = 4*S2 + 2*S1 + S0."),
        ("Binary Coded Decimal (BCD): ", "The CD4511 decoder requires BCD inputs (A, B, C, D). For decimal digits 0 through 7, standard 3-bit binary is identical to BCD (0000_2 to 0111_2). Input D (MSB, weight 8) is hardwired to Ground (0V), ensuring the decoder never enters undefined hexadecimal states (8 to 15)."),
        ("1's Complement Relationship to Occupancy: ", "An elegant mathematical property: if S represents Available Spaces (7 down to 0), the number of Occupied Spaces is given by (7 - S). In 3-bit binary arithmetic, subtracting any number from 7 is equivalent to taking its bitwise NOT: Occupied = NOT(S2), NOT(S1), NOT(S0). Thus, occupancy data is available directly from the complementary Q_bar pins of the flip-flops!")
    ]
    for b_pre, b_text in num_concepts:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        bp.add_run(b_pre).bold = True
        bp.add_run(b_text)

    add_h2("2.2 Sequential Logic: Synchronous vs. Asynchronous (Ripple) Architecture")
    p = doc.add_paragraph()
    p.add_run("A common question in COA viva examinations is: ")
    p.add_run("'Why did you use a Synchronous counter rather than an Asynchronous (Ripple) counter?'").italic = True
    p.add_run("\nIn a ripple counter (such as the 74HC93), each flip-flop is clocked by the output of the preceding stage. This accumulates propagation delays (t_pd), creating transient false states or ")
    p.add_run("glitches (race hazards)").bold = True
    p.add_run(" on the output lines during transitions (e.g., from 011_2 to 100_2, the output might momentarily flicker through 010_2 or 000_2). In a parking garage controller, momentary false 000_2 glitches would erroneously trigger the FULL alarm and lock the gate!\n"
              "To prevent this, our design uses a ")
    p.add_run("Synchronous Counter").bold = True
    p.add_run(": all flip-flops share the exact same clock pulse line (COUNT_CLK). Next-state excitation equations are computed in parallel through combinational gates, guaranteeing that all bits switch simultaneously without intermediate transient glitches.")

    add_h2("2.3 D-Flip-Flop Toggle Excitation & Derivations")
    p = doc.add_paragraph()
    p.add_run("The 74HC74 IC contains edge-triggered D flip-flops. Unlike T or JK flip-flops that toggle natively, a D flip-flop transfers the voltage at input D to output Q on the rising clock edge (Q_next = D). To produce toggle behavior (T), we apply the Boolean relationship: ")
    p.add_run("D = Q XOR T\n").bold = True
    p.add_run("For our 3-bit Up/Down counter, let DIR be the direction signal (DIR = 1 for UP/Exit, DIR = 0 for DOWN/Entry):")

    exc_table = doc.add_table(rows=4, cols=4)
    exc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate([Inches(1.2), Inches(1.8), Inches(1.8), Inches(2.1)]):
        exc_table.rows[0].cells[i].width = w
    set_table_borders(exc_table)

    headers = ["Bit Stage", "Toggle Condition (T)", "D-Input Excitation Formula", "Hardware Implementation"]
    for i, h in enumerate(headers):
        cell = exc_table.rows[0].cells[i]
        set_cell_background(cell, HEX_TABLE_HEADER)
        p_h = cell.paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    data = [
        ("Bit 0 (LSB, S0)", "T0 = 1 (Always toggles)", "D0 = Q0 XOR 1 = NOT(Q0)", "Feedback Q0_bar directly to D0 pin"),
        ("Bit 1 (S1)", "T1 = (UP & Q0) + (DOWN & ~Q0)", "D1 = Q1 XOR T1", "XNOR(DIR, Q0) into XOR gate (74HC86)"),
        ("Bit 2 (MSB, S2)", "T2 = (UP & Q1 & Q0) + (DOWN & ~Q1 & ~Q0)", "D2 = Q2 XOR T2", "AND-OR steering into XOR gate (74HC86)")
    ]
    for row_idx, row_data in enumerate(data, start=1):
        bg = HEX_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            cell = exc_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            p_c = cell.paragraphs[0]
            r_c = p_c.add_run(text)
            r_c.font.size = Pt(9)

    doc.add_paragraph()

    # ---------------------------------------------------------
    # SECTION 3: BREADBOARD & CIRCUIT ANALYSIS
    # ---------------------------------------------------------
    add_h1("3. Hardware Component Analysis & Breadboard Circuit Architecture")

    p = doc.add_paragraph()
    p.add_run("The complete virtual breadboard design is implemented across two standard full-size breadboards powered by a regulated 5.0 V DC power rail. Every integrated circuit, switch, and indicator is selected from the verified standard 74HC CMOS and 4000-series family.")

    add_h2("3.1 Integrated Circuit (IC) Bill of Materials & Function Table")

    bom_table = doc.add_table(rows=8, cols=5)
    bom_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate([Inches(0.8), Inches(1.2), Inches(1.5), Inches(1.8), Inches(1.6)]):
        bom_table.rows[0].cells[i].width = w
    set_table_borders(bom_table)

    bom_headers = ["Tag", "IC Number", "Generic Description", "Function in Controller", "Key Pins Used"]
    for i, h in enumerate(bom_headers):
        cell = bom_table.rows[0].cells[i]
        set_cell_background(cell, HEX_TABLE_HEADER)
        p_h = cell.paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    bom_data = [
        ("U1", "CD4511", "BCD to 7-Segment Decoder/Driver", "Decodes binary states S0..S2 into 7-segment outputs (a..g)", "Inputs A,B,C; LT, BL, LE; Segs a-g"),
        ("U2", "74HC74", "Dual D-Type Flip-Flop with Set/Reset", "Stores Bit 0 (LSB, S0) and Bit 1 (S1) of state register", "1CLK, 1D, 1Q, 1Q_bar; 2CLK, 2D, 2Q"),
        ("U3", "74HC74", "Dual D-Type Flip-Flop with Set/Reset", "Stores Bit 2 (MSB, S2) of state register", "1CLK, 1D, 1Q, 1Q_bar (FF2)"),
        ("U4", "74HC08", "Quad 2-Input AND Gate", "Decodes FULL flag (~S2*~S1*~S0), EMPTY flag, and sensor gating", "Gates 1 to 4 (Pins 1..13)"),
        ("U5", "74HC32", "Quad 2-Input OR Gate", "Combines gate driver signals and emergency override paths", "Gates 1 to 3 (Pins 1..10)"),
        ("U6", "74HC04", "Hex Inverter (NOT Gates)", "Inverts status flags and sensor lines; active-low preset generation", "Inverters 1 to 5 (Pins 1..11)"),
        ("U7", "74HC86", "Quad 2-Input XOR Gate", "Computes next-state D inputs for flip-flops (D = Q XOR T)", "Gates 1 to 3 (Pins 1..10)")
    ]

    for row_idx, row_data in enumerate(bom_data, start=1):
        bg = HEX_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            cell = bom_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            p_c = cell.paragraphs[0]
            r_c = p_c.add_run(text)
            r_c.font.size = Pt(8.5)

    doc.add_paragraph()

    add_h2("3.2 Critical CD4511 Pin Configuration (High-Frequency Viva Topic)")
    p = doc.add_paragraph()
    p.add_run("Professors routinely examine students on the auxiliary control pins of the CD4511 decoder. Below is the exact electrical justification for each pin's wiring in this project:")

    cd_pins = [
        ("Pin 16 (VDD) & Pin 8 (VSS): ", "Power supply pins. VDD is tied to +5.0 V DC; VSS is tied to Ground (0 V)."),
        ("Pin 3 (~LT - Lamp Test): ", "Active-low input. In normal operation, it MUST be tied to +5.0 V (HIGH). If grounded (LOW), all segments (a-g) illuminate simultaneously displaying '8' regardless of BCD data (used strictly for testing burnt-out LEDs)."),
        ("Pin 4 (~BL - Blanking Input): ", "Active-low input. In normal operation, it MUST be tied to +5.0 V (HIGH). If grounded (LOW), the display turns completely blank/OFF (useful for power saving or blinking displays)."),
        ("Pin 5 (LE / ~STROBE - Latch Enable): ", "Controls internal data latches. In our circuit, Pin 5 is tied directly to Ground (LOW). In this transparent mode, any change on the input lines (A, B, C) immediately propagates to the 7-segment display without requiring a strobe pulse."),
        ("Pin 6 (Input D - MSB): ", "Since our garage capacity is 7 spaces (binary 000_2 to 111_2), input D (which represents numerical weight 8) is tied permanently to Ground (0 V). This restricts valid inputs to 0–7."),
        ("Pins 7, 1, 2 (Inputs A, B, C): ", "Connected directly to the counter state bus: Pin 7 (A, weight 1) <- S0 (LSB); Pin 1 (B, weight 2) <- S1; Pin 2 (C, weight 4) <- S2 (MSB)."),
        ("Pins 9-15 (Outputs a through g): ", "Each output drives the corresponding segment of the Common-Cathode display through a 330 Ohm current-limiting resistor to limit forward current to safe levels (~10-15 mA per segment).")
    ]
    for b_pre, b_text in cd_pins:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2.5)
        bp.add_run(b_pre).bold = True
        bp.add_run(b_text)

    add_h2("3.3 Input Switches & Pull-Down Resistor Network")
    p = doc.add_paragraph()
    p.add_run("Tactile pushbuttons (SW1 Entry, SW2 Exit, SW3 Reset) are connected between the +5V rail and the logic gate inputs. A ")
    p.add_run("10 kOhm pull-down resistor").bold = True
    p.add_run(" connects each input node to Ground (0V).\n"
              "Why is this required? In CMOS technology (74HC family), an unpressed switch without a pull-down resistor creates a ")
    p.add_run("floating (high-impedance / Hi-Z) input").bold = True
    p.add_run(". Floating CMOS gate inputs act like tiny antennas, picking up stray electromagnetic interference and oscillating wildly between 0 and 1, causing erroneous triggers and excessive power dissipation. The 10 kOhm resistor guarantees a solid logic '0' when the button is open, and pulls cleanly to '1' (5V) when pressed.")

    # ---------------------------------------------------------
    # SECTION 4: COMPUTER ORGANIZATION & ARCHITECTURE MAPPING
    # ---------------------------------------------------------
    add_h1("4. Computer Organization & Architecture (COA) Architectural Mapping")

    p = doc.add_paragraph()
    p.add_run("The most important objective of this course project is demonstrating how elementary digital circuits form the building blocks of general-purpose microprocessors. This parking controller is a physical, working model of a ")
    p.add_run("Central Processing Unit (CPU) Datapath and Hardwired Control Unit").bold = True
    p.add_run(".")

    coa_table = doc.add_table(rows=6, cols=3)
    coa_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate([Inches(1.8), Inches(2.5), Inches(2.6)]):
        coa_table.rows[0].cells[i].width = w
    set_table_borders(coa_table)

    coa_headers = ["COA Subsystem", "General-Purpose CPU Counterpart", "Implementation in Parking Controller"]
    for i, h in enumerate(coa_headers):
        cell = coa_table.rows[0].cells[i]
        set_cell_background(cell, HEX_TABLE_HEADER)
        p_h = cell.paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    coa_data = [
        ("Architectural State Register", "Program Counter (PC) or Accumulator (ACC) holding execution address / state.", "3-bit flip-flop cluster (S2, S1, S0) storing system status across clock cycles."),
        ("ALU Datapath & Micro-Operations", "ALU micro-operations: INC (increment) and DEC (decrement) instructions.", "XOR excitation network computing next-state vector: S <- S - 1 or S <- S + 1."),
        ("Condition Codes & Status Register", "EFLAGS register: Zero Flag (Z-flag = 1 when result is 0), Overflow/Underflow flags.", "FULL detector gate (asserts 1 when S=000_2); EMPTY detector gate (asserts 1 when S=111_2)."),
        ("Hardwired Control Unit", "Combinational decoder generating control words and enabling clock pulses.", "74HC08 AND and 74HC32 OR gates decoding sensors, flags, and asserting gate enables."),
        ("Internal Bus & Memory-Mapped I/O", "Data bus distributing operand words from register to peripheral decoders.", "3-bit parallel bus (S2, S1, S0) routing register contents to CD4511 display controller.")
    ]

    for row_idx, row_data in enumerate(coa_data, start=1):
        bg = HEX_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            cell = coa_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            p_c = cell.paragraphs[0]
            r_c = p_c.add_run(text)
            r_c.font.size = Pt(8.5)

    doc.add_paragraph()

    add_callout(
        "RTL (Register Transfer Language) Execution Sequence for Vehicle Arrival:\n"
        "1. Fetch/Decode Sensor: IN_SW = 1, Check Status Flag: FULL\n"
        "2. If FULL == 0: Assert ENTRY_GATE_OPEN <- 1; Generate COUNT_CLK Pulse; S <- S - 1\n"
        "3. If FULL == 1: Inhibit COUNT_CLK; ENTRY_GATE_OPEN <- 0; Assert FULL_ALERT_LED <- 1\n"
        "This is identical to a microprocessor executing: CMP S, 0; JZ FULL_HANDLER; DEC S; MOV [PORT_GATE], 1",
        "Instruction Cycle & RTL Equivalence"
    )

    # ---------------------------------------------------------
    # SECTION 5: SOLUTIONS TO PROFESSOR'S SYLLABUS QUESTIONS
    # ---------------------------------------------------------
    add_h1("5. Solutions to Professor's Open-Ended Questions (from Syllabus Slides)")

    p = doc.add_paragraph()
    p.add_run("The following solutions address the specific questions extracted from the professor's unit lecture slides, demonstrating how the theoretical principles are embodied directly within this Smart Parking Garage Controller project.")

    # --- UNIT 1 QUESTIONS ---
    add_h2("Unit 1: Number Systems, Codes & Logic Gate Transformations")

    q1 = ("Q1. A digital system receives input data in binary, but the display must show the result in decimal/hexadecimal. "
          "How would you convert the data and verify the correctness of the result?")
    a1 = ("In this project, the internal register holds data as a 3-bit unsigned binary vector (S2, S1, S0). To display this as a human-readable decimal digit, "
          "we route the state bus into a BCD-to-7-segment decoder (CD4511). "
          "The decoder uses an internal combinational logic matrix that translates each binary combination (000_2 to 111_2) into active-high segment drive signals (a through g). "
          "To verify correctness, we establish a comprehensive truth table mapping each state (0 to 7) to expected segment outputs, and inspect voltage levels across pins 9–15. "
          "For example, when S = 011_2 (3), segments a, b, c, d, g must measure 5V (HIGH) while e, f measure 0V (LOW).")
    add_callout(f"Question: {q1}\n\nModel Viva Answer: {a1}", "Unit 1 - Question 1 (Directly Applicable)")

    q4 = ("Q4. A digital counter produces errors when multiple bits change simultaneously. "
          "How could Gray code or synchronous clocking help reduce this problem?")
    a4 = ("When a counter transitions across binary boundaries (such as 011_2 to 100_2), multiple flip-flop outputs switch states at once. In asynchronous (ripple) counters, "
          "varying propagation delays cause bits to change at slightly different nanosecond intervals, generating transient intermediate states (e.g., 011 -> 010 -> 000 -> 100). "
          "These intermediate glitches can prematurely trigger combinational decoders. "
          "We solve this in two ways: (1) Using a Synchronous Counter architecture where all flip-flops trigger off a single global clock pulse (COUNT_CLK), ensuring all outputs switch simultaneously; "
          "and (2) In asynchronous shaft-encoders or mechanical car sensors, Gray code is used because exactly one bit changes between successive states, eliminating race conditions entirely.")
    add_callout(f"Question: {q4}\n\nModel Viva Answer: {a4}", "Unit 1 - Question 4 (Directly Applicable)")

    q6 = ("Q6. A designer wants to implement a logic function using only NAND gates. "
          "How would you transform an existing AND-OR logic circuit into a NAND-only implementation?")
    a6 = ("NAND is a Universal Gate capable of realizing all three basic logic primitives (NOT, AND, OR). To convert our gate control expression: "
          "ENTRY_OPEN = EMERG + (IN & ~FULL), we apply De Morgan's double inversion theorem: "
          "1. Start with the Sum-of-Products (SOP) form: Y = A + B, where A = EMERG and B = (IN & ~FULL).\n"
          "2. Apply double negation without changing functionality: Y = NOT(NOT(A + B)).\n"
          "3. Apply De Morgan's Law to the inner negation: NOT(A + B) = NOT(A) * NOT(B).\n"
          "4. Therefore: Y = NOT( NOT(A) * NOT(B) ) = NAND( NOT(EMERG), NOT(IN & ~FULL) ).\n"
          "In hardware, this replaces the AND-OR network with an all-NAND structure, standardizing IC inventory and reducing manufacturing propagation delay.")
    add_callout(f"Question: {q6}\n\nModel Viva Answer: {a6}", "Unit 1 - Question 6 (Directly Applicable)")

    q7 = ("Q7. A digital circuit gives an incorrect output for a particular combination of inputs. "
          "How would you use truth tables and Boolean logic gates to identify the fault?")
    a7 = ("We use a systematic fault-isolation methodology known in computer architecture as Logic Probing / Stuck-At Fault Analysis: "
          "1. Generate the expected Truth Table for all 2^n input combinations.\n"
          "2. Isolate the failing test vector (e.g., when inputs are IN=1, OUT=0, S=000_2, the expected output is ENTRY_OPEN=0, but the gate reads 1).\n"
          "3. Backtrace through the circuit schematic from the primary output back to the primary inputs using a digital voltmeter or logic probe.\n"
          "4. Measure intermediate gate pins: probe the FULL detector output (U4 Pin 6). If it reads 0V when S2=S1=S0=0V, the fault is isolated to the AND detector (stuck-at-0 fault on inverter or input pin), immediately identifying defective wiring or IC failure.")
    add_callout(f"Question: {q7}\n\nModel Viva Answer: {a7}", "Unit 1 - Question 7 (Directly Applicable)")

    # --- UNIT 2 QUESTIONS ---
    add_h2("Unit 2: Computer Architectures & Functional Units")

    q2_1 = ("Q1. A computer must execute a program that reads data from memory, processes it, and stores the result. "
            "How would the functional units of the computer cooperate to complete this task?")
    a2_1 = ("The functional units cooperate through a synchronized instruction cycle: "
            "1. Control Unit: Emits memory address on the Address Bus and asserts Read control signal. "
            "2. Memory Unit: Places operand onto the Data Bus. "
            "3. ALU: Reads operand into temporary registers, performs the arithmetic/logical operation. "
            "4. Control Unit: Generates clock strobe to latch the ALU result into an Accumulator or general-purpose register. "
            "In our project, the Sensors act as I/O input ports, the Combinational Matrix acts as the Hardwired Control Unit, the D Flip-Flops act as the internal Register, and the CD4511 acts as the I/O Display Controller.")
    add_callout(f"Question: {q2_1}\n\nModel Viva Answer: {a2_1}", "Unit 2 - Question 1 (Directly Applicable)")

    q2_2 = ("Q2. Two processors use different bus structures to transfer data between the CPU, memory, and I/O devices. "
            "How would you compare their performance and identify the more suitable architecture?")
    a2_2 = ("In a Single-Bus Organization, all functional units (CPU, memory, I/O) share a single common data path. It is cost-effective and compact, but creates a performance bottleneck (bus contention) because only one transfer can occur per clock cycle. "
            "In a Multiple-Bus Organization (e.g., separate processor-memory bus and peripheral I/O bus), concurrent transfers can execute simultaneously (e.g., ALU fetching next instruction while I/O updates display). "
            "In our controller, we use a dedicated internal state bus (S2..S0) decoupled from the sensor input lines, ensuring instantaneous display updates without bus arbitration overhead.")
    add_callout(f"Question: {q2_2}\n\nModel Viva Answer: {a2_2}", "Unit 2 - Question 2 (Directly Applicable)")

    # --- UNIT 3 QUESTIONS ---
    add_h2("Unit 3: ALU Design & Arithmetic Operations")

    q3_1 = ("Q1. A digital circuit contains a complex Boolean expression that is difficult to implement. "
            "How would you apply De Morgan's theorems to simplify the expression and redesign the circuit?")
    a3_1 = ("De Morgan's theorems state: (1) NOT(A * B) = NOT(A) + NOT(B), and (2) NOT(A + B) = NOT(A) * NOT(B). "
            "In our controller, the FULL detector condition requires detecting when S2=0, S1=0, and S0=0. "
            "A naive implementation requires three inverters followed by a 3-input AND gate: FULL = ~S2 * ~S1 * ~S0. "
            "Applying De Morgan's second theorem: ~S2 * ~S1 * ~S0 = NOT(S2 + S1 + S0). "
            "This simplifies the hardware to a single 3-input NOR gate directly connected to the Q outputs, eliminating three separate inverters and reducing chip count and propagation delay!")
    add_callout(f"Question: {q3_1}\n\nModel Viva Answer: {a3_1}", "Unit 3 - Question 1 (Directly Applicable)")

    # --- UNIT 4 QUESTIONS ---
    add_h2("Unit 4: Control Unit Design & Hazard Analysis")

    q4_6 = ("Q6. A control unit must generate control signals for a complex set of instructions. "
            "How would you compare hardwired and microprogrammed control units when selecting a design?")
    a4_6 = ("1. Hardwired Control Unit: Implemented using fixed combinational logic gates (AND, OR, decoders, flip-flops). "
            "Advantages: Maximum execution speed (single gate-delay latency), highly optimized for RISC architectures and real-time control. "
            "Disadvantage: Inflexible; changing the instruction set requires physically redesigning circuit wiring.\n"
            "2. Microprogrammed Control Unit: Control signals are stored as binary words (micro-instructions) in a dedicated Control ROM. "
            "Advantages: Highly flexible, easy to update/emulate complex instruction sets (CISC) by reprogramming ROM.\n"
            "Selection for our project: A Hardwired Control Unit was selected because our parking garage requires real-time, deterministic, nanosecond responses to physical vehicle sensors with minimal component overhead.")
    add_callout(f"Question: {q4_6}\n\nModel Viva Answer: {a4_6}", "Unit 4 - Question 6 (Directly Applicable)")

    q4_10 = ("Q10. A processor executes instructions using a basic processing unit and ALU. "
             "How would you trace the control signals, register transfers, and ALU operations required to execute a conditional branch instruction?")
    a4_10 = ("To execute a conditional branch (e.g., JZ FULL_LABEL - Jump if Zero/Full): "
             "1. Condition Evaluation: The Control Unit samples the Status Register Zero Flag (FULL). "
             "2. Micro-Operation if Condition True (FULL == 1): The branch target address is loaded into the Program Counter: PC <- Branch_Address. "
             "3. Micro-Operation if Condition False (FULL == 0): The PC simply increments sequentially: PC <- PC + 1. "
             "In our parking controller: If FULL == 1, the clock gate is disabled (CLK_EN = 0), preventing the state register from decrementing into negative underflow, and the Entry Gate remains locked. If FULL == 0, CLK_EN = 1, and the register transfers S <- S - 1.")
    add_callout(f"Question: {q4_10}\n\nModel Viva Answer: {a4_10}", "Unit 4 - Question 10 (Directly Applicable)")

    # ---------------------------------------------------------
    # SECTION 6: TOP 15 LAB VIVA QUESTIONS & MODEL ANSWERS
    # ---------------------------------------------------------
    add_h1("6. Top 15 Lab Viva & Defense Questions with Model Answers")

    p = doc.add_paragraph()
    p.add_run("These are the most critical, open-ended questions professors and lab examiners ask during hardware project defenses. Memorizing these concise engineering answers will ensure full marks:")

    viva_qa = [
        ("1. Why did you use D flip-flops (74HC74) instead of JK flip-flops (74HC73)?",
         "The 74HC74 D flip-flop requires only a single data input per bit and has standard corner power pins (Pin 14 VCC, Pin 7 GND). In contrast, the 74HC73 dual JK flip-flop features non-standard power pins (Pin 4 VCC, Pin 11 GND) and requires two excitation lines (J and K) per stage, increasing breadboard wire congestion significantly. D flip-flops with XOR toggle gates provide cleaner, modular breadboard wiring."),

        ("2. Walk me through the exact logic gates that prevent a car from entering when full.",
         "When state is 000_2, the zero-detector AND gate outputs FULL = 1. This signal passes through an inverter (74HC04) to produce ~FULL = 0. The ~FULL signal feeds a 2-input AND gate alongside the Entry Switch (IN_SW). When ~FULL = 0, the AND gate output is forced LOW (0), suppressing the clock pulse P_DN and keeping the Entry Gate indicator RED/Locked."),

        ("3. What happens if two cars trigger the entry and exit sensors at the exact same millisecond?",
         "This is handled by our Simultaneous Event Inhibit Logic: P_DN = IN * ~OUT * ~FULL and P_UP = OUT * ~IN * ~EMPTY. When both IN=1 and OUT=1 simultaneously, both clock pulses P_DN and P_UP evaluate to 0. The counter clock is suppressed (net count change = 0), while both gate driver OR gates assert HIGH, safely opening both entry and exit gates."),

        ("4. What happens if you remove the 10 kOhm pull-down resistors on the switches?",
         "Without pull-down resistors, the inputs float in a high-impedance state when switches are unpressed. CMOS inputs have extremely high input impedance (~10^12 Ohms) and pick up stray electric fields, floating unpredictably around the 2.5V threshold. The controller would count randomly, gates would chatter, and IC power consumption would surge."),

        ("5. What is contact bounce (switch bounce) and how would you resolve it in real industrial hardware?",
         "Mechanical switches do not close cleanly; their metal contacts physically bounce for 5 to 20 milliseconds, producing a burst of rapid 0-1-0 pulses that a high-speed digital counter registers as multiple cars! In our virtual simulator, bounce is idealized. In a real-world industrial circuit, we debounce using: (1) An RC low-pass filter with a Schmitt Trigger (74HC14), or (2) A Set-Reset (SR) latch cross-coupled NAND gate debouncer."),

        ("6. Why is Pin 6 (Input D) of the CD4511 decoder tied to Ground?",
         "The CD4511 is a Binary-Coded Decimal (BCD) decoder that accepts 4-bit numbers (0000 to 1001, representing 0 to 9). Our garage capacity is 7 spots, represented by 3 bits (S0, S1, S2). Input D carries a numerical weight of 8 (2^3). By permanently grounding Pin 6, we restrict inputs strictly to values 0–7, preventing the decoder from receiving invalid states (8–15) which would blank the display."),

        ("7. What is the role of Pins 3 (~LT), 4 (~BL), and 5 (LE) on the CD4511?",
         "Pin 3 (~LT) is Lamp Test: tied to +5V to disable lamp test mode (grounding it forces all segments ON). Pin 4 (~BL) is Blanking: tied to +5V to keep the display active (grounding it blanks the display). Pin 5 (LE) is Latch Enable: tied to Ground to operate in transparent mode so output segments track the counter in real time."),

        ("8. How does the Emergency Override switch bypass counter boundary limits?",
         "The Emergency switch (EMERG) connects directly to the final OR gates driving the barrier actuators: ENTRY_OPEN = EMERG + (IN & ~FULL) and EXIT_OPEN = EMERG + (OUT & ~EMPTY). When EMERG = 1, the OR gates output 1 regardless of the counter state or FULL flag, forcing both barrier arms wide open for evacuation."),

        ("9. Explain why the Reset button sets the counter to 7 instead of 0.",
         "In this controller, the counter tracks 'Available Spaces', not parked cars. When the garage is empty / reset, maximum spaces (7) are available. Therefore, the active-low reset signal is connected to the asynchronous PRESET (~PRE) pins of all three flip-flops, forcing Q2=1, Q1=1, Q0=1 (111_2 = 7)."),

        ("10. What is the difference between Synchronous and Asynchronous Reset?",
         "An Asynchronous Reset (used here) acts immediately upon assertion via dedicated internal clear/preset transistors, overriding the clock. A Synchronous Reset takes effect only on the next rising clock edge. Asynchronous reset ensures instant emergency initialization even if the sensor clock is absent."),

        ("11. What are Setup Time (t_su) and Hold Time (t_h) in the 74HC74 flip-flop?",
         "Setup Time (t_su = ~15 ns for 74HC74) is the minimum duration the data input (D) must remain stable BEFORE the rising clock edge arrives. Hold Time (t_h = ~0-3 ns) is the minimum duration the data must remain stable AFTER the clock edge. Violating these timing constraints causes metastability, where the flip-flop output oscillates unpredictably."),

        ("12. If garage capacity were expanded to 16 spaces, what modifications are required?",
         "Expanding to 16 spaces requires: (1) A 4-bit counter register (adding a 4th flip-flop FF3 for state S3), (2) Upgrading to a 4-bit synchronous steering network, (3) The FULL detector expands to a 4-input AND gate (~S3*~S2*~S1*~S0), and (4) The display requires a 2-digit BCD system using a binary-to-BCD converter (such as 74HC185) driving two separate CD4511 decoders for Tens and Units digits."),

        ("13. What is the propagation delay of this circuit and what is its maximum operating frequency?",
         "The critical path runs from sensor trigger -> AND gating -> XOR excitation -> flip-flop clock-to-Q -> AND zero-detect -> gate output. Each 74HC gate has a propagation delay of ~10 ns; the 74HC74 has t_pd ~ 15 ns. Total critical path delay is ~45 ns. This yields a maximum theoretical clocking frequency of f_max = 1 / 45 ns ~ 22 MHz, vastly exceeding human vehicle speeds (< 2 Hz)."),

        ("14. How would you represent this circuit in Verilog HDL for an FPGA implementation?",
         "In Verilog, the sequential register is coded as: always @(posedge clk or negedge rst_n) begin if (!rst_n) count <= 3'b111; else if (pulse_up) count <= count + 1'b1; else if (pulse_dn) count <= count - 1'b1; end. The status flags are continuous assignments: assign full = (count == 3'b000); assign empty = (count == 3'b111); assign entry_gate = emerg | (in_sw & ~full);"),

        ("15. What are the advantages of this hardwired controller over a microcontroller (like Arduino)?",
         "A hardwired discrete logic controller provides: (1) Instantaneous, deterministic microsecond response with zero software latency or interrupt overhead, (2) Immune to software crashes, stack overflows, or firmware corruption, and (3) Demonstrates fundamental low-level computer architecture hardware principles directly.")
    ]

    for q_text, a_text in viva_qa:
        q_p = doc.add_paragraph()
        q_p.paragraph_format.space_before = Pt(6)
        q_p.paragraph_format.space_after = Pt(2)
        q_p.paragraph_format.keep_with_next = True
        run_q = q_p.add_run(q_text)
        run_q.bold = True
        run_q.font.color.rgb = COLOR_SECONDARY

        a_p = doc.add_paragraph()
        a_p.paragraph_format.space_after = Pt(6)
        a_p.paragraph_format.left_indent = Inches(0.15)
        run_a = a_p.add_run(a_text)
        run_a.font.color.rgb = COLOR_TEXT

    # ---------------------------------------------------------
    # SECTION 7: TESTING & TROUBLESHOOTING MATRIX
    # ---------------------------------------------------------
    add_h1("7. Testing & Verification Matrix")

    test_table = doc.add_table(rows=8, cols=5)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate([Inches(0.6), Inches(1.5), Inches(1.5), Inches(1.7), Inches(1.6)]):
        test_table.rows[0].cells[i].width = w
    set_table_borders(test_table)

    test_headers = ["Test", "Scenario", "Stimulus / Inputs", "Expected Hardware Response", "COA Architectural Concept"]
    for i, h in enumerate(test_headers):
        cell = test_table.rows[0].cells[i]
        set_cell_background(cell, HEX_TABLE_HEADER)
        p_h = cell.paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9)

    test_data = [
        ("T1", "System Reset", "Press SW3 (Reset)", "Count = 7 (111_2), EMPTY=1, FULL=0, Gates closed", "Asynchronous Preset Micro-op"),
        ("T2", "Single Entry", "Pulse SW1 (Car In)", "Count decrements 7 -> 6 (110_2), Entry Green flashes", "Decrement ALU Micro-operation"),
        ("T3", "Fill to Full", "Enter 6 more cars", "Count reaches 0 (000_2), FULL=1, Red Alarm active", "Zero Detect Condition Code"),
        ("T4", "Blocked Entry", "Press SW1 when count=0", "Count stays 0; Entry stays Red/Locked; clock inhibited", "Conditional Branch / Inhibit Gating"),
        ("T5", "Normal Exit", "Pulse SW2 (Car Out)", "Count increments 0 -> 1 (001_2), FULL flag clears", "Increment ALU Micro-operation"),
        ("T6", "Simultaneous", "Press SW1 + SW2", "Count unchanged; both Entry & Exit Gates open", "Hazard Suppression / Inhibit"),
        ("T7", "Emergency", "Flip SW4 (EMERG) ON", "Both gates forced Green continuously; count frozen", "High-Priority Control Override")
    ]

    for row_idx, row_data in enumerate(test_data, start=1):
        bg = HEX_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            cell = test_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            p_c = cell.paragraphs[0]
            r_c = p_c.add_run(text)
            r_c.font.size = Pt(8.5)

    doc.add_paragraph()

    # Save Document
    output_path = r"C:\Users\vaibh\.gemini\antigravity\scratch\smart-parking-garage\Smart_Parking_Garage_Controller_COA_Guide.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()
