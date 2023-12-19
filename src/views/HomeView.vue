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
      <NoteCard v-for="card in filteredCards" :key="card.id" :info="card" @delete="deleteNote" />
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
import { collection, getDocs, addDoc, deleteDoc, doc } from 'firebase/firestore/lite';

export default {
  name: 'HomeView',
  data() {
    return {
      cards: [],
      store,
      newNoteGrad: "",
      newNoteNaziv: "",
      newNoteText: "",
      notesCollectionRef: collection(db, 'notes'),
    };
  },
  mounted() {
    this.fetchNotes();
  },
  methods: {
    async fetchNotes() {
      try {
        const notesSnapshot = await getDocs(this.notesCollectionRef);
        this.cards = [];
        notesSnapshot.forEach((doc) => {
          const noteData = doc.data();
          const noteId = doc.id;
          const noteWithId = { ...noteData, id: noteId };
          this.cards.push(noteWithId);
        });
        console.log('Firebase dohvat...', this.cards);
      } catch (error) {
        console.error('Greška u dohvatu:', error);
      }
    },
    async postNewNote() {
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
          naziv_biljeske: noteNaziv,
          tekst: noteText,
          email: store.currentUser,
          posted_at: Date.now(),
          id: newNoteRef.id,
        };

        this.cards.push(newNoteData);
        this.newNoteGrad = '';
        this.newNoteNaziv = '';
        this.newNoteText = '';
      } catch (error) {
        console.error(error);
      }
    },
    async deleteNote(noteId) {
      try {
        const noteRef = doc(db, 'notes', noteId);
        await deleteDoc(noteRef);
        console.log('Bilješka je uspješno izbrisana.');
       // Ažurirajte kartice nakon brisanja bilješke
        await this.fetchNotes();
      } catch (error) {
        console.error('Greška pri brisanju bilješke:', error);
      }
      console.log('Funkcija deleteNote je pozvana s ID:', noteId);
    },
  },
  computed: {
    filteredCards() {
      let termin = this.store.searchTerm;
      return this.cards.filter(card => {
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
