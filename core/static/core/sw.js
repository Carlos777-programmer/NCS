<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('{% static "core/sw.js" %}')
      .then(() => console.log('Service Worker registrado no login!'))
      .catch((err) => console.log('Erro:', err))
  }
</script>