// Helper functions to convert a percentage of canvas area to pixels.

export function percentWidthToPix (percent, ctx) {
  return Math.floor((ctx.canvas.width / 100) * percent)
}

export function percentHeightToPix (percent, ctx) {
  return Math.floor((ctx.canvas.height / 100) * percent)
}
