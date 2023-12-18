<template>
  <div class="card text-center">
    <div class="card-header">
      {{ info.grad }}
    </div>
    <div class="card-body p-0">
      <h5 class="card-title">{{ info.naziv_biljeske }}</h5>
      <p class="card-text">{{ info.tekst }}</p>
    </div>
    <div class="card-footer text-body-secondary">
      {{ formatTime(info.posted_at) }}
      <button @click="editNote" class="btn btn-primary btn-sm m-1">Uredi</button>
      <button @click="deleteNote" class="btn btn-danger btn-sm m-1">Obriši</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['info'],
  name: 'NoteCard',
  methods: {
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    editNote() {
      this.$router.push({ name: 'EditNote', params: { id: this.info.id } });
    },
    deleteNote() {
      // Implementirajte logiku za brisanje bilješke
      // Ovdje možete koristiti Firebase da izbrišete bilješku s ID-om this.info.id iz baze
      // Primjer:
      // const noteRef = db.collection('notes').doc(this.info.id);
      // noteRef.delete().then(() => {
      //   // Bilješka je uspješno obrisana iz baze, možete ažurirati prikaz na korisničkom sučelju
      // }).catch((error) => {
      //   console.error('Greška pri brisanju bilješke:', error);
      // });
    },
  },
};
</script>
