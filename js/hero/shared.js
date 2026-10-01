/* Shared helpers for hero visual modules. */

/* Read theme colours from the active CSS variables. */
export function themeVars() {
  const cs = getComputedStyle(document.documentElement);
  const v = (name, fallback) => (cs.getPropertyValue(name).trim() || fallback);
  const rgb = (v('--accent-rgb', '26, 155, 232')).split(',').map((n) => parseFloat(n));
  const glow = (v('--glow-rgb', '56, 189, 248')).split(',').map((n) => parseFloat(n));
  const bgRgb = (v('--bg-void-rgb', '255, 255, 255')).split(',').map((n) => parseFloat(n));
  const dark = (bgRgb[0] + bgRgb[1] + bgRgb[2]) / 3 < 128;
  return {
    accent: v('--accent', '#1A9BE8'),
    accentRgb: rgb,
    glowRgb: glow,
    bg: v('--bg-void', '#FFFFFF'),
    bgRgb,
    text: v('--text-primary', '#0B1220'),
    muted: v('--text-muted', '#55657D'),
    subtle: v('--text-subtle', '#7C8BA1'),
    dark,
    a: (alpha) => `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`,
    g: (alpha) => `rgba(${glow[0]}, ${glow[1]}, ${glow[2]}, ${alpha})`,
    bgA: (alpha) => `rgba(${bgRgb[0]}, ${bgRgb[1]}, ${bgRgb[2]}, ${alpha})`,
  };
}

/* Set up a 2D canvas that tracks its container size and device pixel ratio. */
export function canvas2d(container) {
  const canvas = document.createElement('canvas');
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  const state = { w: 0, h: 0, dpr: 1 };
  function resize() {
    state.dpr = Math.min(window.devicePixelRatio || 1, 2);
    state.w = container.clientWidth || 1;
    state.h = container.clientHeight || 1;
    canvas.width = Math.round(state.w * state.dpr);
    canvas.height = Math.round(state.h * state.dpr);
    canvas.style.width = state.w + 'px';
    canvas.style.height = state.h + 'px';
    ctx.setTransform(state.dpr, 0, 0, state.dpr, 0, 0);
  }
  resize();
  window.addEventListener('resize', resize, { passive: true });
  return {
    canvas, ctx, state,
    destroy() { window.removeEventListener('resize', resize); if (canvas.parentNode) canvas.parentNode.removeChild(canvas); },
  };
}

/* Mouse position normalised to -1..1, smoothed. */
export function mouseTracker() {
  const raw = { x: 0, y: 0 };
  const smooth = { x: 0, y: 0 };
  const onMove = (e) => { raw.x = (e.clientX / window.innerWidth - 0.5) * 2; raw.y = (e.clientY / window.innerHeight - 0.5) * 2; };
  window.addEventListener('mousemove', onMove, { passive: true });
  return {
    smooth,
    update(k = 0.05) { smooth.x += (raw.x - smooth.x) * k; smooth.y += (raw.y - smooth.y) * k; },
    destroy() { window.removeEventListener('mousemove', onMove); },
  };
}

export const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
export const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const easeOutBack = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
export const clamp01 = (t) => Math.max(0, Math.min(1, t));

/* Draw a check mark inside a box centred at (cx, cy); progress 0..1 draws it in. */
export function drawCheck(ctx, cx, cy, size, progress, color, width) {
  const p = clamp01(progress);
  if (p <= 0) return;
  const s = size / 2;
  const pts = [[cx - s * 0.7, cy + s * 0.05], [cx - s * 0.15, cy + s * 0.6], [cx + s * 0.8, cy - s * 0.55]];
  const seg1 = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]);
  const seg2 = Math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]);
  const total = seg1 + seg2;
  const len = total * p;
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = width; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath();
  ctx.moveTo(pts[0][0], pts[0][1]);
  if (len <= seg1) {
    const t = len / seg1; ctx.lineTo(pts[0][0] + (pts[1][0] - pts[0][0]) * t, pts[0][1] + (pts[1][1] - pts[0][1]) * t);
  } else {
    ctx.lineTo(pts[1][0], pts[1][1]);
    const t = (len - seg1) / seg2; ctx.lineTo(pts[1][0] + (pts[2][0] - pts[1][0]) * t, pts[1][1] + (pts[2][1] - pts[1][1]) * t);
  }
  ctx.stroke();
  ctx.restore();
}
