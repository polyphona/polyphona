export class Note {
  constructor (startTime, duration, pitch) {
    this.startTime = startTime
    this.duration = duration
    this.pitch = pitch
  }
}

export class NoteCanvasAdapter {
  toBox (renderContext, note) {
    return {
      x: renderContext.percentPerQuarter * note.startTime,
      y: renderContext.percentPerInterval * note.pitch,
      width: renderContext.percentPerQuarter * note.duration,
      height: renderContext.percentPerInterval
    }
  }

  toNote (renderContext, box) {
    return new Note(
      box.x / renderContext.percentPerQuarter,
      box.width / renderContext.percentPerQuarter,
      Math.floor(box.y / renderContext.percentPerInterval)
    )
  }
}

export class Track {
  constructor () {
    this.notes = []
  }

  addNote = (note) => {
    this.notes.push(note)
  }
}
