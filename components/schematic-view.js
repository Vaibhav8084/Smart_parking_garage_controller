// Digital Logic Schematic View with Real-time Signal Propagation
class SchematicView {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.startLoop();
  }

  startLoop() {
    this.render();
    requestAnimationFrame(() => this.startLoop());
  }

  render() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    const s = window.simState || {
      S0: 1, S1: 1, S2: 1,
      full: 0, empty: 1,
      entryGateOpen: 0, exitGateOpen: 0,
      inRaw: 0, outRaw: 0, emerg: 0,
      availableSpaces: 7
    };

    // Dark circuit canvas
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, w, h);

    // Grid dots
    ctx.fillStyle = '#1e293b';
    for (let x = 20; x < w; x += 20) {
      for (let y = 20; y < h; y += 20) {
        ctx.fillRect(x - 0.5, y - 0.5, 1.2, 1.2);
      }
    }

    // --- INPUT NODES (Left side) ---
    this.drawInputPort(ctx, 40, 90, 'IN_SW', s.inRaw);
    this.drawInputPort(ctx, 40, 170, 'OUT_SW', s.outRaw);
    this.drawInputPort(ctx, 40, 250, 'EMERG', s.emerg);
    this.drawInputPort(ctx, 40, 330, 'RESET', s.resetRaw || 0);

    // --- GATE LOGIC STAGE (Inhibit & Direction) ---
    // Gate 1: AND gate for Entry Inhibit: IN * NOT(FULL)
    this.drawANDGate(ctx, 160, 90, 'IN & ~FULL', s.inRaw && !s.full);
    this.drawWire(ctx, 70, 90, 160, 80, s.inRaw);

    // Gate 2: OR gate for Entry Gate: (IN & ~FULL) + EMERG
    this.drawORGate(ctx, 270, 100, 'ENTRY GATE', s.entryGateOpen);
    this.drawWire(ctx, 200, 90, 270, 90, s.inRaw && !s.full);
    this.drawWire(ctx, 70, 250, 250, 250, s.emerg);
    this.drawWire(ctx, 250, 250, 270, 110, s.emerg);

    // Output indicator: ENTRY GATE GREEN LED
    this.drawOutputPort(ctx, 360, 100, 'ENTRY_OPEN', s.entryGateOpen, '#22c55e');

    // Gate 3: AND gate for Exit Inhibit: OUT * NOT(EMPTY)
    this.drawANDGate(ctx, 160, 170, 'OUT & ~EMPTY', s.outRaw && !s.empty);
    this.drawWire(ctx, 70, 170, 160, 160, s.outRaw);

    // Gate 4: OR gate for Exit Gate: (OUT & ~EMPTY) + EMERG
    this.drawORGate(ctx, 270, 180, 'EXIT GATE', s.exitGateOpen);
    this.drawWire(ctx, 200, 170, 270, 170, s.outRaw && !s.empty);
    this.drawWire(ctx, 250, 250, 270, 190, s.emerg);

    // Output indicator: EXIT GATE GREEN LED
    this.drawOutputPort(ctx, 360, 180, 'EXIT_OPEN', s.exitGateOpen, '#22c55e');

    // --- 3-BIT SYNCHRONOUS REGISTER (Center-Right) ---
    // Flip-Flop Blocks
    this.drawFlipFlop(ctx, 460, 80, 'FF0 (LSB)', s.S0, !s.S0);
    this.drawFlipFlop(ctx, 460, 200, 'FF1', s.S1, !s.S1);
    this.drawFlipFlop(ctx, 460, 320, 'FF2 (MSB)', s.S2, !s.S2);

    // Clock Line distribution
    const clkSignal = (s.pulseDn || s.pulseUp);
    this.drawWire(ctx, 320, 30, 460, 95, clkSignal);
    this.drawWire(ctx, 430, 95, 460, 215, clkSignal);
    this.drawWire(ctx, 430, 215, 460, 335, clkSignal);
    ctx.fillStyle = clkSignal ? '#facc15' : '#64748b';
    ctx.font = '10px Fira Code';
    ctx.fillText('COUNT_CLK', 320, 24);

    // --- STATUS DETECTORS (FULL & EMPTY) ---
    // FULL Detector (Zero Detect: ~S2 & ~S1 & ~S0)
    this.drawANDGate(ctx, 620, 140, 'FULL DETECT', s.full);
    this.drawWire(ctx, 520, 125, 620, 130, !s.S0); // S0_bar
    this.drawWire(ctx, 520, 245, 620, 140, !s.S1); // S1_bar
    this.drawWire(ctx, 520, 365, 620, 150, !s.S2); // S2_bar
    this.drawOutputPort(ctx, 690, 140, 'FULL_FLAG', s.full, '#ef4444');

    // Feedback full wire to Entry inhibit
    this.drawWire(ctx, 690, 140, 710, 140, s.full);
    this.drawWire(ctx, 710, 140, 710, 50, s.full);
    this.drawWire(ctx, 710, 50, 150, 50, s.full);
    this.drawWire(ctx, 150, 50, 160, 100, !s.full);

    // EMPTY Detector (Max Detect: S2 & S1 & S0)
    this.drawANDGate(ctx, 620, 280, 'EMPTY DETECT', s.empty);
    this.drawWire(ctx, 520, 95, 620, 270, s.S0); // S0
    this.drawWire(ctx, 520, 215, 620, 280, s.S1); // S1
    this.drawWire(ctx, 520, 335, 620, 290, s.S2); // S2
    this.drawOutputPort(ctx, 690, 280, 'EMPTY_FLAG', s.empty, '#10b981');

    // --- CD4511 BCD TO 7-SEGMENT DECODER ---
    this.drawDecoderBlock(ctx, 760, 180, 100, 180, 'CD4511 BCD DECODER', s.availableSpaces);

    // Wires from FFs to CD4511 Inputs
    this.drawWire(ctx, 520, 95, 760, 210, s.S0);
    this.drawWire(ctx, 520, 215, 760, 240, s.S1);
    this.drawWire(ctx, 520, 335, 760, 270, s.S2);

    // 7-Segment Display representation
    this.draw7SegSchematic(ctx, 910, 230, s.availableSpaces);
  }

  drawInputPort(ctx, x, y, label, val) {
    ctx.fillStyle = val ? '#38bdf8' : '#1e293b';
    ctx.strokeStyle = val ? '#38bdf8' : '#475569';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(x - 30, y - 12, 55, 24, 4);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = val ? '#000' : '#94a3b8';
    ctx.font = 'bold 9px Fira Code';
    ctx.textAlign = 'center';
    ctx.fillText(label, x - 2, y + 4);
    ctx.textAlign = 'left';

    // Node dot
    ctx.fillStyle = val ? '#38bdf8' : '#64748b';
    ctx.beginPath();
    ctx.arc(x + 28, y, 4, 0, Math.PI * 2);
    ctx.fill();
  }

  drawOutputPort(ctx, x, y, label, val, color) {
    ctx.fillStyle = val ? color : '#1e293b';
    ctx.strokeStyle = val ? color : '#475569';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(x, y - 12, 65, 24, 4);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = val ? '#fff' : '#94a3b8';
    ctx.font = 'bold 9px Fira Code';
    ctx.fillText(label, x + 8, y + 4);

    if (val) {
      ctx.shadowColor = color;
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.arc(x - 6, y, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  drawANDGate(ctx, x, y, label, active) {
    ctx.fillStyle = active ? 'rgba(34, 197, 94, 0.15)' : '#111827';
    ctx.strokeStyle = active ? '#22c55e' : '#475569';
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(x, y - 18);
    ctx.lineTo(x + 20, y - 18);
    ctx.arc(x + 20, y, 18, -Math.PI / 2, Math.PI / 2);
    ctx.lineTo(x, y + 18);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 8px Fira Code';
    ctx.fillStyle = active ? '#22c55e' : '#64748b';
    ctx.fillText('AND', x + 8, y + 3);
  }

  drawORGate(ctx, x, y, label, active) {
    ctx.fillStyle = active ? 'rgba(56, 189, 248, 0.15)' : '#111827';
    ctx.strokeStyle = active ? '#38bdf8' : '#475569';
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(x, y - 18);
    ctx.quadraticCurveTo(x + 20, y - 16, x + 35, y);
    ctx.quadraticCurveTo(x + 20, y + 16, x, y + 18);
    ctx.quadraticCurveTo(x + 10, y, x, y - 18);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 8px Fira Code';
    ctx.fillStyle = active ? '#38bdf8' : '#64748b';
    ctx.fillText('OR', x + 12, y + 3);
  }

  drawFlipFlop(ctx, x, y, name, qVal, qbarVal) {
    ctx.fillStyle = '#151d2e';
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, 60, 75);
    ctx.fillRect(x, y, 60, 75);

    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 9px Fira Code';
    ctx.fillText(name, x + 6, y + 16);

    // Clock wedge
    ctx.beginPath();
    ctx.moveTo(x, y + 30);
    ctx.lineTo(x + 8, y + 35);
    ctx.lineTo(x, y + 40);
    ctx.stroke();

    // Outputs Q and Q_bar
    ctx.font = 'bold 10px Fira Code';
    ctx.fillStyle = qVal ? '#22c55e' : '#64748b';
    ctx.fillText(`Q: ${qVal}`, x + 24, y + 38);

    ctx.fillStyle = qbarVal ? '#22c55e' : '#64748b';
    ctx.fillText(`Q̄: ${qbarVal}`, x + 24, y + 58);
  }

  drawDecoderBlock(ctx, x, y, w, h, title, decVal) {
    ctx.fillStyle = '#111827';
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2;
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);

    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 10px Fira Code';
    ctx.fillText('CD4511', x + 16, y + 24);
    ctx.font = '8px Inter';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText('BCD to 7-SEG', x + 16, y + 38);

    // Inputs
    ctx.font = '8px Fira Code';
    ctx.fillText('A (S0)', x + 8, y + 65);
    ctx.fillText('B (S1)', x + 8, y + 95);
    ctx.fillText('C (S2)', x + 8, y + 125);
    ctx.fillText('D (GND)', x + 8, y + 155);

    // Outputs
    ctx.fillText('a..g ➔', x + w - 40, y + 95);
  }

  draw7SegSchematic(ctx, x, y, val) {
    ctx.fillStyle = '#000';
    ctx.fillRect(x, y - 45, 50, 90);
    ctx.strokeStyle = '#334155';
    ctx.strokeRect(x, y - 45, 50, 90);

    ctx.font = 'bold 44px Fira Code';
    ctx.fillStyle = '#22c55e';
    ctx.shadowColor = '#22c55e';
    ctx.shadowBlur = 10;
    ctx.textAlign = 'center';
    ctx.fillText(val, x + 25, y + 16);
    ctx.shadowBlur = 0;
    ctx.textAlign = 'left';
  }

  drawWire(ctx, x1, y1, x2, y2, active) {
    ctx.strokeStyle = active ? '#22c55e' : '#334155';
    ctx.lineWidth = active ? 2.5 : 1.5;

    ctx.beginPath();
    ctx.moveTo(x1, y1);

    // Manhattan right-angle routing
    const midX = (x1 + x2) / 2;
    ctx.lineTo(midX, y1);
    ctx.lineTo(midX, y2);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // Solder connection dot
    ctx.fillStyle = ctx.strokeStyle;
    ctx.beginPath();
    ctx.arc(x1, y1, 2.5, 0, Math.PI * 2);
    ctx.arc(x2, y2, 2.5, 0, Math.PI * 2);
    ctx.fill();
  }
}

window.SchematicView = SchematicView;
