export const NoteTooSmallException = () => {
}

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
    const width = Math.floor(box.width / renderContext.percentPerQuarter)
    if (!width) {
      throw new NoteTooSmallException()
    }
    return new Note(
      Math.floor(box.x / renderContext.percentPerQuarter),
      width,
      Math.floor(box.y / renderContext.percentPerInterval)
    )
  }

  clip (renderContext, box) {
    return {
      x: Math.floor(box.x / renderContext.percentPerQuarter) * renderContext.percentPerQuarter,
      y: Math.floor(box.y / renderContext.percentPerInterval) * renderContext.percentPerInterval,
      width: Math.floor(box.width / renderContext.percentPerQuarter) * renderContext.percentPerQuarter,
      height: box.height
    }
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
