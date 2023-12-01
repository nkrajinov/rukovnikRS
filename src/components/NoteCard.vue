<template>
  <div class="card text-center">
      <div class="card-header">
       Featured
      </div>
      <div class="card-body p-0">
       <h5 class="card-title">Special title treatment</h5>
       <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
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