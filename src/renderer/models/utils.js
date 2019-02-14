/* Clip a value by increment.
Examples:
clip(10.3, 1) => 10
clip(12, 5) => 10
clip(15.01, 2.5) => 15.0
*/
export function clip (value, increment) {
  return Math.floor(value / increment) * increment
}
