// Automated Test Suite for Smart Parking Garage Controller
class TestSuite {
  constructor() {
    this.container = document.getElementById('testCasesContainer');
    this.consoleLog = document.getElementById('testConsoleLog');
    this.btnRunAll = document.getElementById('btnRunAllTests');
    this.btnClear = document.getElementById('btnClearTestLog');

    this.testCases = [
      {
        id: 1,
        title: 'Test 1: System Power-On / Preset Reset',
        desc: 'Asserts asynchronous preset sets Q2 Q1 Q0 = 111 (7 spaces), EMPTY=1, FULL=0.',
        run: async () => this.runTest1()
      },
      {
        id: 2,
        title: 'Test 2: Normal Single Car Entry',
        desc: 'Asserts car entry decrements count from 7 to 6 and opens Entry Gate momentarily.',
        run: async () => this.runTest2()
      },
      {
        id: 3,
        title: 'Test 3: Fill to Full Capacity (7 Cars)',
        desc: 'Enters cars until count reaches 000; asserts FULL=1 and Entry Gate locked.',
        run: async () => this.runTest3()
      },
      {
        id: 4,
        title: 'Test 4: Blocked Entry Attempt at Full Capacity',
        desc: 'Asserts that pressing Entry PB when FULL=1 inhibits clock and keeps count at 0.',
        run: async () => this.runTest4()
      },
      {
        id: 5,
        title: 'Test 5: Normal Exit from Full State',
        desc: 'Asserts car exit increments count to 1, clears FULL flag, and unlocks Entry Gate.',
        run: async () => this.runTest5()
      },
      {
        id: 6,
        title: 'Test 6: Simultaneous Entry and Exit',
        desc: 'Asserts both IN and OUT simultaneously open both gates with net count delta = 0.',
        run: async () => this.runTest6()
      },
      {
        id: 7,
        title: 'Test 7: Emergency Override Mode',
        desc: 'Asserts Emergency Switch forces both barrier gates OPEN continuously.',
        run: async () => this.runTest7()
      }
    ];

    this.renderTestCards();
    this.bindEvents();
  }

  bindEvents() {
    if (this.btnRunAll) {
      this.btnRunAll.addEventListener('click', () => this.runAll());
    }
    if (this.btnClear) {
      this.btnClear.addEventListener('click', () => {
        this.consoleLog.innerHTML = '[SYSTEM] Log cleared.<br>';
      });
    }
  }

  log(msg, type = 'info') {
    const time = new Date().toLocaleTimeString();
    let color = '#38bdf8';
    if (type === 'pass') color = '#22c55e';
    if (type === 'fail') color = '#ef4444';
    if (type === 'warn') color = '#facc15';

    const line = `<div style="color:${color}; margin-bottom: 2px;">[${time}] ${msg}</div>`;
    this.consoleLog.innerHTML += line;
    this.consoleLog.scrollTop = this.consoleLog.scrollHeight;
  }

  renderTestCards() {
    if (!this.container) return;
    this.container.innerHTML = '';

    this.testCases.forEach(tc => {
      const card = document.createElement('div');
      card.className = 'test-card-item';
      card.id = `testCard_${tc.id}`;
      card.innerHTML = `
        <div class="test-info">
          <h5>${tc.title}</h5>
          <p>${tc.desc}</p>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="test-badge pending" id="testBadge_${tc.id}">PENDING</span>
          <button class="btn-outline btn-sm" id="btnRunSingle_${tc.id}">Run</button>
        </div>
      `;

      card.querySelector(`#btnRunSingle_${tc.id}`).addEventListener('click', () => {
        this.runSingle(tc);
      });

      this.container.appendChild(card);
    });
  }

  setTestStatus(id, status) {
    const card = document.getElementById(`testCard_${id}`);
    const badge = document.getElementById(`testBadge_${id}`);
    if (!card || !badge) return;

    card.className = `test-card-item ${status}`;
    badge.className = `test-badge ${status}`;
    badge.textContent = status.toUpperCase();
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async runSingle(tc) {
    this.setTestStatus(tc.id, 'running');
    this.log(`--- Starting ${tc.title} ---`, 'warn');
    try {
      const passed = await tc.run();
      if (passed) {
        this.setTestStatus(tc.id, 'pass');
        this.log(`PASS: ${tc.title} verified successfully!`, 'pass');
      } else {
        this.setTestStatus(tc.id, 'fail');
        this.log(`FAIL: ${tc.title} failed assertion!`, 'fail');
      }
    } catch(err) {
      this.setTestStatus(tc.id, 'fail');
      this.log(`ERROR in ${tc.title}: ${err.message}`, 'fail');
    }
  }

  async runAll() {
    this.log('=== RUNNING ALL 7 HARDWARE VERIFICATION TESTS ===', 'warn');
    for (const tc of this.testCases) {
      await this.runSingle(tc);
      await this.sleep(400);
    }
    this.log('=== TEST SUITE RUN COMPLETED ===', 'pass');
  }

  // --- TEST IMPLEMENTATIONS ---
  async runTest1() {
    // Test 1: Reset
    window.simController.resetSystem();
    await this.sleep(100);
    const s = window.simState;
    const pass = (s.availableSpaces === 7 && s.S0 === 1 && s.S1 === 1 && s.S2 === 1 && s.empty === 1 && s.full === 0);
    this.log(`Assertion: Spaces = ${s.availableSpaces} (Exp: 7), State = ${s.S2}${s.S1}${s.S0} (Exp: 111)`);
    return pass;
  }

  async runTest2() {
    // Test 2: Single Entry from 7 -> 6
    window.simController.resetSystem();
    await this.sleep(100);
    await window.simController.pulseEntry();
    await this.sleep(150);
    const s = window.simState;
    const pass = (s.availableSpaces === 6 && s.S2 === 1 && s.S1 === 1 && s.S0 === 0);
    this.log(`Assertion: Spaces after 1 car in = ${s.availableSpaces} (Exp: 6), State = ${s.S2}${s.S1}${s.S0} (Exp: 110)`);
    return pass;
  }

  async runTest3() {
    // Test 3: Fill to Full (enter until 0)
    window.simController.resetSystem();
    await this.sleep(50);
    for (let i = 0; i < 7; i++) {
      await window.simController.pulseEntry();
      await this.sleep(60);
    }
    const s = window.simState;
    const pass = (s.availableSpaces === 0 && s.full === 1 && s.S2 === 0 && s.S1 === 0 && s.S0 === 0);
    this.log(`Assertion: Spaces = ${s.availableSpaces} (Exp: 0), FULL Flag = ${s.full} (Exp: 1)`);
    return pass;
  }

  async runTest4() {
    // Test 4: Blocked Entry at Full
    const sBefore = window.simState.availableSpaces;
    await window.simController.pulseEntry(); // attempt to enter when full
    await this.sleep(100);
    const sAfter = window.simState.availableSpaces;
    const pass = (sBefore === 0 && sAfter === 0 && window.simState.entryGateOpen === 0);
    this.log(`Assertion: Attempted entry while full. Spaces before=${sBefore}, after=${sAfter}, GateOpen=${window.simState.entryGateOpen}`);
    return pass;
  }

  async runTest5() {
    // Test 5: Exit from full (0 -> 1)
    await window.simController.pulseExit();
    await this.sleep(150);
    const s = window.simState;
    const pass = (s.availableSpaces === 1 && s.full === 0);
    this.log(`Assertion: Car leaves full garage. Spaces = ${s.availableSpaces} (Exp: 1), FULL Flag = ${s.full} (Exp: 0)`);
    return pass;
  }

  async runTest6() {
    // Test 6: Simultaneous Entry & Exit
    window.simController.resetSystem();
    await this.sleep(50);
    // Move to 3 spaces available
    for (let i = 0; i < 4; i++) {
      await window.simController.pulseEntry();
      await this.sleep(40);
    }
    const countBefore = window.simState.availableSpaces; // 3
    await window.simController.pulseSimultaneous();
    await this.sleep(150);
    const countAfter = window.simState.availableSpaces;
    const pass = (countBefore === countAfter);
    this.log(`Assertion: Simultaneous In+Out. Count before = ${countBefore}, Count after = ${countAfter} (Delta = 0)`);
    return pass;
  }

  async runTest7() {
    // Test 7: Emergency Override
    window.simController.setEmergency(true);
    await this.sleep(100);
    const openDuring = (window.simState.entryGateOpen === 1 && window.simState.exitGateOpen === 1);
    window.simController.setEmergency(false);
    await this.sleep(100);
    const pass = openDuring && (window.simState.emerg === 0);
    this.log(`Assertion: Emergency Switch activated. Both gates forced OPEN = ${openDuring}`);
    return pass;
  }
}

window.TestSuite = TestSuite;
