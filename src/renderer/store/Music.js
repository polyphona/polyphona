export const NoteTooSmallException = () => {
}

/* Examples:
clip(10.3, 1) => 10
clip(12, 5) => 10
clip(15.01, 2.5) => 15.0
*/
const clip = (value, increment) => Math.floor(value / increment) * increment

export class Note {
  constructor (startTime, duration, pitch) {
    this.startTime = startTime
    this.duration = duration
    this.pitch = pitch
    this.id = undefined
  }

  /* True if the note collides with existing note with the same pitch */
  collides (note) {
    const samePitch = note.pitch === this.pitch
    const endNoteCollide = note.startTime <= this.startTime && note.startTime + note.duration >= this.startTime + this.duration
    const startNoteCollide = note.startTime >= this.startTime && note.startTime + note.duration <= this.startTime + this.duration
    return samePitch && (endNoteCollide || startNoteCollide)
  }
}

export class NoteCanvasAdapter {
  toBox (renderContext, note) {
    return {
      id: note.id,
      x: renderContext.percentPerTick * note.startTime,
      y: renderContext.percentPerInterval * note.pitch,
      width: renderContext.percentPerTick * note.duration,
      height: renderContext.percentPerInterval
    }
  }

  toNote (renderContext, box) {
    const duration = Math.floor(box.width / renderContext.percentPerTick)
    if (!duration) {
      throw new NoteTooSmallException()
    }
    return new Note(
      Math.floor(box.x / renderContext.percentPerTick),
      duration,
      Math.floor(box.y / renderContext.percentPerInterval)
    )
  }

  clip (renderContext, box) {
    return {
      x: clip(box.x, renderContext.percentPerTick),
      y: clip(box.y, renderContext.percentPerInterval),
      width: clip(box.width, renderContext.percentPerTick),
      height: clip(box.height, renderContext.percentPerInterval)
    }
  }
}

export class Track {
  constructor (remoteId = null, name = 'Test') {
    this.notes = []
    this.lastId = 0
    this.remoteId = remoteId
    this.name = name
  }

  addNote = (note) => {
    note.id = this.lastId
    this.lastId++
    this.notes.push(note)
  }

  deleteNote = (note) => {
    const index = this.notes.indexOf(note)
    this.notes.splice(index, 1)
  }
}

export const SCALE = {
  0: 'C',
  1: 'C#',
  2: 'D',
  3: 'D#',
  4: 'E',
  5: 'F',
  6: 'F#',
  7: 'G',
  8: 'G#',
  9: 'A',
  10: 'A#',
  11: 'B',
  12: 'C'
}
