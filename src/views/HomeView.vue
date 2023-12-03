<template>
  <div class="row">
    <div class="col-2"></div>
    <div class="col-7">
      <NoteCard v-for="card in cards" :key="card.grad" :info="card" />
    </div>
    <div class="col-3">
      Sidebar
      {{ store.searchTerm }}
    </div>
  </div>
</template>

<script>
import NoteCard from '@/components/NoteCard.vue';
import store from "@/store";

let cards = [
  { grad: 'Zagreb', naziv_biljeske: 'Posjet Zoo vrtu', vrijeme: 'prije nekoliko trenutaka' },
  { grad: 'Madrid', naziv_biljeske: 'muzej', vrijeme: 'prije 8 dana' },
  { grad: 'Paris', naziv_biljeske: 'E.toranj', vrijeme: 'prije godinu' },
];

export default {
  name: 'HomeView',
  data() {
    return {
      cards: cards,
      store,
    };
  },
  components: {
    NoteCard,
  },
};
</script>
