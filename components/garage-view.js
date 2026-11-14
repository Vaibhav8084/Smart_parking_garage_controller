// Garage Canvas View: Physical Parking Garage Animation & Gates
class GarageView {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    
    // Physical state
    this.totalSpots = 7;
    this.spots = [
      { id: 1, x: 260, y: 70, w: 90, h: 140, occupied: false, carColor: null },
      { id: 2, x: 370, y: 70, w: 90, h: 140, occupied: false, carColor: null },
      { id: 3, x: 480, y: 70, w: 90, h: 140, occupied: false, carColor: null },
      { id: 4, x: 590, y: 70, w: 90, h: 140, occupied: false, carColor: null },
      { id: 5, x: 300, y: 270, w: 90, h: 140, occupied: false, carColor: null },
      { id: 6, x: 440, y: 270, w: 90, h: 140, occupied: false, carColor: null },
      { id: 7, x: 580, y: 270, w: 90, h: 140, occupied: false, carColor: null }
    ];

    this.carColors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4'];

    // Animated cars in transit
    this.movingCars = [];

    // Gate angles (0 = down / closed, 1 = up / open)
    this.entryGateAngle = 0;
    this.exitGateAngle = 0;

    // Start render loop
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  syncOccupancy(occupiedCount) {
    // Synchronize number of parked cars with logical occupancy count (7 - available)
    let currentOccupied = this.spots.filter(s => s.occupied).length;
    
    if (occupiedCount > currentOccupied) {
      // Need to add cars to empty spots
      const needed = occupiedCount - currentOccupied;
      let added = 0;
      for (let spot of this.spots) {
        if (!spot.occupied && added < needed) {
          spot.occupied = true;
          spot.carColor = this.carColors[spot.id % this.carColors.length];
          added++;
        }
      }
    } else if (occupiedCount < currentOccupied) {
      // Need to remove cars
      const toRemove = currentOccupied - occupiedCount;
      let removed = 0;
      for (let i = this.spots.length - 1; i >= 0; i--) {
        if (this.spots[i].occupied && removed < toRemove) {
          this.spots[i].occupied = false;
          this.spots[i].carColor = null;
          removed++;
        }
      }
    }
  }

  spawnEnteringCar() {
    // Animate a car driving through entry gate into an available spot
    const emptySpot = this.spots.find(s => !s.occupied && !s.reserved);
    if (!emptySpot) return;

    emptySpot.reserved = true;
    const color = this.carColors[Math.floor(Math.random() * this.carColors.length)];

    this.movingCars.push({
      x: 30,
      y: 140,
      targetX: emptySpot.x + 20,
      targetY: emptySpot.y + 20,
      stage: 'approach_entry',
      color: color,
      targetSpot: emptySpot,
      speed: 3
    });
  }

  spawnExitingCar() {
    // Find an occupied spot to leave
    const occupiedSpot = this.spots.slice().reverse().find(s => s.occupied && !s.leaving);
    if (!occupiedSpot) return;

    occupiedSpot.leaving = true;
    const color = occupiedSpot.carColor || '#3b82f6';

    this.movingCars.push({
      x: occupiedSpot.x + 20,
      y: occupiedSpot.y + 20,
      stage: 'leave_spot',
      color: color,
      originSpot: occupiedSpot,
      speed: 3
    });
  }

  animate() {
    this.update();
    this.draw();
    requestAnimationFrame(this.animate);
  }

  update() {
    // Smooth gate arm angle transitions
    const entryTarget = window.simState && window.simState.entryGateOpen ? 1 : 0;
    const exitTarget = window.simState && window.simState.exitGateOpen ? 1 : 0;

    this.entryGateAngle += (entryTarget - this.entryGateAngle) * 0.15;
    this.exitGateAngle += (exitTarget - this.exitGateAngle) * 0.15;

    // Update telemetry elements if present
    const tEntry = document.getElementById('teleEntryGate');
    const tExit = document.getElementById('teleExitGate');
    if (tEntry) {
      const deg = Math.round(this.entryGateAngle * 90);
      tEntry.textContent = deg > 15 ? `OPEN (${deg}°) [PASS]` : `DOWN (${deg}°) [LOCKED]`;
      tEntry.style.color = deg > 15 ? '#10b981' : '#94a3b8';
    }
    if (tExit) {
      const deg = Math.round(this.exitGateAngle * 90);
      tExit.textContent = deg > 15 ? `OPEN (${deg}°) [PASS]` : `DOWN (${deg}°) [LOCKED]`;
      tExit.style.color = deg > 15 ? '#10b981' : '#94a3b8';
    }

    // Update moving cars
    for (let i = this.movingCars.length - 1; i >= 0; i--) {
      const car = this.movingCars[i];

      if (car.stage === 'approach_entry') {
        // Move towards entry gate barrier
        if (car.x < 120) {
          car.x += car.speed;
        } else {
          // Wait for gate to open
          if (this.entryGateAngle > 0.6) {
            car.stage = 'drive_to_spot';
          }
        }
      } else if (car.stage === 'drive_to_spot') {
        car.x += (car.targetX - car.x) * 0.05;
        car.y += (car.targetY - car.y) * 0.05;

        if (Math.abs(car.x - car.targetX) < 3 && Math.abs(car.y - car.targetY) < 3) {
          // Car has parked
          car.targetSpot.occupied = true;
          car.targetSpot.reserved = false;
          car.targetSpot.carColor = car.color;
          this.movingCars.splice(i, 1);
        }
      } else if (car.stage === 'leave_spot') {
        // Back out into drive aisle
        car.y += 1.5;
        if (car.y >= 210) {
          car.originSpot.occupied = false;
          car.originSpot.leaving = false;
          car.originSpot.carColor = null;
          car.stage = 'drive_to_exit';
        }
      } else if (car.stage === 'drive_to_exit') {
        // Drive towards exit gate at x=140, y=360
        car.x += (120 - car.x) * 0.04;
        car.y += (360 - car.y) * 0.04;

        if (car.x < 135) {
          if (this.exitGateAngle > 0.6) {
            car.stage = 'exit_out';
          }
        }
      } else if (car.stage === 'exit_out') {
        car.x -= car.speed;
        if (car.x < -60) {
          this.movingCars.splice(i, 1);
        }
      }
    }
  }

  draw() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Background asphalt
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);

    // Driving lanes
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 110, w, 140); // Central transit aisle
    ctx.fillRect(0, 310, 220, 110); // Exit approach

    // Road markings & dashed centerlines
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 2;
    ctx.setLineDash([12, 12]);
    ctx.beginPath();
    ctx.moveTo(0, 180);
    ctx.lineTo(w, 180);
    ctx.stroke();
    ctx.setLineDash([]);

    // Entry & Exit lane signs on pavement
    ctx.font = 'bold 12px Fira Code';
    ctx.fillStyle = '#38bdf8';
    ctx.fillText('➔ ENTRY LANE', 25, 175);
    ctx.fillStyle = '#a855f7';
    ctx.fillText('➔ EXIT LANE', 25, 375);

    // Draw Parking Spots
    this.spots.forEach(spot => {
      // Spot boundary lines
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 3;
      ctx.strokeRect(spot.x, spot.y, spot.w, spot.h);

      // Spot label & status
      ctx.font = 'bold 11px Inter';
      ctx.fillStyle = spot.occupied ? '#ef4444' : '#10b981';
      ctx.fillText(`BAY 0${spot.id}`, spot.x + 10, spot.y + 20);

      // Status pill
      ctx.font = '9px Fira Code';
      ctx.fillText(spot.occupied ? 'OCCUPIED' : 'VACANT', spot.x + 10, spot.y + 35);

      // Draw parked car if occupied
      if (spot.occupied && spot.carColor) {
        this.drawCar(ctx, spot.x + 18, spot.y + 40, spot.carColor, 0);
      }
    });

    // Draw Moving Cars
    this.movingCars.forEach(car => {
      const angle = (car.stage === 'leave_spot') ? Math.PI : (car.stage === 'exit_out' || car.stage === 'drive_to_exit') ? Math.PI : 0;
      this.drawCar(ctx, car.x, car.y, car.color, angle);
    });

    // Draw Entry Gate (Barrier Arm & Post)
    this.drawGate(ctx, 160, 120, this.entryGateAngle, 'ENTRY', window.simState && window.simState.entryGateOpen);

    // Draw Exit Gate (Barrier Arm & Post)
    this.drawGate(ctx, 160, 320, this.exitGateAngle, 'EXIT', window.simState && window.simState.exitGateOpen);

    // Perimeter curb / barrier
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 4;
    ctx.strokeRect(2, 2, w - 4, h - 4);
  }

  drawCar(ctx, x, y, color, rotation = 0) {
    ctx.save();
    ctx.translate(x + 25, y + 45);
    ctx.rotate(rotation);

    // Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.fillRect(-22, -42, 44, 84);

    // Car Body
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(-20, -40, 40, 80, 8);
    ctx.fill();

    // Windshield & Rear Window
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(-15, -20, 30, 14); // Front windshield
    ctx.fillRect(-14, 15, 28, 10);  // Rear windshield

    // Roof
    ctx.fillStyle = 'rgba(0,0,0,0.15)';
    ctx.fillRect(-15, -6, 30, 21);

    // Headlights
    ctx.fillStyle = '#fef08a';
    ctx.fillRect(-18, -39, 8, 4);
    ctx.fillRect(10, -39, 8, 4);

    // Taillights
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(-18, 36, 8, 4);
    ctx.fillRect(10, 36, 8, 4);

    ctx.restore();
  }

  drawGate(ctx, x, y, angleNorm, label, isOpen) {
    ctx.save();

    // Gate Housing Post
    ctx.fillStyle = '#334155';
    ctx.fillRect(x - 12, y - 10, 24, 30);
    ctx.fillStyle = '#64748b';
    ctx.fillRect(x - 8, y - 6, 16, 22);

    // LED on housing
    ctx.fillStyle = isOpen ? '#22c55e' : '#ef4444';
    ctx.shadowColor = isOpen ? '#22c55e' : '#ef4444';
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.arc(x, y - 18, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Gate Arm Pivot & Rotation
    ctx.translate(x, y + 5);
    const armAngle = -angleNorm * (Math.PI / 2.2);
    ctx.rotate(armAngle);

    // Barrier Arm (Striped Red & White)
    const armLen = 75;
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#fff';
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, armLen);
    ctx.stroke();

    // Red stripes
    ctx.strokeStyle = '#ef4444';
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, armLen);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.restore();
  }
}

window.GarageView = GarageView;
