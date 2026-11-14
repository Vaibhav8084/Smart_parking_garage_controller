// FSM State Transition Graph and Dynamic Table Synchronizer
class FSMView {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');

    // 8 states: 0 to 7 arranged along a circular / racetrack layout
    this.states = [];
    const cx = this.canvas.width / 2;
    const cy = this.canvas.height / 2;
    const rx = 180;
    const ry = 130;

    for (let i = 0; i < 8; i++) {
      // Position around ellipse
      const angle = (i / 8) * Math.PI * 2 - Math.PI / 2;
      this.states.push({
        val: i,
        bin: i.toString(2).padStart(3, '0'),
        x: cx + Math.cos(angle) * rx,
        y: cy + Math.sin(angle) * ry
      });
    }

    this.startLoop();
  }

  startLoop() {
    this.render();
    this.updateTableHighlight();
    requestAnimationFrame(() => this.startLoop());
  }

  updateTableHighlight() {
    const currentState = window.simState ? window.simState.availableSpaces : 7;
    const rows = document.querySelectorAll('#stateTable tbody tr');
    rows.forEach(row => {
      const stateVal = parseInt(row.getAttribute('data-state'));
      if (stateVal === currentState) {
        row.classList.add('active-state');
      } else {
        row.classList.remove('active-state');
      }
    });
  }

  render() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    const currState = window.simState ? window.simState.availableSpaces : 7;

    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, w, h);

    // Draw transition arcs between adjacent states
    for (let i = 0; i < 8; i++) {
      const from = this.states[i];
      const nextUp = this.states[(i + 1) % 8];

      // Draw transition lines
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(nextUp.x, nextUp.y);
      ctx.stroke();
    }

    // Draw State Nodes
    this.states.forEach(st => {
      const isActive = (st.val === currState);

      // Node Circle
      ctx.fillStyle = isActive ? '#0284c7' : '#151d2e';
      ctx.strokeStyle = isActive ? '#38bdf8' : (st.val === 0 ? '#ef4444' : st.val === 7 ? '#10b981' : '#334155');
      ctx.lineWidth = isActive ? 3 : 2;

      ctx.beginPath();
      ctx.arc(st.x, st.y, 22, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      if (isActive) {
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 15;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // State Text
      ctx.fillStyle = isActive ? '#fff' : '#f8fafc';
      ctx.font = 'bold 12px Fira Code';
      ctx.textAlign = 'center';
      ctx.fillText(st.bin, st.x, st.y - 1);

      ctx.font = '9px Inter';
      ctx.fillStyle = isActive ? '#e0f2fe' : '#94a3b8';
      ctx.fillText(`(${st.val})`, st.x, st.y + 12);
      ctx.textAlign = 'left';

      // Special labels for FULL and EMPTY
      if (st.val === 0) {
        ctx.font = 'bold 8px Fira Code';
        ctx.fillStyle = '#ef4444';
        ctx.fillText('FULL (000)', st.x - 22, st.y + 34);
      } else if (st.val === 7) {
        ctx.font = 'bold 8px Fira Code';
        ctx.fillStyle = '#10b981';
        ctx.fillText('EMPTY (111)', st.x - 24, st.y - 28);
      }
    });
  }
}

window.FSMView = FSMView;
