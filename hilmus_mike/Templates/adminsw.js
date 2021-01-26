
var cacheName = 'mikeadmincache';
var appShellFiles = [
  '{% url "home:lipa_na_mpesa_form" %}',
  '{% url "home:paypal" %}',

  '{% url "mike_admin:home" %}',
  '{% url "mike_admin:profile" %}',

  '{% url "mike_admin:testimonials" %}',

  '{% url "mike_admin:terms" %}',

  '{% url "mike_admin:music" %}',

  '{% url "mike_admin:services" %}',

  '{% url "mike_admin:users" %}',

  '{% url "mike_admin:lipa" %}',
  '{% url "mike_admin:post_messages" %}',
  '{% url "mike_admin:payments" %}'

];

let contentToCache=appShellFiles

self.addEventListener('install', function(e) {
    console.log('[Service Worker] Install');
    e.waitUntil(
      caches.open(cacheName).then(function(cache) {
        console.log('[Service Worker] Caching all: app shell and content');
        return cache.addAll(contentToCache);
      })
    );
  });


  self.addEventListener('fetch', function(e) {
    e.respondWith(
      caches.match(e.request).then(function(r) {
        console.log('[Service Worker] Fetching resource: '+e.request.url);
        return r || fetch(e.request).then(function(response) {
          return caches.open(cacheName).then(function(cache) {
            console.log('[Service Worker] Caching new resource: '+e.request.url);
            cache.put(e.request, response.clone());
            return response;
          });
        });
      })
    );
  });
