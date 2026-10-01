/* Hero visual: Signal Flow (js/hero/flow.js) — a pipeline where packets are processed, verified and delivered. */
import { init } from './hero/flow.js';

export function initHero(container) {
  if (!container) return null;
  return init(container);
}
