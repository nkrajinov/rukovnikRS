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
      <p>{{ formatTime(info.posted_at) }}</p>
      <button @click="editNote" class="btn btn-primary btn-sm m-1">Uredi</button>
      <button @click="confirmDelete" class="btn btn-danger btn-sm m-1">Obriši</button>
    </div>
  </div>
</template>

<script>
import { deleteDoc, doc } from 'firebase/firestore/lite';
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
    async confirmDelete() {
      const confirmed = confirm('Jeste li sigurni da želite obrisati ovu bilješku?');

      if (confirmed) {
        try {
          await this.$emit('delete', this.info.id);
          console.log('Bilješka je uspješno izbrisana.');
        } catch (error) {
          console.error('Greška pri brisanju bilješke:', error);
        }
      }
    },
  },
};
</script>
