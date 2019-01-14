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

  equals (note) {
    // TODO Renommer Collide => Vérifier intervalle parmi ceux recouverts par les autres notes
    if (note.startTime === this.startTime && note.duration === this.duration && note.pitch === this.pitch) {
      return true
    }
    return false
  }
}

export class NoteCanvasAdapter {
  toBox (renderContext, note) {
    return {
      id: note.id,
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
      x: clip(box.x, renderContext.percentPerQuarter),
      y: clip(box.y, renderContext.percentPerInterval),
      width: clip(box.width, renderContext.percentPerQuarter),
      height: clip(box.height, renderContext.percentPerInterval)
    }
  }
}

export class Track {
  constructor () {
    this.notes = []
    this.lastId = 0
  }

  addNote = (note) => {
    // TODO Ajouter Check anciennes notes
    note.id = this.lastId
    this.lastId++
    this.notes.push(note)
  }

  deleteNote = (note) => {
    const index = this.notes.indexOf(note)
    this.notes.splice(index, 1)
  }
}
