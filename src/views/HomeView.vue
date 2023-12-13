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
    cards: [],//kod objekta ide :
    store,
    newNoteGrad: "",
    newNoteNaziv: "",
    newNoteText: "",
  };
},
mounted() {
  this.fetchNotes();
},
methods: {
    async fetchNotes() {
      try {
        const notesSnapshot = await getDocs(notesCollectionRef);

        this.cards = [];
        notesSnapshot.forEach((doc) => {
          this.cards.push(doc.data());
        });

        console.log('firebase dohvat...:', this.cards);
      } catch (error) {
        console.error('Greška u dohvatu:', error);
      }
    },
    
    postNewNote() {
      console.log("OK");

      const notePutovanje = this.newNoteGrad;
      const noteNaziv = this.newNoteNaziv;
      const noteText = this.newNoteText;

      const notesCollectionRef = collection(db, 'notes');

      addDoc(notesCollectionRef, {
        grad: notePutovanje,
        naz: noteNaziv,
        tekst: noteText,
        email: store.currentUser,
        posted_at: Date.now(),
     }).then((docRef) => {
       console.log('Spremljeno', docRef.id);
      }).catch((error) => {
       console.error(error);
     });
    },

  },
  computed: {
    filteredCards() {
      let termin = this.store.searchTerm;
      return this.cards.filter(card => card.naziv_biljeske.includes(termin));
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
