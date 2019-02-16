<template>
  <ol>
    <li v-for="pitch in pitches" :key="'pitch-' + pitch.id">{{ pitch.name }}</li>
  </ol>
</template>

<script>
export default {
  name: 'pitch-header',
  computed: {
    scale () {
      return this.$store.getters['music/getMusicContext'].scale
    },
    pitches () {
      return Object.keys(this.scale).map((index) => ({
        id: index,
        name: this.scale[index]
      })).reverse()
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "../../styles/_bootstrap_override.scss";

  ol {
    // Fill parent's height.
    height: 100%;

    // Remove default list styling.
    list-style-type: none;
    padding: 0;
    margin: 0;

    // Display list items in a column.
    display: flex;
    flex-flow: column;

    text-align: center;
    color: map-get($theme-colors, "light");
    background: map-get($theme-colors, "dark");

    li {
        padding: 0 .5em;
        margin: auto 0;
    }
  }
</style>
