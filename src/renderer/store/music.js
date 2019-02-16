export class Note {
  constructor (startTime, duration, pitch, velocity = 0.8) {
    // NOTE: will be set when the note is added to a `Track`.
    this.id = undefined
    this.startTime = startTime
    this.duration = duration
    this.pitch = pitch
    this.velocity = velocity
  }

  /* Whether this note collides in any manner with the given note. */
  disturbs (note) {
    const samePitch = note.pitch === this.pitch

    const overlapsRight = this.startTime < note.startTime + note.duration
    const overlapsLeft = this.startTime + this.duration > note.startTime
    const overlaps = overlapsRight && overlapsLeft

    return samePitch && overlaps
  }
}

export class Track {
  constructor (remoteId = null, name = '') {
    this.notes = []
    this.lastId = 0
    this.remoteId = remoteId
    this.name = name
  }

  addNote = note => {
    note.id = this.lastId
    this.lastId++
    this.notes.push(note)
  }

  deleteNote = note => {
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
  C: 0,
  'C#': 1,
  D: 2,
  'D#': 3,
  E: 4,
  F: 5,
  'F#': 6,
  G: 7,
  'G#': 8,
  A: 9,
  'A#': 10,
  B: 11
}
