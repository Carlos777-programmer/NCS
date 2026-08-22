self.addEventListener('fetch', function(event) {
  // Permite que o app funcione normalmente conectando ao servidor
  event.respondWith(fetch(event.request));
});