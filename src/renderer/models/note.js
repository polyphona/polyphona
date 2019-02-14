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
    var samePitch = note.pitch === this.pitch
    var disturbs = !(
      this.startTime + this.duration < note.startTime ||
      this.startTime > note.startTime + note.duration
    )
    var juxtaposed =
      this.startTime === note.startTime + note.duration ||
      this.startTime + this.duration === note.startTime
    return samePitch && disturbs && !juxtaposed
  }
}
