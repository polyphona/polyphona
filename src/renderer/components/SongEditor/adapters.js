import { clip } from './utils'
import { NoteTooSmallException } from './errors'
import { Note } from '@/store/music'

/* Convert canvas percentages to pixels and vice-versa. */
export class MouseCanvasAdapter {
  percentWidthToPix (percent, ctx) {
    return Math.floor((ctx.canvas.width / 100) * percent)
  }

  percentHeightToPix (percent, ctx) {
    return Math.floor((ctx.canvas.height / 100) * percent)
  }

  pixWidthToPercent (pixels, ctx) {
    return (100 * pixels) / ctx.canvas.width
  }

  pixHeightToPercent (pixels, ctx) {
    return (100 * pixels) / ctx.canvas.height
  }
}

/* Convert canvas boxes to notes and vice-versa. */
export class NoteCanvasAdapter {
  /* Convert a ``Note`` to a box. */
  toBox (renderContext, note) {
    const height = renderContext.percentPerInterval
    return {
      id: note.id,
      x: renderContext.percentPerTick * note.startTime,
      y: 100 - (height + renderContext.percentPerInterval * note.pitch),
      width: renderContext.percentPerTick * note.duration,
      height
    }
  }

  /* Convert a box to a ``Note``. */
  toNote (renderContext, box) {
    const duration = Math.floor(box.width / renderContext.percentPerTick)
    if (!duration) {
      throw new NoteTooSmallException()
    }
    return new Note(
      Math.floor(box.x / renderContext.percentPerTick),
      duration,
      Math.floor(
        (100 - (box.y + box.height)) / renderContext.percentPerInterval
      )
    )
  }

  /* Clip a box to unit note dimensions. */
  clip (renderContext, box) {
    return {
      x: clip(box.x, renderContext.percentPerTick),
      y: clip(box.y, renderContext.percentPerInterval),
      width: clip(box.width, renderContext.percentPerTick),
      height: clip(box.height, renderContext.percentPerInterval)
    }
  }
}
