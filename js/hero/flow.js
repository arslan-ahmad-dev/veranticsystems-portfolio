/* Hero option: Signal Flow — a pipeline of nodes. Packets enter on the left, pass through
   processing and a verification gate, and leave as confirmed results on the right. */
import { themeVars, canvas2d, mouseTracker, drawCheck, easeOutCubic, clamp01 } from './shared.js';

export function init(container) {
  container.dataset.mask = 'none';
  const { ctx, state, destroy: destroyCanvas } = canvas2d(container);
  const mouse = mouseTracker();
  let theme = themeVars();
  const onTheme = () => { theme = themeVars(); };
  window.addEventListener('themechange', onTheme);

  // Normalised layout (0..1). Layers: inputs -> processors -> gate -> output
  const nodes = [
    { id: 'in0', x: 0.10, y: 0.22, r: 13, kind: 'in' },
    { id: 'in1', x: 0.08, y: 0.50, r: 13, kind: 'in' },
    { id: 'in2', x: 0.10, y: 0.78, r: 13, kind: 'in' },
    { id: 'p0', x: 0.40, y: 0.32, r: 22, kind: 'proc' },
    { id: 'p1', x: 0.40, y: 0.68, r: 22, kind: 'proc' },
    { id: 'gate', x: 0.68, y: 0.50, r: 32, kind: 'gate' },
    { id: 'out', x: 0.92, y: 0.50, r: 20, kind: 'out' },
  ];
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
  const edges = [
    ['in0', 'p0'], ['in1', 'p0'], ['in1', 'p1'], ['in2', 'p1'],
    ['p0', 'gate'], ['p1', 'gate'], ['gate', 'out'],
  ];
  const routes = [
    ['in0', 'p0', 'gate', 'out'], ['in1', 'p0', 'gate', 'out'],
    ['in1', 'p1', 'gate', 'out'], ['in2', 'p1', 'gate', 'out'],
  ];
  const packets = [];
  const pulses = [];   // node pulses {node, t0}
  let outCheck = 0;    // check-mark draw progress on the output node
  let verifiedCount = 0;
  let lastSpawn = 0, alive = true, ready = false;
  const start = performance.now();

  // Cubic bezier between two nodes with a horizontal "S" shape
  function bez(a, b, W, H) {
    const ax = a.x * W, ay = a.y * H, bx = b.x * W, by = b.y * H;
    const dx = (bx - ax) * 0.5;
    return { p0: [ax, ay], p1: [ax + dx, ay], p2: [bx - dx, by], p3: [bx, by] };
  }
  function bezPoint(c, t) {
    const mt = 1 - t;
    return [
      mt * mt * mt * c.p0[0] + 3 * mt * mt * t * c.p1[0] + 3 * mt * t * t * c.p2[0] + t * t * t * c.p3[0],
      mt * mt * mt * c.p0[1] + 3 * mt * mt * t * c.p1[1] + 3 * mt * t * t * c.p2[1] + t * t * t * c.p3[1],
    ];
  }

  function frame(now) {
    if (!alive) return;
    requestAnimationFrame(frame);
    if (container.offsetParent === null) return;
    const t = (now - start) / 1000;
    const { w, h } = state;
    mouse.update(0.04);
    ctx.clearRect(0, 0, w, h);

    // Layout box with breathing room, subtle parallax
    const pad = Math.min(w, h) * 0.08;
    const W = w - pad * 2, H = Math.min(h - pad * 2, W * 0.9);
    const ox = pad + mouse.smooth.x * 8, oy = (h - H) / 2 + mouse.smooth.y * 6;
    ctx.save(); ctx.translate(ox, oy);
    const bob = (n) => Math.sin(t * 0.9 + n.x * 7 + n.y * 3) * 3;
    const pos = (n) => [n.x * W, n.y * H + bob(n)];

    // Spawn packets
    if (t - lastSpawn > 0.75) {
      lastSpawn = t;
      packets.push({ route: routes[Math.floor(Math.random() * routes.length)], seg: 0, u: 0, speed: 0.55 + Math.random() * 0.2, trail: [] });
    }

    // Edges
    ctx.lineCap = 'round';
    for (const [aId, bId] of edges) {
      const a = byId[aId], b = byId[bId];
      const [ax, ay] = pos(a), [bx, by] = pos(b);
      const c = bez({ x: ax / W, y: ay / H }, { x: bx / W, y: by / H }, W, H);
      ctx.beginPath(); ctx.moveTo(c.p0[0], c.p0[1]); ctx.bezierCurveTo(c.p1[0], c.p1[1], c.p2[0], c.p2[1], c.p3[0], c.p3[1]);
      ctx.strokeStyle = theme.a(0.22); ctx.lineWidth = 3; ctx.setLineDash([]); ctx.stroke();
      // moving dashes
      ctx.strokeStyle = theme.a(0.5); ctx.lineWidth = 2.5; ctx.setLineDash([4, 16]); ctx.lineDashOffset = -t * 40; ctx.stroke();
      ctx.setLineDash([]);
    }

    // Packets
    for (let k = packets.length - 1; k >= 0; k--) {
      const p = packets[k];
      const a = byId[p.route[p.seg]], b = byId[p.route[p.seg + 1]];
      const [ax, ay] = pos(a), [bx, by] = pos(b);
      const c = bez({ x: ax / W, y: ay / H }, { x: bx / W, y: by / H }, W, H);
      p.u += p.speed / 60;
      const [x, y] = bezPoint(c, clamp01(p.u));
      p.trail.push([x, y]); if (p.trail.length > 10) p.trail.shift();
      // trail
      for (let i = 0; i < p.trail.length; i++) {
        const f = (i + 1) / p.trail.length;
        ctx.beginPath(); ctx.arc(p.trail[i][0], p.trail[i][1], 2.5 + f * 3.5, 0, Math.PI * 2);
        ctx.fillStyle = theme.a(0.08 + f * 0.5); ctx.fill();
      }
      ctx.beginPath(); ctx.arc(x, y, 6, 0, Math.PI * 2); ctx.fillStyle = theme.accent; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, 13, 0, Math.PI * 2); ctx.fillStyle = theme.a(0.2); ctx.fill();
      if (p.u >= 1) {
        pulses.push({ node: b.id, t0: t });
        if (b.kind === 'gate') p.speed *= 0.85;   // slows through inspection
        if (b.kind === 'out') { verifiedCount++; outCheck = 0.0001; packets.splice(k, 1); continue; }
        p.seg++; p.u = 0; p.trail = [];
      }
    }

    // Pulses
    for (let k = pulses.length - 1; k >= 0; k--) {
      const pl = pulses[k]; const age = t - pl.t0;
      if (age > 1) { pulses.splice(k, 1); continue; }
      const n = byId[pl.node]; const [x, y] = pos(n);
      ctx.beginPath(); ctx.arc(x, y, n.r + 6 + age * 26, 0, Math.PI * 2);
      ctx.strokeStyle = theme.a((1 - age) * 0.5); ctx.lineWidth = 2; ctx.stroke();
    }

    // Nodes
    for (const n of nodes) {
      const [x, y] = pos(n);
      // glow
      const g = ctx.createRadialGradient(x, y, 0, x, y, n.r * 3);
      g.addColorStop(0, theme.a(n.kind === 'gate' ? 0.22 : 0.12)); g.addColorStop(1, theme.a(0));
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, n.r * 3, 0, Math.PI * 2); ctx.fill();
      // body
      ctx.beginPath(); ctx.arc(x, y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = theme.bg; ctx.fill();
      ctx.lineWidth = n.kind === 'gate' ? 2.5 : 2; ctx.strokeStyle = theme.a(0.85); ctx.stroke();
      if (n.kind === 'in') {
        ctx.fillStyle = theme.a(0.9); ctx.fillRect(x - 4.5, y - 4.5, 9, 9);
      } else if (n.kind === 'proc') {
        // rotating "processing" arc
        ctx.beginPath(); ctx.arc(x, y, n.r * 0.55, t * 2.2, t * 2.2 + Math.PI * 1.3);
        ctx.strokeStyle = theme.accent; ctx.lineWidth = 2.5; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, n.r * 0.55, 0, Math.PI * 2); ctx.strokeStyle = theme.a(0.2); ctx.lineWidth = 2.5; ctx.stroke();
      } else if (n.kind === 'gate') {
        // shield outline + inner ring that "scans"
        ctx.save(); ctx.translate(x, y);
        ctx.beginPath();
        ctx.moveTo(0, -17); ctx.lineTo(14, -11); ctx.lineTo(14, 1); ctx.quadraticCurveTo(14, 12, 0, 18); ctx.quadraticCurveTo(-14, 12, -14, 1); ctx.lineTo(-14, -11); ctx.closePath();
        ctx.strokeStyle = theme.accent; ctx.lineWidth = 2.5; ctx.stroke();
        ctx.fillStyle = theme.a(0.14); ctx.fill();
        const scanY = -14 + ((t * 0.8) % 1) * 28;
        ctx.beginPath(); ctx.moveTo(-11, scanY); ctx.lineTo(11, scanY); ctx.strokeStyle = theme.a(0.9); ctx.lineWidth = 1.5; ctx.stroke();
        ctx.restore();
      } else if (n.kind === 'out') {
        if (outCheck > 0) { outCheck = Math.min(1, outCheck + 0.06); }
        ctx.beginPath(); ctx.arc(x, y, n.r, 0, Math.PI * 2); ctx.fillStyle = theme.a(0.15 + easeOutCubic(outCheck) * 0.75); ctx.fill();
        drawCheck(ctx, x, y, n.r * 1.1, outCheck || 0.001, outCheck > 0.3 ? (theme.dark ? theme.bg : '#FFFFFF') : theme.a(0.9), 2.4);
      }
    }

    // Labels
    ctx.font = '700 11px "Mona Sans", sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    ctx.fillStyle = theme.muted;
    const label = (id, txt, dy = 0) => { const [x, y] = pos(byId[id]); ctx.fillText(txt, x, y + byId[id].r + 10 + dy); };
    const fr = document.documentElement.lang === 'fr';
    label('in1', 'LEADS', 0); label('p1', 'CRM', 0); label('gate', fr ? 'AUTOMATISER' : 'AUTOMATE', 0); label('out', fr ? 'RDV PRIS' : 'BOOKED', 0);
    // counter
    ctx.textAlign = 'right'; ctx.font = '700 13px "Mona Sans", sans-serif'; ctx.fillStyle = theme.accent;
    ctx.fillText(fr ? `${verifiedCount} rendez-vous pris` : `${verifiedCount} leads booked`, W, -6);

    ctx.restore();
    if (!ready) { ready = true; setTimeout(() => container.classList.add('is-ready'), 150); }
  }
  requestAnimationFrame(frame);

  return {
    destroy() { alive = false; window.removeEventListener('themechange', onTheme); mouse.destroy(); destroyCanvas(); },
  };
}
