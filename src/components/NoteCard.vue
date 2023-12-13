<template>
  <div class="card text-center">
    <div class="card-header">
      {{ info.grad }}
    </div>
    <div class="card-body p-0">
      <h5 class="card-title">{{ info.naz }}</h5>
      <p class="card-text">{{ info.tekst }}</p>
    </div>
    <div class="card-footer text-body-secondary">
      {{ formatTime(info.posted_at) }}
    </div>
  </div>
</template>

<script>
export default {
  props: ['info'],
  name: 'NoteCard',
  methods: {
    formatTime(timestamp) {
      // Format the timestamp to display it as desired (e.g., using moment.js or Date methods)
      // Example format using Date:
      const date = new Date(timestamp);
      return date.toLocaleString(); // Modify this according to your preferred time format
    },
  },
};
</script>
