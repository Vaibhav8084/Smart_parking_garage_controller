// Digital Logic Analyzer Waveform Capture Canvas
class WaveformView {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.paused = false;

    // Buffer of captured points
    this.maxSamples = 400;
    this.history = [];

    // Channel definitions
    this.channels = [
      { id: 'inRaw', name: 'CH1: IN_SW', color: '#38bdf8' },
      { id: 'outRaw', name: 'CH2: OUT_SW', color: '#a855f7' },
      { id: 'clk', name: 'CH3: CLK', color: '#facc15' },
      { id: 'S0', name: 'CH4: S0 (LSB)', color: '#22c55e' },
      { id: 'S1', name: 'CH5: S1', color: '#10b981' },
      { id: 'S2', name: 'CH6: S2 (MSB)', color: '#059669' },
      { id: 'full', name: 'CH7: FULL', color: '#ef4444' },
      { id: 'entryGateOpen', name: 'CH8: ENTRY_GATE', color: '#ec4899' }
    ];

    // Bind controls
    const btnPause = document.getElementById('btnWavePause');
    const btnClear = document.getElementById('btnWaveClear');
    if (btnPause) {
      btnPause.addEventListener('click', () => {
        this.paused = !this.paused;
        btnPause.textContent = this.paused ? 'Resume Trace' : 'Pause Trace';
      });
    }
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        this.history = [];
      });
    }

    this.startSampling();
    this.startRender();
  }

  startSampling() {
    setInterval(() => {
      if (this.paused) return;

      const s = window.simState || {
        inRaw: 0, outRaw: 0, pulseDn: 0, pulseUp: 0,
        S0: 1, S1: 1, S2: 1, full: 0, entryGateOpen: 0
      };

      const sample = {
        inRaw: s.inRaw ? 1 : 0,
        outRaw: s.outRaw ? 1 : 0,
        clk: (s.pulseDn || s.pulseUp) ? 1 : 0,
        S0: s.S0 ? 1 : 0,
        S1: s.S1 ? 1 : 0,
        S2: s.S2 ? 1 : 0,
        full: s.full ? 1 : 0,
        entryGateOpen: s.entryGateOpen ? 1 : 0
      };

      this.history.push(sample);
      if (this.history.length > this.maxSamples) {
        this.history.shift();
      }
    }, 40); // 25 Hz sampling
  }

  startRender() {
    this.render();
    requestAnimationFrame(() => this.startRender());
  }

  render() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Dark grid background
    ctx.fillStyle = '#020617';
    ctx.fillRect(0, 0, w, h);

    // Channel lane height & dividers
    const laneHeight = h / this.channels.length;

    this.channels.forEach((ch, idx) => {
      const yBase = (idx + 1) * laneHeight;
      const yHigh = yBase - laneHeight * 0.75;
      const yLow = yBase - laneHeight * 0.15;

      // Lane divider line
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, yBase);
      ctx.lineTo(w, yBase);
      ctx.stroke();

      // Channel name tag
      ctx.font = 'bold 9px Fira Code';
      ctx.fillStyle = ch.color;
      ctx.fillText(ch.name, 10, yHigh + 10);

      // Draw digital trace
      if (this.history.length > 1) {
        const stepX = (w - 140) / this.maxSamples;
        ctx.strokeStyle = ch.color;
        ctx.lineWidth = 2;
        ctx.beginPath();

        for (let i = 0; i < this.history.length; i++) {
          const sample = this.history[i];
          const val = sample[ch.id];
          const px = 130 + i * stepX;
          const py = val === 1 ? yHigh : yLow;

          if (i === 0) {
            ctx.moveTo(px, py);
          } else {
            const prevVal = this.history[i - 1][ch.id];
            const prevY = prevVal === 1 ? yHigh : yLow;
            if (val !== prevVal) {
              // Vertical transition edge
              ctx.lineTo(px, prevY);
              ctx.lineTo(px, py);
            } else {
              ctx.lineTo(px, py);
            }
          }
        }
        ctx.stroke();
      }
    });

    // Vertical time cursor
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(w - 1, 0);
    ctx.lineTo(w - 1, h);
    ctx.stroke();
    ctx.setLineDash([]);
  }
}

window.WaveformView = WaveformView;
