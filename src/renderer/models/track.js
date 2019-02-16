import { Note } from './note'

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
