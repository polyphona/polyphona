export class Note {
  constructor (startTime, duration, pitch) {
    this.startTime = startTime
    this.duration = duration
    this.pitch = pitch
  }

  equals (note) {
    if (note.startTime === this.startTime && note.duration === this.duration && note.pitch === this.pitch) {
      return true
    }
    return false
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
      Math.floor(box.x / renderContext.percentPerQuarter),
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

  deleteNote = (note) => {
    const index = this.notes.indexOf(note)
    console.log(index)
    this.notes.splice(index, 1)
  }
}
