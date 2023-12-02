<template>
  <div class="card text-center">
      <div class="card-header">
       Moje putovanje
      </div>
      <div class="card-body p-0">
       <h5 class="card-title">Moja bilješka</h5>
       <p class="card-text">Tekst bilješke mog putovanja, datum.</p>
      </div>
      <div class="card-footer text-body-secondary">
    2 days ago
       </div>
  </div>
</template>

<script>
export default {
  name: 'NoteCard',
  props: {
    msg: String
  }
}
</script>