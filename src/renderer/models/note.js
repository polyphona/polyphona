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
