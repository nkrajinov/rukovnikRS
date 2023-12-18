<template>
  <div class="row">
    <div class="col-2"></div>
    <div class="col-7">
      <form @submit.prevent="postNewNote" class="form-inline mb-5">
        <div class="form-group">
  <label for="gradid">Putovanje</label>
  <input
    v-model="newNoteGrad"
    type="text"
    class="form-control ml-2"
    placeholder="Unesite ime grada"
    id="gradid"
    name="newNoteGrad"
  />
</div>
<div class="form-group">
  <label for="nazivid">Naziv bilješke</label>
  <input
    v-model="newNoteNaziv"
    type="text"
    class="form-control ml-2"
    placeholder="Unesite naziv bilješke"
    id="nazivid"
    name="newNoteNaziv"
  />
</div>
<div class="form-group">
  <label for="tekstid">Tekst bilješke</label>
  <input
    v-model="newNoteText"
    type="text"
    class="form-control ml-2"
    placeholder="Unesite tekst bilješke"
    id="tekstid"
    name="newNoteText"
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
import { collection, getDocs, addDoc } from 'firebase/firestore/lite';

//let cards = [
//  { grad: 'Zagreb', naziv_biljeske: 'Posjet Zoo vrtu', vrijeme: 'prije nekoliko trenutaka' },
//  { grad: 'Madrid', naziv_biljeske: 'muzej', vrijeme: 'prije 8 dana' },
//  { grad: 'Paris', naziv_biljeske: 'E.toranj', vrijeme: 'prije godinu' },
//];

export default {
  name: 'HomeView',
  data() {
    return {
      cards: [],//kod objekta ide dvotočka
      store,
      newNoteGrad: "",
      newNoteNaziv: "",
      newNoteText: "",
      notesCollectionRef: collection(db, 'notes'),
    };
  },
  mounted() {//atribut trenutak kada se komponenta prikaže na ekranu
    this.fetchNotes();
  },
  methods: {
    async fetchNotes() {
      try {
        const notesSnapshot = await getDocs(this.notesCollectionRef);

        this.cards = [];
        notesSnapshot.forEach((doc) => {
          this.cards.push(doc.data());
        });

        console.log('firebase dohvat...:', this.cards);
      } catch (error) {
        console.error('Greška u dohvatu:', error);
      }
    },
    async postNewNote() {
  console.log("OK");

  const notePutovanje = this.newNoteGrad;
  const noteNaziv = this.newNoteNaziv;
  const noteText = this.newNoteText;

  try {
    const newNoteRef = await addDoc(this.notesCollectionRef, {
      grad: notePutovanje,
      naziv_biljeske: noteNaziv,
      tekst: noteText,
      email: store.currentUser,
      posted_at: Date.now(),
    });

    console.log('Spremljeno');

    const newNoteData = {
      grad: notePutovanje,
      naziv_biljeske: noteNaziv, // Promijenjen naziv ključa u skladu s vašim podacima
      tekst: noteText,
      email: store.currentUser,
      posted_at: Date.now(),
      id: newNoteRef.id, // Dodajte ID novododane bilješke u lokalni objekt
    };

    this.cards.push(newNoteData); // Dodajte novu bilješku u this.cards
    this.newNoteGrad = ''; // Očistite polja nakon dodavanja bilješke
    this.newNoteNaziv = '';
    this.newNoteText = '';
  } catch (error) {
    console.error(error);
  }
},
},
  computed: {
  filteredCards() {
    let termin = this.store.searchTerm;
    return this.cards.filter(card => {
      // Check if card.naziv_biljeske exists and is a string before using includes
      return card.naziv_biljeske && typeof card.naziv_biljeske === 'string' &&
        card.naziv_biljeske.includes(termin);
    });
  },
},
  created() {
    this.fetchNotes();
  },
  components: {
    NoteCard,
  },
};
</script>
