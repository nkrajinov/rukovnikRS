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
  export default {
    data() {
      return {
        updatedNoteGrad: '',
        updatedNoteNaziv: '',
        updatedNoteText: '',
      };
    },
    methods: {
      updateNote() {
        const noteId = this.$route.params.id;

// Referenca na dokument u Firestore-u koji želimo ažurirati
const noteRef = db.collection('notes').doc(noteId);

// Ažuriranje podataka bilješke u bazi podataka
noteRef.update({
  grad: this.updatedNoteGrad,
  naziv_biljeske: this.updatedNoteNaziv,
  tekst: this.updatedNoteText,
})
.then(() => {
  console.log('Bilješka je uspješno ažurirana.');
  // Opcionalno: Preusmjerite korisnika natrag na početnu stranicu ili gdje god želite
})
.catch((error) => {
  console.error('Greška pri ažuriranju bilješke:', error);
});
      },
    },
  };
  </script>
  