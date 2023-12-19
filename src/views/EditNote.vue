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
        noteId: this.$route.params.id,//spremam id bilješke iz rute u komponenti
      };
    },
    methods: {//dohvaćam podatke bilješke iz Firestore-a na temelju ID-a
    async fetchNoteData() {
      try {
        const doc = await db.collection('notes').doc(this.noteId).get();
        if (doc.exists) {
          const data = doc.data();
          // Postavite vrijednosti podataka bilješke u vaše inpute za uređivanje
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
    async updateNote() {
      try {
        // Ako želite osigurati da su podaci bilješke ažurirani prije nego što preusmjerite korisnika,
        // možete pričekati da se ažuriranje završi prije preusmjeravanja
        await db.collection('notes').doc(this.noteId).update({
          grad: this.updatedNoteGrad,
          naziv_biljeske: this.updatedNoteNaziv,
          tekst: this.updatedNoteText,
        });

        console.log('Bilješka je uspješno ažurirana.');
        // Ovdje možete postaviti logiku za preusmjeravanje korisnika na željenu rutu
      } catch (error) {
        console.error('Greška pri ažuriranju bilješke:', error);
      }
    },
  },
  mounted() {
    // Kada se komponenta mounta, dohvatite podatke bilješke iz baze
    this.fetchNoteData();
  },
};
</script>