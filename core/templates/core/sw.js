// sw.js - Versão de Limpeza / Desativação
self.addEventListener('install', (event) => {
    self.skipWaiting(); // Força a ativação imediata do novo worker
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    return caches.delete(cacheName); // Apaga todos os caches antigos
                })
            );
        }).then(() => {
            return self.clients.claim(); // Assume o controle imediato das abas
        }).then(() => {
            // Opcional: força todas as abas a recarregarem limpas
            self.clients.matchAll({ type: 'window' }).then((clients) => {
                clients.forEach((client) => client.navigate(client.url));
            });
        })
    );
});