// ==========================================================================
// Smart Parking Garage Controller - Core Logic Engine & Coordinator
// Computer Organization & Architecture Project Simulation
// ==========================================================================

class GarageSimulationController {
  constructor() {
    // 3-Bit State Register (S2 = MSB, S0 = LSB)
    // Initialized to 111_2 (7 available spaces = empty garage)
    this.state = {
      S2: 1,
      S1: 1,
      S0: 1,
      availableSpaces: 7,

      // Raw Input Signals from virtual switches
      inRaw: 0,
      outRaw: 0,
      emerg: 0,
      resetRaw: 0,

      // Filtered Internal Clock Pulses
      pulseDn: 0,
      pulseUp: 0,

      // Status Flags
      full: 0,
      empty: 1,

      // Actuator Outputs
      entryGateOpen: 0,
      exitGateOpen: 0,

      // 7-Segment Display Segments [a, b, c, d, e, f, g]
      segments: [1, 1, 1, 0, 0, 0, 0] // 7
    };

    window.simState = this.state;
    window.simController = this;

    // CD4511 BCD to 7-Segment Truth Table for digits 0 to 7
    this.cd4511Table = {
      0: [1, 1, 1, 1, 1, 1, 0],
      1: [0, 1, 1, 0, 0, 0, 0],
      2: [1, 1, 0, 1, 1, 0, 1],
      3: [1, 1, 1, 1, 0, 0, 1],
      4: [0, 1, 1, 0, 0, 1, 1],
      5: [1, 0, 1, 1, 0, 1, 1],
      6: [1, 0, 1, 1, 1, 1, 1],
      7: [1, 1, 1, 0, 0, 0, 0]
    };

    // Auto traffic generator timer
    this.autoTrafficInterval = null;

    // Initialize Views
    this.initViews();
    this.bindDOMControls();
    this.initTabs();
    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  initViews() {
    // Instantiate sub-components
    this.garageView = new GarageView('garageCanvas');
    this.breadboardView = new BreadboardView('breadboardCanvas');
    this.schematicView = new SchematicView('schematicCanvas');
    this.fsmView = new FSMView('fsmCanvas');
    this.waveformView = new WaveformView('waveformCanvas');
    this.testSuite = new TestSuite();
  }

  // --- DIGITAL LOGIC EVALUATION ENGINE ---
  evaluateCombinationalLogic() {
    const s = this.state;

    // 1. Calculate Decimal Count from Register: Value = 4*S2 + 2*S1 + S0
    s.availableSpaces = (s.S2 << 2) | (s.S1 << 1) | s.S0;

    // 2. Status Detectors
    // FULL Flag (Zero Detect: S2=0 & S1=0 & S0=0)
    s.full = (!s.S2 && !s.S1 && !s.S0) ? 1 : 0;

    // EMPTY Flag (Max Detect: S2=1 & S1=1 & S0=1)
    s.empty = (s.S2 && s.S1 && s.S0) ? 1 : 0;

    // 3. Gate Actuators
    // Entry Gate Opens if: EMERGENCY OR (Car arrives at Entry AND NOT FULL)
    s.entryGateOpen = (s.emerg || (s.inRaw && !s.full)) ? 1 : 0;

    // Exit Gate Opens if: EMERGENCY OR (Car arrives at Exit AND NOT EMPTY)
    s.exitGateOpen = (s.emerg || (s.outRaw && !s.empty)) ? 1 : 0;

    // 4. Inhibit & Simultaneous Event Filtering Logic
    // If both IN and OUT are pressed simultaneously: net change = 0 (suppress both clock pulses)
    if (s.inRaw && s.outRaw) {
      s.pulseDn = 0;
      s.pulseUp = 0;
    } else {
      s.pulseDn = (s.inRaw && !s.full && !s.emerg) ? 1 : 0;
      s.pulseUp = (s.outRaw && !s.empty && !s.emerg) ? 1 : 0;
    }

    // 5. CD4511 BCD-to-7-Segment Decoding
    s.segments = this.cd4511Table[s.availableSpaces] || [0, 0, 0, 0, 0, 0, 0];

    // Synchronize physical parking spots with occupancy
    const occupiedCount = 7 - s.availableSpaces;
    this.garageView.syncOccupancy(occupiedCount);
  }

  // --- SYNCHRONOUS REGISTER CLOCK TRANSITION ---
  clockStep(direction) {
    // direction: 0 = Down (Entry), 1 = Up (Exit)
    const s = this.state;
    const q0 = s.S0;
    const q1 = s.S1;
    const q2 = s.S2;

    // Toggle logic for Synchronous Up/Down Counter
    // T0 is always 1 (toggles every valid clock)
    const t0 = 1;

    // T1 toggles when: (UP & Q0) OR (DOWN & ~Q0)
    const t1 = (direction === 1) ? q0 : (!q0 ? 1 : 0);

    // T2 toggles when: (UP & Q1 & Q0) OR (DOWN & ~Q1 & ~Q0)
    const t2 = (direction === 1) ? (q1 && q0 ? 1 : 0) : (!q1 && !q0 ? 1 : 0);

    // Next D values for 74HC74: D = Q XOR T
    s.S0 = q0 ^ t0;
    s.S1 = q1 ^ t1;
    s.S2 = q2 ^ t2;

    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  // --- USER HARDWARE ACTIONS ---
  async pulseEntry() {
    if (this.state.emerg) {
      window.soundFX.playGateOpen();
      return;
    }
    if (this.state.full) {
      window.soundFX.playFullAlert();
      this.flashTotemFull();
      return;
    }

    this.state.inRaw = 1;
    this.evaluateCombinationalLogic();
    this.updateUI();

    window.soundFX.playGateOpen();
    this.garageView.spawnEnteringCar();

    // Clock falling edge after sensor trigger duration
    await this.sleep(120);
    if (this.state.pulseDn) {
      this.clockStep(0); // Count Down
      window.soundFX.playClick();
    }

    await this.sleep(180);
    this.state.inRaw = 0;
    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  async pulseExit() {
    if (this.state.emerg) {
      window.soundFX.playGateOpen();
      return;
    }
    if (this.state.empty) {
      window.soundFX.playClick();
      return;
    }

    this.state.outRaw = 1;
    this.evaluateCombinationalLogic();
    this.updateUI();

    window.soundFX.playGateOpen();
    this.garageView.spawnExitingCar();

    await this.sleep(120);
    if (this.state.pulseUp) {
      this.clockStep(1); // Count Up
      window.soundFX.playClick();
    }

    await this.sleep(180);
    this.state.outRaw = 0;
    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  async pulseSimultaneous() {
    this.state.inRaw = 1;
    this.state.outRaw = 1;
    this.evaluateCombinationalLogic();
    this.updateUI();

    window.soundFX.playGateOpen();
    if (!this.state.full) this.garageView.spawnEnteringCar();
    if (!this.state.empty) this.garageView.spawnExitingCar();

    await this.sleep(250);
    this.state.inRaw = 0;
    this.state.outRaw = 0;
    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  resetSystem() {
    // Asynchronous active-low preset to 111_2 (7 spaces = Empty)
    this.state.S2 = 1;
    this.state.S1 = 1;
    this.state.S0 = 1;
    this.state.inRaw = 0;
    this.state.outRaw = 0;
    this.state.emerg = 0;

    const swEmg = document.getElementById('switchEmergency');
    if (swEmg) swEmg.checked = false;

    window.soundFX.playChime();
    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  setEmergency(active) {
    this.state.emerg = active ? 1 : 0;
    if (active) {
      window.soundFX.playFullAlert();
    } else {
      window.soundFX.playClick();
    }
    this.evaluateCombinationalLogic();
    this.updateUI();
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  flashTotemFull() {
    const banner = document.getElementById('totemBanner');
    if (banner) {
      banner.textContent = 'FULL - NO ENTRY';
      banner.className = 'totem-banner full';
      setTimeout(() => {
        if (!this.state.full) {
          banner.textContent = 'WELCOME';
          banner.className = 'totem-banner';
        }
      }, 1500);
    }
  }

  // --- UI SYNCHRONIZATION ---
  updateUI() {
    const s = this.state;

    // Header updates
    const hCount = document.getElementById('headerSpacesCount');
    if (hCount) hCount.textContent = s.availableSpaces;

    const hStatusPill = document.getElementById('headerStatusPill');
    const hStatusText = document.getElementById('headerStatusText');
    const dot = hStatusPill ? hStatusPill.querySelector('.indicator-dot') : null;

    if (s.emerg) {
      if (hStatusText) hStatusText.textContent = 'EMERGENCY OVERRIDE';
      if (dot) dot.className = 'indicator-dot amber';
    } else if (s.full) {
      if (hStatusText) hStatusText.textContent = 'GARAGE FULL';
      if (dot) dot.className = 'indicator-dot red';
    } else {
      if (hStatusText) hStatusText.textContent = 'OPERATIONAL';
      if (dot) dot.className = 'indicator-dot green';
    }

    // Register Bits Display (FF2, FF1, FF0)
    const valS2 = document.getElementById('valS2');
    const valS1 = document.getElementById('valS1');
    const valS0 = document.getElementById('valS0');
    if (valS2) valS2.textContent = s.S2;
    if (valS1) valS1.textContent = s.S1;
    if (valS0) valS0.textContent = s.S0;

    const q2 = document.getElementById('q2Val');
    const q1 = document.getElementById('q1Val');
    const q0 = document.getElementById('q0Val');
    if (q2) q2.textContent = s.S2;
    if (q1) q1.textContent = s.S1;
    if (q0) q0.textContent = s.S0;

    const qb2 = document.getElementById('qbar2Val');
    const qb1 = document.getElementById('qbar1Val');
    const qb0 = document.getElementById('qbar0Val');
    if (qb2) qb2.textContent = s.S2 ? 0 : 1;
    if (qb1) qb1.textContent = s.S1 ? 0 : 1;
    if (qb0) qb0.textContent = s.S0 ? 0 : 1;

    // Flip-flop card active borders
    const ff0Block = document.getElementById('ff0Block');
    const ff1Block = document.getElementById('ff1Block');
    const ff2Block = document.getElementById('ff2Block');
    if (ff0Block) ff0Block.className = s.S0 ? 'flipflop-block active' : 'flipflop-block';
    if (ff1Block) ff1Block.className = s.S1 ? 'flipflop-block active' : 'flipflop-block';
    if (ff2Block) ff2Block.className = s.S2 ? 'flipflop-block active' : 'flipflop-block';

    // Metrics
    const binVal = document.getElementById('binaryStateVal');
    if (binVal) binVal.textContent = `${s.S2}${s.S1}${s.S0}₂`;

    const decVal = document.getElementById('decimalCountVal');
    if (decVal) decVal.textContent = s.availableSpaces;

    const occVal = document.getElementById('occupancyVal');
    if (occVal) occVal.textContent = `${7 - s.availableSpaces} / 7`;

    // LED Indicators (Entry Gate, Exit Gate, Full, Empty)
    const ledEntry = document.getElementById('ledEntryGate');
    const txtEntry = document.getElementById('txtEntryGate');
    if (ledEntry && txtEntry) {
      if (s.entryGateOpen) {
        ledEntry.className = 'led-indicator active-green';
        txtEntry.textContent = 'OPEN (GREEN / PASS)';
        txtEntry.style.color = '#22c55e';
      } else {
        ledEntry.className = s.full ? 'led-indicator active-red' : 'led-indicator';
        txtEntry.textContent = s.full ? 'FULL / LOCKED (RED)' : 'LOCKED (IDLE)';
        txtEntry.style.color = s.full ? '#ef4444' : '#94a3b8';
      }
    }

    const ledExit = document.getElementById('ledExitGate');
    const txtExit = document.getElementById('txtExitGate');
    if (ledExit && txtExit) {
      if (s.exitGateOpen) {
        ledExit.className = 'led-indicator active-green';
        txtExit.textContent = 'OPEN (GREEN / PASS)';
        txtExit.style.color = '#22c55e';
      } else {
        ledExit.className = 'led-indicator';
        txtExit.textContent = 'CLOSED (IDLE)';
        txtExit.style.color = '#94a3b8';
      }
    }

    const ledFull = document.getElementById('ledFullFlag');
    const txtFull = document.getElementById('txtFullFlag');
    if (ledFull && txtFull) {
      ledFull.className = s.full ? 'led-indicator red active' : 'led-indicator';
      txtFull.textContent = s.full ? 'HIGH (GARAGE FULL)' : 'LOW (Spaces Available)';
      txtFull.style.color = s.full ? '#ef4444' : '#94a3b8';
    }

    const ledEmpty = document.getElementById('ledEmptyFlag');
    const txtEmpty = document.getElementById('txtEmptyFlag');
    if (ledEmpty && txtEmpty) {
      ledEmpty.className = s.empty ? 'led-indicator green active' : 'led-indicator';
      txtEmpty.textContent = s.empty ? 'HIGH (All 7 Empty)' : 'LOW (Cars Present)';
      txtEmpty.style.color = s.empty ? '#10b981' : '#94a3b8';
    }

    // Physical 7-Segment Totem Display (CSS segments a-g)
    const segEls = document.querySelectorAll('#mainSevenSegment .seg');
    if (segEls.length === 7) {
      ['a', 'b', 'c', 'd', 'e', 'f', 'g'].forEach((segName, idx) => {
        const el = document.querySelector(`#mainSevenSegment .seg-${segName}`);
        if (el) {
          if (s.segments[idx]) {
            el.classList.add('on');
          } else {
            el.classList.remove('on');
          }
        }
      });
    }

    // Totem Banner text
    const banner = document.getElementById('totemBanner');
    if (banner) {
      if (s.emerg) {
        banner.textContent = 'EVACUATE';
        banner.className = 'totem-banner emergency';
      } else if (s.full) {
        banner.textContent = 'FULL';
        banner.className = 'totem-banner full';
      } else {
        banner.textContent = 'WELCOME';
        banner.className = 'totem-banner';
      }
    }

    // Telemetry items
    const telePulseDn = document.getElementById('telePulseDn');
    if (telePulseDn) telePulseDn.textContent = s.pulseDn ? '1 (HIGH / COUNT -1)' : '0 (LOW)';

    const telePulseUp = document.getElementById('telePulseUp');
    if (telePulseUp) telePulseUp.textContent = s.pulseUp ? '1 (HIGH / COUNT +1)' : '0 (LOW)';
  }

  // --- CONTROLS & EVENT BINDINGS ---
  bindDOMControls() {
    const btnIn = document.getElementById('btnCarIn');
    const btnOut = document.getElementById('btnCarOut');
    const btnSim = document.getElementById('btnSimultaneous');
    const btnReset = document.getElementById('btnReset');
    const swEmg = document.getElementById('switchEmergency');
    const btnAuto = document.getElementById('btnAutoTraffic');
    const btnClearGarage = document.getElementById('btnClearGarage');
    const soundToggle = document.getElementById('soundToggleBtn');

    if (btnIn) btnIn.addEventListener('click', () => this.pulseEntry());
    if (btnOut) btnOut.addEventListener('click', () => this.pulseExit());
    if (btnSim) btnSim.addEventListener('click', () => this.pulseSimultaneous());
    if (btnReset) btnReset.addEventListener('click', () => this.resetSystem());
    if (swEmg) swEmg.addEventListener('change', (e) => this.setEmergency(e.target.checked));

    if (btnClearGarage) {
      btnClearGarage.addEventListener('click', () => this.resetSystem());
    }

    if (btnAuto) {
      btnAuto.addEventListener('click', () => {
        if (this.autoTrafficInterval) {
          clearInterval(this.autoTrafficInterval);
          this.autoTrafficInterval = null;
          btnAuto.classList.remove('btn-primary');
          btnAuto.classList.add('btn-outline');
          btnAuto.innerHTML = '<span class="play-icon">▶</span> Auto-Traffic Simulation';
        } else {
          btnAuto.classList.remove('btn-outline');
          btnAuto.classList.add('btn-primary');
          btnAuto.innerHTML = '<span class="play-icon">⏸</span> Stop Auto-Traffic';
          this.autoTrafficInterval = setInterval(() => {
            if (this.state.emerg) return;
            // Randomly choose entry or exit based on current occupancy
            const available = this.state.availableSpaces;
            if (available === 7) {
              this.pulseEntry();
            } else if (available === 0) {
              this.pulseExit();
            } else {
              if (Math.random() > 0.45) {
                this.pulseEntry();
              } else {
                this.pulseExit();
              }
            }
          }, 1800);
        }
      });
    }

    if (soundToggle) {
      soundToggle.addEventListener('click', () => {
        window.soundFX.enabled = !window.soundFX.enabled;
        soundToggle.style.opacity = window.soundFX.enabled ? '1' : '0.4';
      });
    }

    // Keyboard Shortcuts (I = Car In, O = Car Out, R = Reset, E = Emergency)
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return;
      if (e.key === 'i' || e.key === 'I') this.pulseEntry();
      if (e.key === 'o' || e.key === 'O') this.pulseExit();
      if (e.key === 'r' || e.key === 'R') this.resetSystem();
      if (e.key === 'e' || e.key === 'E') {
        if (swEmg) {
          swEmg.checked = !swEmg.checked;
          this.setEmergency(swEmg.checked);
        }
      }
    });
  }

  // --- TAB NAVIGATION ---
  initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-tab');

        tabBtns.forEach(b => b.classList.remove('active'));
        tabPanes.forEach(p => p.classList.remove('active'));

        btn.classList.add('active');
        const targetPane = document.getElementById(targetId);
        if (targetPane) targetPane.classList.add('active');
      });
    });
  }
}

// Start simulation on DOM load
window.addEventListener('DOMContentLoaded', () => {
  new GarageSimulationController();
});
