<template>
  <div class="row">
  <div class="col-2"></div>
  <div class="col-7">
    <NoteCard/>
    <NoteCard/>
  </div>
  <div class="col-3">
  ... ovdje ide desni stupac!
  </div>
  </div>
 </template>

<script>
// @ is an alias to /src
import NoteCard from '@/components/NoteCard.vue'

export default {
  name: 'HomeView',
  components: {
    NoteCard,
  }
}
</script>
