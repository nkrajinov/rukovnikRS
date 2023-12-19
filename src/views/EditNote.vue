<template>
    <div>
      <h2>Uredi bilješku</h2>
      <form @submit.prevent="updateNote">
        <div class="form-group">
          <label for="updatedNoteGrad">Putovanje</label>
          <input v-model="updatedNoteGrad" type="text" class="form-control" id="updatedNoteGrad" name="updatedNoteGrad">
        </div>
        <div class="form-group">
          <label for="updatedNoteNaziv">Naziv bilješke</label>
          <input v-model="updatedNoteNaziv" type="text" class="form-control" id="updatedNoteNaziv" name="updatedNoteNaziv">
        </div>
        <div class="form-group">
          <label for="updatedNoteText">Tekst bilješke</label>
          <input v-model="updatedNoteText" type="text" class="form-control" id="updatedNoteText" name="updatedNoteText">
        </div>
        <button type="submit" class="btn btn-primary">Spremi promjene</button>
      </form>
    </div>
  </template>
  
  <script>
import { db } from '@/firebase';
import { doc, getDoc, updateDoc } from 'firebase/firestore/lite';

export default {
  data() {
    return {
      updatedNoteGrad: '',
      updatedNoteNaziv: '',
      updatedNoteText: '',
      noteId: this.$route.params.id,
    };
  },
  methods: {
    async fetchNoteData() {
      try {
        const noteRef = doc(db, 'notes', this.noteId);
        const docSnap = await getDoc(noteRef);

        if (docSnap.exists()) {
          const data = docSnap.data();
          this.updatedNoteGrad = data.grad || '';
          this.updatedNoteNaziv = data.naziv_biljeske || '';
          this.updatedNoteText = data.tekst || '';
        } else {
          console.error('Dokument ne postoji');
        }
      } catch (error) {
        console.error('Greška pri dohvatu podataka:', error);
      }
    },
    async fetchNotes() {
      try {
        console.log('Ovdje dohvatite podatke o karticama...');
      } catch (error) {
        console.error('Greška pri dohvatu podataka o karticama:', error);
      }
    },async updateNote() {
      try {
        const noteRef = doc(db, 'notes', this.noteId);
        await updateDoc(noteRef, {
          grad: this.updatedNoteGrad,
          naziv_biljeske: this.updatedNoteNaziv,
          tekst: this.updatedNoteText,
        });
        console.log('Bilješka je uspješno ažurirana.');
        await this.fetchNotes();
        this.$router.push({ name: 'home' });//nakon izmjene idemo na naslovnicu
      } catch (error) {
        console.error('Greška pri ažuriranju bilješke:', error);
      }
    },
  },

  mounted() {
    this.fetchNoteData();
  },
};

</script>