<template>
  <div class="row">
    <div class="col-2"></div>
    <div class="col-7">
      <NoteCard v-for="card in filteredCards" :key="card.grad" :info="card" />
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
  data() { //f
    return {
      cards,
      store,
    };
  },
  computed: { //objekt i unutra f za obradu ili filter
    filteredCards() {
      //logika koja filtrira cards, trebamo this pokazivač za pristupanje u data dio
      let termin = this.store.searchTerm;
      //odaberemo array kojeg želimo filtrirati, pozovemo metodu filter i kao parametar predamo f koji će za svaki card koji je unutar cardova vratiti T ili F
      return this.cards.filter(card => card.naziv_biljeske.includes(termin));
    },
  },
  components: {
    NoteCard,
  },
};
</script>
