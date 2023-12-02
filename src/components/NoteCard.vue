<template>
  <div class="card text-center">
    <div class="card-header">
      {{ info.grad }}
    </div>
    <div class="card-body p-0">
      <h5 class="card-title">{{ info.naziv_biljeske }}</h5>
      <p class="card-text">Tekst bilješke mog putovanja, datum.</p>
    </div>
    <div class="card-footer text-body-secondary">
      {{ info.vrijeme }}
    </div>
  </div>
</template>

<script>
export default {
  props: ['info'],
  name: 'NoteCard',
};
</script>
