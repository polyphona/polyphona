export const NoteTooSmallException = () => {
}

/* Examples:
clip(10.3, 1) => 10
clip(12, 5) => 10
clip(15.01, 2.5) => 15.0
*/
const clip = (value, increment) => Math.floor(value / increment) * increment

export class Note {
  constructor (startTime, duration, pitch, velocity = 0.8) {
    this.startTime = startTime
    this.duration = duration
    this.pitch = pitch
    this.id = undefined
    this.velocity = velocity
  }

  /*
  Returns true if this note collides in any manner with the argument note
   */
  disturbs (note) {
    var samePitch = Boolean(note.pitch === this.pitch)
    var disturbs = Boolean(!(this.startTime + this.duration < note.startTime || this.startTime > note.startTime + note.duration))
    var juxtaposed = Boolean(this.startTime === note.startTime + note.duration || this.startTime + this.duration === note.startTime)
    return (samePitch && disturbs) && !juxtaposed
  }
}

export class NoteCanvasAdapter {
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

  toNote (renderContext, box) {
    const duration = Math.floor(box.width / renderContext.percentPerTick)
    if (!duration) {
      throw new NoteTooSmallException()
    }
    return new Note(
      Math.floor(box.x / renderContext.percentPerTick),
      duration,
      Math.floor((100 - (box.y + box.height)) / renderContext.percentPerInterval)
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

export class TrackLoader {
  static toTrack (data) {
    let track = new Track(data.id, data.name)
    for (const note of data.notes) {
      track.addNote(new Note(note.startTime, note.duration, note.pitch))
    }
    return track
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

export const INVERSESCALE = {
  'C': 0,
  'C#': 1,
  'D': 2,
  'D#': 3,
  'E': 4,
  'F': 5,
  'F#': 6,
  'G': 7,
  'G#': 8,
  'A': 9,
  'A#': 10,
  'B': 11
}
