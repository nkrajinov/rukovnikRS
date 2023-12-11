<template>
  <div class="row">
    <div class="col-2"></div>
    <div class="col-7">
      <form @submit.prevent="postNewNote" class="form-inline mb-5">
        <div class="form-group">
          <label for="notePutovanje">Putovanje</label>
          <input
            v-model="newNoteGrad"
            type="text"
            class="form-control ml-2"
            placeholder="Unesite ime grada"
            id="gradid"
          />
        </div>
        <div class="form-group">
          <label for="noteNaziv">Naziv bilješke</label>
          <input
            v-model="newNoteNaziv"
            type="text"
            class="form-control ml-2"
            placeholder="Unesite naziv bilješke"
            id="nazivid"
          />
        </div>
        <div class="form-group">
          <label for="noteText">Tekst bilješke</label>
          <input
            v-model="newNoteText"
            type="text"
            class="form-control ml-2"
            placeholder="Unesite tekst bilješke"
            id="tekstid"
          />
        </div>
        <button type="submit" class="btn btn-primary ml-2">Objavi bilješku</button>
      </form>
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
import { db } from '@/firebase';

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
      newNoteGrad: "",
      newNoteNaziv: "",
      newNoteText: "",
    };
  },
  methods: {
    postNewNote() {
      console.log("OK");

      const notePutovanje = this.newNoteGrad;
      const noteNaziv = this.newNoteNaziv;
      const noteText = this.newNoteText;

      db.collection('posts').add({
        grad: notePutovanje,
        naz: noteNaziv,
        tekst: noteText,
        email: store.currentUser,
        posted_at: Date.now(),
      }).then((docRef) => {
        console.log('Spremljeno', docRef.id);
      })
      .catch((error) => {
        console.error(e);
      });
    },
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
