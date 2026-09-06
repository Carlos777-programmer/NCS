self.addEventListener('install', (event) => {
    self.skipWaiting(); // Força a ativação imediata do novo worker
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    return caches.delete(cacheName); // Apaga caches antigos
                })
            );
        }).then(() => {
            return self.clients.claim(); // Assume o controle imediato das abas
        })
    );
});

// Evento disparado quando o servidor envia uma notificação Web Push
self.addEventListener('push', function (event) {
    if (!(self.Notification && self.Notification.permission === 'granted')) {
        return;
    }

    var data = {};
    if (event.data) {
        data = event.data.json();
    }

    var title = data.head || "NCS ERP - Alerta";
    var message = data.body || "Nova notificação do sistema.";
    var icon = data.icon || "";
    var url = data.url || "/";

    var options = {
        body: message,
        icon: icon,
        data: {
            url: url
        }
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Evento disparado quando o usuário clica na notificação que apareceu no celular/PC
self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});