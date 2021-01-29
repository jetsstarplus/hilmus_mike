{% load static %}
var cacheName = 'mikecacheV2';
var appShellFiles = [
  '{% url "pages:index" %}',
  '{% url "pages:contact" %}',
  '{% url "pages:shop" %}',

  '{% static "pages/mike/HOME.webp" %}',
  "{% static 'pages/mike/home2.webp' %}",
  "{% static 'pages/mike/artmm.webp' %}",
  "{% static 'images_africa.jpg' %}",
  "{% static 'SDG-Logo.png' %}",

  '{% url "article:post" %}',
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
