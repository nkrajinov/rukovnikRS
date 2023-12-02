<template>
  <div class="row">
  <div class="col-2"></div>
  <div class="col-7">
    <NoteCard/>
    <NoteCard/>
    <NoteCard/>
  </div>
  <div class="col-3">Sidebar {{ hello }} {{ lista }}</div>
  </div>
 </template>

<script>
// @ is an alias to /src
import NoteCard from '@/components/NoteCard.vue';

export default {
  name: 'HomeView',
  data() {
    return {
      hello: 'world',
      lista: [1, 2, 3, 'lj'],
    };
  },
  components: {
    NoteCard,
  },
};
</script>