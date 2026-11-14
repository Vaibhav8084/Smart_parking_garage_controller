// Interactive Virtual Breadboard Canvas with Live 74xx ICs, Wires, and Voltage Probing
class BreadboardView {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.hoveredPin = null;

    // Component placement on breadboard
    this.ics = [
      { id: 'U2', name: '74HC74 (FF0, FF1)', x: 120, y: 190, pins: 14, w: 90, h: 48, type: 'dip14' },
      { id: 'U3', name: '74HC74 (FF2)', x: 250, y: 190, pins: 14, w: 90, h: 48, type: 'dip14' },
      { id: 'U4', name: '74HC08 (AND)', x: 380, y: 190, pins: 14, w: 90, h: 48, type: 'dip14' },
      { id: 'U5', name: '74HC32 (OR)', x: 510, y: 190, pins: 14, w: 90, h: 48, type: 'dip14' },
      { id: 'U6', name: '74HC04 (NOT)', x: 640, y: 190, pins: 14, w: 90, h: 48, type: 'dip14' },
      { id: 'U7', name: '74HC86 (XOR)', x: 770, y: 190, pins: 14, w: 90, h: 48, type: 'dip14' },
      { id: 'U1', name: 'CD4511 (BCD-to-7Seg)', x: 910, y: 190, pins: 16, w: 104, h: 48, type: 'dip16' }
    ];

    // Discrete board components
    this.boardComponents = [
      { id: 'DISP', name: '7-Segment Display (Common Cathode)', x: 1050, y: 170, w: 60, h: 90, type: 'display' },
      { id: 'LED_ENTRY', name: 'Entry Gate LED (D1)', x: 160, y: 380, color: '#22c55e', type: 'led' },
      { id: 'LED_FULL', name: 'Garage Full LED (D3)', x: 220, y: 380, color: '#ef4444', type: 'led' },
      { id: 'LED_EXIT', name: 'Exit Gate LED (D2)', x: 280, y: 380, color: '#22c55e', type: 'led' },
      { id: 'SW_IN_B', name: 'Entry Tactile SW1', x: 80, y: 380, w: 30, h: 30, type: 'button' },
      { id: 'SW_OUT_B', name: 'Exit Tactile SW2', x: 380, y: 380, w: 30, h: 30, type: 'button' }
    ];

    // Wire connections between pins and nodes
    this.wires = [
      // Power rails to ICs
      { from: [120 + 85, 185], to: [120 + 85, 75], color: '#ef4444', label: 'VCC (+5V)', active: () => 1 },
      { from: [120 + 40, 245], to: [120 + 40, 310], color: '#1e293b', label: 'GND (0V)', active: () => 0 },
      { from: [910 + 95, 185], to: [910 + 95, 75], color: '#ef4444', label: 'CD4511 VDD', active: () => 1 },
      { from: [910 + 50, 245], to: [910 + 50, 310], color: '#1e293b', label: 'CD4511 VSS', active: () => 0 },
      
      // Counter State Lines (S0, S1, S2) from Flip-Flops to CD4511
      { from: [120 + 35, 240], to: [910 + 42, 245], color: '#38bdf8', label: 'NET: S0 (LSB)', active: () => window.simState ? window.simState.S0 : 1 },
      { from: [120 + 75, 240], to: [910 + 10, 185], color: '#10b981', label: 'NET: S1', active: () => window.simState ? window.simState.S1 : 1 },
      { from: [250 + 35, 240], to: [910 + 20, 185], color: '#a855f7', label: 'NET: S2 (MSB)', active: () => window.simState ? window.simState.S2 : 1 },

      // CD4511 to 7-Segment Segments
      { from: [910 + 80, 245], to: [1050 + 10, 220], color: '#facc15', label: 'SEG a', active: () => window.simState ? window.simState.segments[0] : 1 },
      { from: [910 + 70, 245], to: [1050 + 20, 220], color: '#facc15', label: 'SEG b', active: () => window.simState ? window.simState.segments[1] : 1 },
      { from: [910 + 60, 245], to: [1050 + 30, 220], color: '#facc15', label: 'SEG c', active: () => window.simState ? window.simState.segments[2] : 1 },
      { from: [910 + 50, 245], to: [1050 + 40, 220], color: '#facc15', label: 'SEG d', active: () => window.simState ? window.simState.segments[3] : 1 },

      // Status Flags Wires
      { from: [380 + 35, 240], to: [220, 375], color: '#ef4444', label: 'NET: FULL_FLAG', active: () => window.simState ? window.simState.full : 0 },
      { from: [510 + 35, 240], to: [160, 375], color: '#22c55e', label: 'NET: ENTRY_GATE', active: () => window.simState ? window.simState.entryGateOpen : 0 }
    ];

    // Mouse listener for pin probing
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      this.checkPinHover(mouseX, mouseY);
    });

    this.render = this.render.bind(this);
    this.startLoop();
  }

  startLoop() {
    this.render();
    requestAnimationFrame(() => this.startLoop());
  }

  checkPinHover(mx, my) {
    let found = null;

    // Check IC pins
    for (const ic of this.ics) {
      const pinCount = ic.pins;
      const spacing = ic.w / (pinCount / 2 + 1);

      // Top row pins (Pin 14 down to 8 or 16 down to 9)
      for (let i = 0; i < pinCount / 2; i++) {
        const px = ic.x + (i + 1) * spacing;
        const py = ic.y;
        if (Math.hypot(mx - px, my - py) < 10) {
          const pinNum = pinCount - i;
          found = { ic: ic.name, pin: pinNum, x: px, y: py, func: this.getPinFunc(ic.id, pinNum) };
          break;
        }
      }

      // Bottom row pins (Pin 1 to 7 or 1 to 8)
      for (let i = 0; i < pinCount / 2; i++) {
        const px = ic.x + (i + 1) * spacing;
        const py = ic.y + ic.h;
        if (Math.hypot(mx - px, my - py) < 10) {
          const pinNum = i + 1;
          found = { ic: ic.name, pin: pinNum, x: px, y: py, func: this.getPinFunc(ic.id, pinNum) };
          break;
        }
      }
      if (found) break;
    }

    this.hoveredPin = found;
    const insp = document.getElementById('inspectorContent');
    if (insp) {
      if (found) {
        const volt = found.func.level();
        insp.innerHTML = `<span style="color:#38bdf8;">${found.ic}</span> &bull; <b>Pin ${found.pin}</b> (${found.func.name}) &bull; Voltage: <b style="color:${volt >= 2.5 ? '#22c55e' : '#94a3b8'}">${volt.toFixed(1)}V (${volt >= 2.5 ? 'HIGH / 1' : 'LOW / 0'})</b> &bull; Net: <code>${found.func.net}</code>`;
      } else {
        insp.textContent = 'Hover over an IC pin or tie point to inspect live logic voltage levels...';
      }
    }
  }

  getPinFunc(icId, pinNum) {
    const s = window.simState || { S0: 1, S1: 1, S2: 1, full: 0, empty: 1, entryGateOpen: 0 };

    if (icId === 'U2') {
      if (pinNum === 14) return { name: 'VCC', net: '+5V_RAIL', level: () => 5.0 };
      if (pinNum === 7) return { name: 'GND', net: 'GND_RAIL', level: () => 0.0 };
      if (pinNum === 5) return { name: '1Q (S0)', net: 'BUS_S0', level: () => s.S0 ? 5.0 : 0.0 };
      if (pinNum === 6) return { name: '1Q̄', net: 'BUS_S0_BAR', level: () => s.S0 ? 0.0 : 5.0 };
      if (pinNum === 9) return { name: '2Q (S1)', net: 'BUS_S1', level: () => s.S1 ? 5.0 : 0.0 };
      if (pinNum === 3) return { name: '1CLK', net: 'COUNT_CLK', level: () => s.pulseDn || s.pulseUp ? 5.0 : 0.0 };
      return { name: `Pin ${pinNum}`, net: 'LOGIC_NET', level: () => 5.0 };
    }
    if (icId === 'U3') {
      if (pinNum === 14) return { name: 'VCC', net: '+5V_RAIL', level: () => 5.0 };
      if (pinNum === 7) return { name: 'GND', net: 'GND_RAIL', level: () => 0.0 };
      if (pinNum === 5) return { name: '1Q (S2)', net: 'BUS_S2', level: () => s.S2 ? 5.0 : 0.0 };
      return { name: `Pin ${pinNum}`, net: 'LOGIC_NET', level: () => 5.0 };
    }
    if (icId === 'U1') {
      if (pinNum === 16) return { name: 'VDD', net: '+5V_RAIL', level: () => 5.0 };
      if (pinNum === 8) return { name: 'VSS', net: 'GND_RAIL', level: () => 0.0 };
      if (pinNum === 7) return { name: 'Input A', net: 'BUS_S0', level: () => s.S0 ? 5.0 : 0.0 };
      if (pinNum === 1) return { name: 'Input B', net: 'BUS_S1', level: () => s.S1 ? 5.0 : 0.0 };
      if (pinNum === 2) return { name: 'Input C', net: 'BUS_S2', level: () => s.S2 ? 5.0 : 0.0 };
      if (pinNum === 6) return { name: 'Input D', net: 'GND', level: () => 0.0 };
      return { name: `Segment Out`, net: 'DISP_BUS', level: () => 5.0 };
    }
    return { name: `Pin ${pinNum}`, net: 'SIGNAL', level: () => 5.0 };
  }

  render() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Breadboard base color
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, w, h);

    // Draw Breadboard 1 and Breadboard 2 chassis
    this.drawBreadboardChassis(ctx, 40, 40, 520, 560, 'BREADBOARD 1: CONTROL & REGISTERS');
    this.drawBreadboardChassis(ctx, 580, 40, 560, 560, 'BREADBOARD 2: STEERING & DISPLAY');

    // Draw Wires (underneath components)
    this.drawWires(ctx);

    // Draw IC Chips
    this.ics.forEach(ic => this.drawDIP(ctx, ic));

    // Draw Board Components (LEDs, 7-Seg, Pushbuttons)
    this.drawBoardComponents(ctx);

    // Draw Pin Hover Highlight
    if (this.hoveredPin) {
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(this.hoveredPin.x, this.hoveredPin.y, 8, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.arc(this.hoveredPin.x, this.hoveredPin.y, 4, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  drawBreadboardChassis(ctx, bx, by, bw, bh, title) {
    // Plastic body
    ctx.fillStyle = '#e2e8f0';
    ctx.beginPath();
    ctx.roundRect(bx, by, bw, bh, 8);
    ctx.fill();
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Title on breadboard
    ctx.fillStyle = '#64748b';
    ctx.font = 'bold 10px Fira Code';
    ctx.fillText(title, bx + 16, by + 24);

    // Center trough (channel)
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(bx + 10, by + 185, bw - 20, 16);

    // Top Power Rails (+ and -)
    ctx.strokeStyle = '#ef4444'; // Red (+)
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(bx + 15, by + 50);
    ctx.lineTo(bx + bw - 15, by + 50);
    ctx.stroke();

    ctx.strokeStyle = '#0284c7'; // Blue (-)
    ctx.beginPath();
    ctx.moveTo(bx + 15, by + 75);
    ctx.lineTo(bx + bw - 15, by + 75);
    ctx.stroke();

    // Bottom Power Rails
    ctx.strokeStyle = '#ef4444';
    ctx.beginPath();
    ctx.moveTo(bx + 15, by + bh - 55);
    ctx.lineTo(bx + bw - 15, by + bh - 55);
    ctx.stroke();

    ctx.strokeStyle = '#0284c7';
    ctx.beginPath();
    ctx.moveTo(bx + 15, by + bh - 30);
    ctx.lineTo(bx + bw - 15, by + bh - 30);
    ctx.stroke();

    // Tie Points (Holes) Grid
    ctx.fillStyle = '#475569';
    for (let x = bx + 25; x < bx + bw - 20; x += 14) {
      // Top section (rows a-e)
      for (let y = by + 95; y < by + 175; y += 14) {
        ctx.beginPath();
        ctx.arc(x, y, 1.8, 0, Math.PI * 2);
        ctx.fill();
      }
      // Bottom section (rows f-j)
      for (let y = by + 215; y < by + 295; y += 14) {
        ctx.beginPath();
        ctx.arc(x, y, 1.8, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  drawDIP(ctx, ic) {
    const { x, y, w, h, pins, name, id } = ic;

    // IC Body (Epoxy Black)
    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, 3);
    ctx.fill();
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Notch on left end (Pin 1 orientation)
    ctx.fillStyle = '#334155';
    ctx.beginPath();
    ctx.arc(x, y + h / 2, 5, -Math.PI / 2, Math.PI / 2);
    ctx.fill();

    // IC Label Text
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 9px Fira Code';
    ctx.textAlign = 'center';
    ctx.fillText(id, x + w / 2, y + h / 2 - 3);
    ctx.font = '7px Inter';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText(name.split(' ')[0], x + w / 2, y + h / 2 + 8);
    ctx.textAlign = 'left';

    // Metal Pins
    const pinCount = pins;
    const spacing = w / (pinCount / 2 + 1);

    for (let i = 0; i < pinCount / 2; i++) {
      const px = x + (i + 1) * spacing;

      // Top pin
      ctx.fillStyle = '#94a3b8';
      ctx.fillRect(px - 2, y - 6, 4, 7);

      // Bottom pin
      ctx.fillRect(px - 2, y + h - 1, 4, 7);
    }
  }

  drawWires(ctx) {
    this.wires.forEach(w => {
      const isHigh = w.active();
      ctx.strokeStyle = isHigh ? (w.color === '#ef4444' ? '#ef4444' : '#22c55e') : '#64748b';
      ctx.lineWidth = isHigh ? 3 : 2;

      ctx.beginPath();
      ctx.moveTo(w.from[0], w.from[1]);

      // Bezier curve for breadboard wire realism
      const midY = (w.from[1] + w.to[1]) / 2 + (w.from[0] > w.to[0] ? -20 : 20);
      ctx.quadraticCurveTo((w.from[0] + w.to[0]) / 2, midY, w.to[0], w.to[1]);
      ctx.stroke();

      // Pin landing solder dots
      ctx.fillStyle = ctx.strokeStyle;
      ctx.beginPath();
      ctx.arc(w.from[0], w.from[1], 3, 0, Math.PI * 2);
      ctx.arc(w.to[0], w.to[1], 3, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  drawBoardComponents(ctx) {
    // 7-Segment Display on Breadboard
    const disp = this.boardComponents.find(c => c.id === 'DISP');
    if (disp) {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(disp.x, disp.y, disp.w, disp.h);
      ctx.strokeStyle = '#334155';
      ctx.strokeRect(disp.x, disp.y, disp.w, disp.h);

      // Draw the active digit glowing
      const digit = window.simState ? window.simState.availableSpaces : 7;
      ctx.font = 'bold 44px Fira Code';
      ctx.fillStyle = '#22c55e';
      ctx.shadowColor = '#22c55e';
      ctx.shadowBlur = 12;
      ctx.textAlign = 'center';
      ctx.fillText(digit, disp.x + disp.w / 2, disp.y + disp.h / 2 + 16);
      ctx.shadowBlur = 0;
      ctx.textAlign = 'left';
    }

    // LEDs on Breadboard
    const leds = this.boardComponents.filter(c => c.type === 'led');
    leds.forEach(l => {
      const isOn = (l.id === 'LED_FULL' && window.simState && window.simState.full) ||
                   (l.id === 'LED_ENTRY' && window.simState && window.simState.entryGateOpen) ||
                   (l.id === 'LED_EXIT' && window.simState && window.simState.exitGateOpen);

      ctx.fillStyle = isOn ? l.color : '#334155';
      ctx.beginPath();
      ctx.arc(l.x, l.y, 8, 0, Math.PI * 2);
      ctx.fill();

      if (isOn) {
        ctx.shadowColor = l.color;
        ctx.shadowBlur = 14;
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      ctx.font = '8px Inter';
      ctx.fillStyle = '#64748b';
      ctx.fillText(l.name.split(' ')[0], l.x - 14, l.y + 18);
    });
  }
}

window.BreadboardView = BreadboardView;
