# Python script to generate the LLT1 Course Report matching sample format with real project screenshots
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def generate_report():
    doc = docx.Document()

    # Standard Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    COLOR_NAVY = RGBColor(15, 23, 42)
    COLOR_BLUE = RGBColor(30, 58, 138)
    COLOR_TEXT = RGBColor(30, 41, 59)
    COLOR_MUTED = RGBColor(100, 116, 139)

    # Normal Style
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(11)
    normal.font.color.rgb = COLOR_TEXT
    normal.paragraph_format.line_spacing = 1.15
    normal_p_format = normal.paragraph_format
    normal_p_format.space_after = Pt(4)

    # Helper: Set Cell Shading
    def set_cell_background(cell, hex_color):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    # Helper: Set Table Borders
    def set_table_borders(table, color="94A3B8"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # Helper: Add Centered Header Text
    def add_center_p(text, bold=False, size=11, space_after=2, color=COLOR_TEXT):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        run.font.color.rgb = color
        return p

    # Helper: Add Code Box
    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F8FAFC")

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="0284C7"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.1)
        p.paragraph_format.right_indent = Inches(0.1)
        p.paragraph_format.line_spacing = 1.05

        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(15, 23, 42)
        doc.add_paragraph()

    # Helper: Add Figure with Caption
    def add_figure(img_path, caption, width=Inches(6.2)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            run_cap = p_cap.add_run(caption)
            run_cap.font.size = Pt(9.5)
            run_cap.font.italic = True
            run_cap.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # 1. INSTITUTION HEADER (Exactly matching sample)
    # -------------------------------------------------------------
    add_center_p("School of Computing", bold=True, size=13, space_after=1, color=COLOR_BLUE)
    add_center_p("Faculty of Engineering and Technology", bold=True, size=12, space_after=1)
    add_center_p("SRM Institute of Science and Technology", bold=True, size=13, space_after=1)
    add_center_p("SRM Nagar, Kattankulathur - 603 203, Chengalpattu Dt.", size=10, space_after=14, color=COLOR_MUTED)

    # -------------------------------------------------------------
    # 2. TITLE
    # -------------------------------------------------------------
    p_title_tag = doc.add_paragraph()
    p_title_tag.paragraph_format.space_after = Pt(2)
    p_title_tag.add_run("Title :").bold = True

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(14)
    run_t = p_title.add_run("LLT1 Component: SMART PARKING GARAGE CONTROLLER DESIGN")
    run_t.bold = True
    run_t.font.size = Pt(13)
    run_t.font.color.rgb = COLOR_BLUE

    # -------------------------------------------------------------
    # 3. SUBMITTED BY & SUBMITTED TO (Two Columns / Clean Table)
    # -------------------------------------------------------------
    sub_table = doc.add_table(rows=1, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sub_table.autofit = False
    sub_table.columns[0].width = Inches(3.25)
    sub_table.columns[1].width = Inches(3.25)

    # Left cell: Submitted by
    cell_left = sub_table.cell(0, 0)
    p_sub_by = cell_left.paragraphs[0]
    p_sub_by.paragraph_format.space_after = Pt(2)
    p_sub_by.add_run("Submitted by\n").bold = True
    p_sub_by.add_run("Vaibhav Singh - RA2511026010029\n"
                    "Kanika Arora - RA2511026010022")

    # Right cell: Submitted to
    cell_right = sub_table.cell(0, 1)
    p_sub_to = cell_right.paragraphs[0]
    p_sub_to.paragraph_format.space_after = Pt(2)
    p_sub_to.add_run("Submitted to\n").bold = True
    p_sub_to.add_run("Dr. S. Sadagopan\n"
                    "Associate Professor\n"
                    "School of Computing\n"
                    "Faculty of Engineering and Technology\n"
                    "SRM Institute of Science and Technology")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # 4. SRM LOGO IMAGE
    # -------------------------------------------------------------
    logo_path = r"C:\Users\vaibh\.gemini\antigravity\scratch\smart-parking-garage\sample_extracted\word\media\image1.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.add_run().add_picture(logo_path, width=Inches(3.2))

    # Academic Year
    add_center_p("Academic Year: 2026 – 2027 Odd Semester", bold=True, size=11, space_after=8, color=COLOR_BLUE)

    # Faculty Details repeat
    p_fac = doc.add_paragraph()
    p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac.paragraph_format.space_after = Pt(16)
    p_fac.add_run("Dr. S. Sadagopan\n"
                  "Associate Professor\n"
                  "School of Computing\n"
                  "Faculty of Engineering and Technology\n"
                  "SRM Institute of Science and Technology")

    # -------------------------------------------------------------
    # 5. SIMULATION TOOL SECTION (Matching sample format)
    # -------------------------------------------------------------
    p_sim_title = doc.add_paragraph()
    p_sim_title.paragraph_format.space_before = Pt(10)
    p_sim_title.paragraph_format.space_after = Pt(4)
    run_sim_t = p_sim_title.add_run("Simulation Tool")
    run_sim_t.bold = True
    run_sim_t.font.size = Pt(13)
    run_sim_t.font.color.rgb = COLOR_BLUE

    p_sim_desc = doc.add_paragraph()
    p_sim_desc.add_run(
        "Autodesk Tinkercad Circuits & Custom COA Digital Hardware Simulator is an interactive electronic workbench and "
        "digital logic simulation environment designed for building and testing Register-Transfer Level (RTL) computer "
        "architecture datapaths. It provides a complete virtual laboratory to construct, wire, probe, and verify discrete "
        "74HC-series digital logic circuits, flip-flops, decoders, and display drivers without requiring physical laboratory breadboards."
    )

    tools_features = [
        ("Virtual Breadboard & IC Workbench: ", "Features photorealistic solderless breadboard chassis with authentic tie-point matrices, dual +5V power rails, and ground distribution. Accurately simulates discrete 74HC logic ICs (74HC74 Dual D Flip-Flop, 74HC08 Quad AND, 74HC32 Quad OR, 74HC04 Hex Inverter, 74HC86 Quad XOR) and standard 4000-series decoders (CD4511 BCD-to-7-Segment driver)."),
        ("Register Datapath & Logic State Inspector: ", "Displays real-time digital voltage levels across all flip-flop Q and complementary Q_bar outputs (S2, S1, S0). Features an interactive mouse probe that dynamically reads net voltages (5.0V HIGH vs 0.0V LOW), pin numbers, and internal gate operations across all DIP-14 and DIP-16 packages."),
        ("Interactive Actuator & Hardware Subsystems: ", "Simulates tactile entry and exit sensor pushbuttons, SPDT emergency override toggle switches, animated motorized barrier arms that swing 90 degrees based on logic states, and Common-Cathode 7-segment display totems that update dynamically."),
        ("8-Channel Digital Logic Analyzer: ", "Provides an oscilloscope-style multi-channel timing waveform trace capturing raw sensor inputs (IN_SW, OUT_SW), clock pulses (COUNT_CLK), register bit lines (S0, S1, S2), condition flags (FULL), and gate driver outputs in real time.")
    ]
    for b_title, b_desc in tools_features:
        p_f = doc.add_paragraph(style='List Bullet')
        p_f.paragraph_format.space_after = Pt(3)
        p_f.add_run(b_title).bold = True
        p_f.add_run(b_desc)

    doc.add_paragraph()

    # -------------------------------------------------------------
    # 6. PROBLEM STATEMENTS TABLE
    # -------------------------------------------------------------
    p_ps = doc.add_paragraph()
    p_ps.paragraph_format.space_before = Pt(8)
    p_ps.paragraph_format.space_after = Pt(4)
    run_ps = p_ps.add_run("Problem statements (numbers as given in the list)")
    run_ps.bold = True
    run_ps.font.size = Pt(12)

    table_prob = doc.add_table(rows=3, cols=2)
    table_prob.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_prob.autofit = False
    table_prob.columns[0].width = Inches(0.8)
    table_prob.columns[1].width = Inches(5.7)
    set_table_borders(table_prob)

    # Header
    set_cell_background(table_prob.rows[0].cells[0], "1E293B")
    set_cell_background(table_prob.rows[0].cells[1], "1E293B")
    r0 = table_prob.rows[0].cells[0].paragraphs[0].add_run("No")
    r0.bold = True
    r0.font.color.rgb = RGBColor(255, 255, 255)
    r1 = table_prob.rows[0].cells[1].paragraphs[0].add_run("Problem statement")
    r1.bold = True
    r1.font.color.rgb = RGBColor(255, 255, 255)

    # Row 1
    table_prob.rows[1].cells[0].paragraphs[0].add_run("1").bold = True
    table_prob.rows[1].cells[1].paragraphs[0].add_run(
        "Design and implement a 3-Bit Synchronous Up/Down Counter Register Datapath using D Flip-Flops (74HC74) "
        "and XOR gates (74HC86) with CD4511 BCD-to-7-Segment Decoder to track available garage spaces (0 to 7 spaces) in real time."
    )

    # Row 2
    table_prob.rows[2].cells[0].paragraphs[0].add_run("2").bold = True
    table_prob.rows[2].cells[1].paragraphs[0].add_run(
        "Design and implement Hardwired Combinational Control Logic with Condition Status Flags (FULL at 000_2, EMPTY at 111_2), "
        "Automated Entry/Exit Barrier Gate Actuation, Emergency Evacuation Override, and Simultaneous Entry/Exit Event Hazard Filtering."
    )

    doc.add_paragraph()

    # -------------------------------------------------------------
    # 7. GROUP MEMBERS TABLE
    # -------------------------------------------------------------
    p_gm = doc.add_paragraph()
    p_gm.paragraph_format.space_before = Pt(6)
    p_gm.paragraph_format.space_after = Pt(4)
    run_gm = p_gm.add_run("Group members")
    run_gm.bold = True
    run_gm.font.size = Pt(12)

    table_gm = doc.add_table(rows=3, cols=3)
    table_gm.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_gm.autofit = False
    table_gm.columns[0].width = Inches(0.8)
    table_gm.columns[1].width = Inches(3.2)
    table_gm.columns[2].width = Inches(2.5)
    set_table_borders(table_gm)

    # Header
    for idx, h_text in enumerate(["S.No", "Name", "Registration No."]):
        cell = table_gm.rows[0].cells[idx]
        set_cell_background(cell, "1E293B")
        r = cell.paragraphs[0].add_run(h_text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Members
    members_data = [
        ("1", "Vaibhav Singh", "RA2511026010029"),
        ("2", "Kanika Arora", "RA2511026010022")
    ]
    for row_idx, (sno, name, regno) in enumerate(members_data, start=1):
        table_gm.rows[row_idx].cells[0].paragraphs[0].add_run(sno)
        table_gm.rows[row_idx].cells[1].paragraphs[0].add_run(name).bold = True
        table_gm.rows[row_idx].cells[2].paragraphs[0].add_run(regno)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. PROBLEM 1: SYNCHRONOUS REGISTER DATAPATH & BCD DISPLAY
    # -------------------------------------------------------------
    p_p1_title = doc.add_paragraph()
    run_p1_t = p_p1_title.add_run("Problem 1: 3-Bit Synchronous Up/Down Counter Datapath & Display Subsystem")
    run_p1_t.bold = True
    run_p1_t.font.size = Pt(14)
    run_p1_t.font.color.rgb = COLOR_BLUE

    p_obj1 = doc.add_paragraph()
    p_obj1.paragraph_format.space_after = Pt(6)
    p_obj1.add_run("Objective: ").bold = True
    p_obj1.add_run(
        "To design, model, and verify a 3-bit synchronous up/down state register (S2, S1, S0) capable of storing "
        "and tracking available parking spots from 7 down to 0 without propagation glitch hazards, and interface "
        "the state bus directly to a CD4511 BCD-to-7-segment decoder to drive a human-readable display."
    )

    p_alg1_head = doc.add_paragraph()
    p_alg1_head.paragraph_format.space_before = Pt(6)
    p_alg1_head.paragraph_format.space_after = Pt(4)
    p_alg1_head.add_run("1.1 Algorithm & RTL Register Transfer Sequence").bold = True

    alg1_steps = [
        "Initialize the register asynchronously: Assert active-low reset signal (~RESET = 0) connected to the asynchronous PRESET (~PRE) pins of flip-flops FF0, FF1, and FF2. State vector initializes to S = [S2, S1, S0] = 111_2 (Decimal 7 available spaces = empty garage).",
        "Wait in IDLE state for rising edge of COUNT_CLK pulse generated by vehicle sensor arrival.",
        "Direction Evaluation: If event is Car Exit (SW2 pressed), set direction control signal DIR = 1 (Count Up: S <- S + 1). If event is Car Entry (SW1 pressed), set DIR = 0 (Count Down: S <- S - 1).",
        "Parallel Next-State Toggle Evaluation (T0, T1, T2):",
        "  - Stage 0 (LSB): T0 = 1 (Always toggles on valid clock).",
        "  - Stage 1: T1 = (DIR * Q0) + (~DIR * ~Q0) = XNOR(DIR, Q0).",
        "  - Stage 2 (MSB): T2 = (DIR * Q1 * Q0) + (~DIR * ~Q1 * ~Q0).",
        "Compute D-Type Flip-Flop Excitation Inputs: D0 = Q0 XOR T0 = ~Q0; D1 = Q1 XOR T1; D2 = Q2 XOR T2.",
        "Clock Trigger: On rising edge of COUNT_CLK, parallel transfer occurs simultaneously: Q0_next = D0, Q1_next = D1, Q2_next = D2.",
        "BCD-to-7-Segment Decoding: Present 3-bit bus to CD4511 inputs A (Pin 7 <- S0), B (Pin 1 <- S1), C (Pin 2 <- S2), and D (Pin 6 <- 0V GND).",
        "Decoder maps binary vector into active-high segment outputs a, b, c, d, e, f, g to illuminate the Common-Cathode display."
    ]
    for step in alg1_steps:
        p_s = doc.add_paragraph(style='List Bullet')
        p_s.paragraph_format.space_after = Pt(2.5)
        p_s.add_run(step)

    # Hardware Equations Table
    p_eq_head = doc.add_paragraph()
    p_eq_head.paragraph_format.space_before = Pt(6)
    p_eq_head.paragraph_format.space_after = Pt(4)
    p_eq_head.add_run("1.2 State Excitation & CD4511 Truth Table").bold = True

    tbl_state = doc.add_table(rows=9, cols=6)
    tbl_state.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate([Inches(0.8), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.0), Inches(1.1)]):
        tbl_state.rows[0].cells[i].width = w
    set_table_borders(tbl_state)

    state_headers = ["Dec", "Current (S2 S1 S0)", "Next on Entry (-1)", "Next on Exit (+1)", "FULL", "CD4511 (a-g)"]
    for i, h in enumerate(state_headers):
        cell = tbl_state.rows[0].cells[i]
        set_cell_background(cell, "1E293B")
        r = cell.paragraphs[0].add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9)

    state_rows = [
        ("0", "000_2 (Full)", "000_2 (Inhibited)", "001_2", "1 (HIGH)", "1111110 ('0')"),
        ("1", "001_2", "000_2", "010_2", "0", "0110000 ('1')"),
        ("2", "010_2", "001_2", "011_2", "0", "1101101 ('2')"),
        ("3", "011_2", "010_2", "100_2", "0", "1111001 ('3')"),
        ("4", "100_2", "011_2", "101_2", "0", "0110011 ('4')"),
        ("5", "101_2", "100_2", "110_2", "0", "1011011 ('5')"),
        ("6", "110_2", "101_2", "111_2", "0", "1011111 ('6')"),
        ("7", "111_2 (Empty)", "110_2", "111_2 (Inhibited)", "0", "1110000 ('7')")
    ]
    for row_idx, r_data in enumerate(state_rows, start=1):
        bg = "F1F5F9" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = tbl_state.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            p_cell = cell.paragraphs[0]
            r = p_cell.add_run(text)
            r.font.size = Pt(8.5)

    doc.add_paragraph()

    # Structural Verilog HDL Code
    p_prog1_head = doc.add_paragraph()
    p_prog1_head.paragraph_format.space_before = Pt(6)
    p_prog1_head.paragraph_format.space_after = Pt(4)
    p_prog1_head.add_run("Program / Structural HDL Implementation (Module 1: Counter Datapath):").bold = True

    verilog_code1 = """; =========================================================================
; Module 1: 3-Bit Synchronous Up/Down Counter Register Datapath
; Target: 74HC74 Dual D-FFs, 74HC86 XOR, CD4511 BCD Decoder Driver
; =========================================================================
module parking_counter_datapath (
    input  wire       clk,          // Synchronous Count Clock (COUNT_CLK)
    input  wire       rst_n,        // Asynchronous Active-Low Preset (~PRESET)
    input  wire       dir,          // Direction: 1 = UP (Exit), 0 = DOWN (Entry)
    input  wire       count_en,     // Clock Enable from Hazard/Boundary Filter
    output reg  [2:0] count,        // 3-Bit State Bus [S2, S1, S0]
    output wire [6:0] seg           // CD4511 Decoded 7-Segment Outputs [a..g]
);

    // Internal D-type Flip-Flop Excitation wires
    wire t0, t1, t2;
    wire d0, d1, d2;

    // Toggle Equations:
    assign t0 = 1'b1;                                          // Bit 0 always toggles
    assign t1 = (dir & count[0]) | (~dir & ~count[0]);          // Bit 1 steering
    assign t2 = (dir & count[1] & count[0]) |                  // Bit 2 steering
                (~dir & ~count[1] & ~count[0]);

    // Next D-State: D = Q XOR T
    assign d0 = count[0] ^ t0;
    assign d1 = count[1] ^ t1;
    assign d2 = count[2] ^ t2;

    // Asynchronous Preset Sequential Register (Initialized to 3'b111 = 7 spaces)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 3'b111;        // Preset to EMPTY state (7 spaces)
        end else if (count_en) begin
            count[0] <= d0;
            count[1] <= d1;
            count[2] <= d2;
        end
    end

    // CD4511 BCD-to-7-Segment Decoder Behavioral Model
    cd4511_decoder u_cd4511 (
        .bcd({1'b0, count}),        // Input D grounded (4-bit BCD: 0000 to 0111)
        .lt_n(1'b1),                // Lamp Test disabled (tied HIGH)
        .bl_n(1'b1),                // Blanking disabled (tied HIGH)
        .le(1'b0),                  // Latch Enable transparent (tied LOW)
        .seg(seg)                   // Active-high segment drivers (a..g)
    );
endmodule"""
    add_code_block(verilog_code1)

    # Output Section with Real Screenshots!
    p_out1_head = doc.add_paragraph()
    p_out1_head.paragraph_format.space_before = Pt(6)
    p_out1_head.paragraph_format.space_after = Pt(4)
    p_out1_head.add_run("Output:").bold = True

    p_out1_desc = doc.add_paragraph()
    p_out1_desc.add_run(
        "The synchronous counter datapath and 7-segment display subsystem were verified across sequential entry and exit cycles. "
        "As seen in Figure 1, three cars entered the garage, successfully parking in Bay 01, Bay 02, and Bay 03. "
        "The state register automatically decremented from 111_2 to 100_2 (Decimal 4), and the CD4511 decoder drove the entrance "
        "totem display to cleanly illuminate '4' available spaces. Figure 2 shows the corresponding virtual breadboard layout "
        "with 74HC ICs, power rails, and bus wiring."
    )

    # Embed Figure 1: Interactive Garage
    fig1_path = r"C:\Users\vaibh\.gemini\antigravity\scratch\smart-parking-garage\report_images\fig1_interactive_garage.png"
    add_figure(fig1_path, "Figure 1: Real-time simulation of the 3-bit synchronous counter datapath and parking facility, showing 3 cars parked, state register S = [1, 0, 0] (Decimal 4 available spaces), and the CD4511-driven 7-segment entrance totem display indicating '4'.", width=Inches(6.3))

    # Embed Figure 2: Virtual Breadboard
    fig2_path = r"C:\Users\vaibh\.gemini\antigravity\scratch\smart-parking-garage\report_images\fig2_virtual_breadboard.png"
    add_figure(fig2_path, "Figure 2: Virtual dual breadboard wiring layout showing the 74HC74 dual flip-flop registers (U2, U3), 74HC08 AND gate (U4), 74HC32 OR gate (U5), 74HC04 inverter (U6), power distribution rails, and signal lines.", width=Inches(6.0))

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. PROBLEM 2: HARDWIRED CONTROL LOGIC & GATE ACTUATION
    # -------------------------------------------------------------
    p_p2_title = doc.add_paragraph()
    run_p2_t = p_p2_title.add_run("Problem 2: Hardwired Control Unit, Condition Codes & Gate Actuation")
    run_p2_t.bold = True
    run_p2_t.font.size = Pt(14)
    run_p2_t.font.color.rgb = COLOR_BLUE

    p_obj2 = doc.add_paragraph()
    p_obj2.paragraph_format.space_after = Pt(6)
    p_obj2.add_run("Objective: ").bold = True
    p_obj2.add_run(
        "To design, model, and verify hardwired combinational control logic that decodes boundary status flags "
        "(FULL and EMPTY), actuates automated motorized barrier gates, enforces entry prevention when the garage "
        "is full, cancels simultaneous entry/exit hazards, and provides high-priority emergency evacuation override."
    )

    p_alg2_head = doc.add_paragraph()
    p_alg2_head.paragraph_format.space_before = Pt(6)
    p_alg2_head.paragraph_format.space_after = Pt(4)
    p_alg2_head.add_run("2.1 Control Algorithm & Combinational Logic Design").bold = True

    alg2_steps = [
        "Status Flag Decoding (Zero / Boundary Detection):",
        "  - FULL Flag (Zero Detect): FULL = ~S2 * ~S1 * ~S0 (Asserts HIGH only when state is 000_2).",
        "  - EMPTY Flag (Max Detect): EMPTY = S2 * S1 * S0 (Asserts HIGH only when state is 111_2).",
        "Automated Entry Gate Barrier Actuation: ENTRY_GATE_OPEN = EMERG + (IN_SW * ~FULL). Gate opens if emergency override is active OR if an entering car arrives AND the garage is NOT full. If FULL == 1, entry gate stays locked (RED).",
        "Automated Exit Gate Barrier Actuation: EXIT_GATE_OPEN = EMERG + (OUT_SW * ~EMPTY). Gate opens if emergency is active OR if an exiting car arrives AND the garage is NOT empty.",
        "Hazard & Simultaneous Event Filtration: If both entry and exit sensors trigger at the exact same instant (IN_SW = 1 and OUT_SW = 1):",
        "  - Count Down Pulse: P_DN = IN_SW * ~OUT_SW * ~FULL * ~EMERG",
        "  - Count Up Pulse: P_UP = OUT_SW * ~IN_SW * ~EMPTY * ~EMERG",
        "  - When IN_SW * OUT_SW == 1, both P_DN and P_UP evaluate to 0. Clock is inhibited (net count delta = 0) while both gates open safely.",
        "Emergency Evacuation Override: Master switch EMERG asserts HIGH. Overrides all counter limits, gates open continuously (100%), and clock counting is bypassed."
    ]
    for step in alg2_steps:
        p_s = doc.add_paragraph(style='List Bullet')
        p_s.paragraph_format.space_after = Pt(2.5)
        p_s.add_run(step)

    # Program 2: Verilog Control Unit
    p_prog2_head = doc.add_paragraph()
    p_prog2_head.paragraph_format.space_before = Pt(6)
    p_prog2_head.paragraph_format.space_after = Pt(4)
    p_prog2_head.add_run("Program / Structural HDL Implementation (Module 2: Hardwired Control Unit):").bold = True

    verilog_code2 = """; =========================================================================
; Module 2: Hardwired Control Unit & Condition Status Flag Generator
; Target: 74HC08 Quad AND, 74HC32 Quad OR, 74HC04 Hex Inverter
; =========================================================================
module parking_control_unit (
    input  wire [2:0] state,        // State Bus [S2, S1, S0] from Datapath
    input  wire       in_sw,        // Car Entry Sensor Switch
    input  wire       out_sw,       // Car Exit Sensor Switch
    input  wire       emerg,        // Emergency Override SPDT Switch
    output wire       full_flag,    // Status Flag: Zero Detect (Garage Full)
    output wire       empty_flag,   // Status Flag: Max Detect (Garage Empty)
    output wire       entry_gate,   // Entry Barrier Actuator (1=Open, 0=Locked)
    output wire       exit_gate,    // Exit Barrier Actuator (1=Open, 0=Closed)
    output wire       pulse_dn,     // Gated Down-Count Pulse to Datapath
    output wire       pulse_up,     // Gated Up-Count Pulse to Datapath
    output wire       count_clk     // Global Clock Line
);

    // 1. Condition Status Flag Decoders
    // FULL: Active-High Zero Detect (~S2 * ~S1 * ~S0)
    assign full_flag  = (~state[2]) & (~state[1]) & (~state[0]);

    // EMPTY: Active-High Max Detect (S2 * S1 * S0)
    assign empty_flag = state[2] & state[1] & state[0];

    // 2. Barrier Gate Driver Actuation Logic
    assign entry_gate = emerg | (in_sw & ~full_flag);
    assign exit_gate  = emerg | (out_sw & ~empty_flag);

    // 3. Hazard Filter & Clock Pulse Steering (Simultaneous In+Out Cancellation)
    assign pulse_dn   = in_sw  & (~out_sw) & (~full_flag)  & (~emerg);
    assign pulse_up   = out_sw & (~in_sw)  & (~empty_flag) & (~emerg);

    // Combined Clock Line: COUNT_CLK pulses on either valid entry or exit
    assign count_clk  = pulse_dn | pulse_up;

endmodule"""
    add_code_block(verilog_code2)

    # Output Section with Real Screenshot!
    p_out2_head = doc.add_paragraph()
    p_out2_head.paragraph_format.space_before = Pt(6)
    p_out2_head.paragraph_format.space_after = Pt(4)
    p_out2_head.add_run("Output:").bold = True

    p_out2_desc = doc.add_paragraph()
    p_out2_desc.add_run(
        "The control unit was verified under comprehensive test scenarios including blocked entry attempts when full, "
        "simultaneous entry and exit triggers, and emergency override activation. The automated verification harness "
        "executed all 7 formal test assertions with 100% pass rates, as captured in Figure 3. The execution log confirms "
        "proper assertion of status flags and gate inhibits."
    )

    # Embed Figure 3: Automated Test Suite Screenshot
    fig3_path = r"C:\Users\vaibh\.gemini\antigravity\scratch\smart-parking-garage\report_images\fig3_automated_tests.png"
    add_figure(fig3_path, "Figure 3: Automated hardware verification harness and execution log asserting 100% pass rate across boundary conditions, full-capacity entry blocking, simultaneous event hazard filtering, and emergency override.", width=Inches(6.2))

    doc.add_page_break()

    # -------------------------------------------------------------
    # 10. COA ARCHITECTURE MAPPING & VIVA DEFENSE SUMMARY
    # -------------------------------------------------------------
    p_coa_title = doc.add_paragraph()
    run_coa_t = p_coa_title.add_run("Computer Organization & Architecture (COA) Academic Mapping")
    run_coa_t.bold = True
    run_coa_t.font.size = Pt(14)
    run_coa_t.font.color.rgb = COLOR_BLUE

    p_coa_desc = doc.add_paragraph()
    p_coa_desc.add_run(
        "This project directly embodies the core architectural principles of modern computer processors. "
        "The table below highlights the 1-to-1 equivalence between this controller and general-purpose CPU micro-architectures:"
    )

    coa_map_table = doc.add_table(rows=6, cols=3)
    coa_map_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate([Inches(1.8), Inches(2.3), Inches(2.4)]):
        coa_map_table.rows[0].cells[i].width = w
    set_table_borders(coa_map_table)

    for i, h in enumerate(["COA Concept", "Microprocessor Subsystem", "Parking Garage Controller Equivalent"]):
        cell = coa_map_table.rows[0].cells[i]
        set_cell_background(cell, "1E293B")
        r = cell.paragraphs[0].add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9)

    coa_map_rows = [
        ("Register Storage", "Program Counter (PC) / Accumulator", "3-Bit Flip-Flop Cluster (S2, S1, S0) storing system status across clock cycles."),
        ("ALU Datapath", "Arithmetic Logic Unit (ALU)", "XOR-based Incrementer/Decrementer datapath executing micro-ops S <- S + 1 and S <- S - 1."),
        ("Condition Codes", "Status Register (EFLAGS Zero Flag)", "FULL detector gate (S=000_2) acting as CPU Zero Flag (ZF) to conditionally branch / inhibit."),
        ("Control Unit", "Hardwired Control Matrix", "74HC08 AND and 74HC32 OR gates decoding instructions with single-gate propagation delay."),
        ("Bus Interconnect", "Internal Data Bus & I/O Decoder", "3-Bit parallel state bus distributing operands from register file to CD4511 display controller.")
    ]
    for row_idx, r_data in enumerate(coa_map_rows, start=1):
        bg = "F1F5F9" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = coa_map_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            p_cell = cell.paragraphs[0]
            r = p_cell.add_run(text)
            r.font.size = Pt(8.5)

    doc.add_paragraph()

    p_viva_head = doc.add_paragraph()
    p_viva_head.paragraph_format.space_before = Pt(8)
    p_viva_head.paragraph_format.space_after = Pt(4)
    run_vh = p_viva_head.add_run("Top 5 Viva Questions & Defense Answers for Examination:")
    run_vh.bold = True
    run_vh.font.size = Pt(12)
    run_vh.font.color.rgb = COLOR_BLUE

    viva_items = [
        ("1. Why use a Synchronous counter over an Asynchronous (Ripple) counter?",
         "Ripple counters suffer from accumulated propagation delay across flip-flops, producing transient glitches (race hazards) on output bits. In this controller, an intermediate glitch could momentarily flash 000_2, falsely triggering the FULL alarm and locking the gate. Synchronous counters clock all flip-flops simultaneously, guaranteeing glitch-free state transitions."),

        ("2. Walk me through the exact logic preventing entry when full.",
         "When state S = 000_2, the zero-detector AND gate outputs FULL = 1. This signal is inverted to ~FULL = 0 and fed into an AND gate alongside the Entry Switch: P_DN = IN_SW * ~FULL. When ~FULL = 0, the AND gate output is forced LOW, blocking the clock pulse from reaching the flip-flops and keeping the entry barrier locked (RED)."),

        ("3. Why are CD4511 auxiliary pins LT, BL, and LE wired to specific rails?",
         "Pin 3 (~LT, Lamp Test) is tied to +5V (HIGH) to disable lamp test mode (grounding it forces all segments to '8'). Pin 4 (~BL, Blanking) is tied to +5V (HIGH) to prevent blanking the display. Pin 5 (LE, Latch Enable) is tied to Ground (LOW) so the decoder operates in transparent mode, updating segments in real time."),

        ("4. What is the role of the 10 kOhm pull-down resistors on switches?",
         "Without pull-down resistors, an open switch leaves CMOS gate inputs in a floating (High-Impedance / Hi-Z) state. High-impedance CMOS inputs act as antennas picking up ambient electromagnetic noise, randomly toggling between 0 and 1. The 10 kOhm resistors ensure a clean 0V reference when buttons are unpressed."),

        ("5. How does the Emergency Override switch bypass counter logic?",
         "The Emergency signal (EMERG) connects directly to final OR gates driving the gates: ENTRY_OPEN = EMERG + (IN_SW * ~FULL). When EMERG = 1, the OR gate output is forced HIGH regardless of the counter state or FULL flag, opening both barrier gates continuously.")
    ]

    for q_t, a_t in viva_items:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(4)
        p_q.paragraph_format.space_after = Pt(1)
        r_q = p_q.add_run(q_t)
        r_q.bold = True
        r_q.font.color.rgb = COLOR_NAVY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(5)
        p_a.paragraph_format.left_indent = Inches(0.2)
        r_a = p_a.add_run(a_t)
        r_a.font.size = Pt(10)

    # Save Document
    output_filename = r"C:\Users\vaibh\.gemini\antigravity\scratch\smart-parking-garage\LLT1_Smart_Parking_Garage_Controller_Report.docx"
    doc.save(output_filename)
    print(f"Report successfully generated at: {output_filename}")

if __name__ == "__main__":
    generate_report()
