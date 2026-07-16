# Vue.js & Angular Framework Architectures

While React and Next.js dominate modern web development, **Vue.js** and **Angular** are key enterprise frameworks featuring distinct design choices.

---

## 1. Vue.js: Reactive Proxies & Composition API

Vue uses a highly reactive design that wraps state variables inside ES6 **Proxies**. It automatically tracks variables accessed during rendering and updates components only when those specific variables change.

### Code Demonstration: Vue Composition API
```html
<script setup>
import { ref, onMounted } from 'vue';

// Reactive state declarations
const name = ref('');
const items = ref([]);

const addItem = () => {
  if (name.value.trim()) {
    items.value.push({ id: Date.now(), name: name.value });
    name.value = '';
  }
};
</script>

<template>
  <div class="vue-container">
    <input v-model="name" placeholder="Type resource name" />
    <button @click="addItem">Add Resource</button>

    <ul>
      <!-- Reactive list rendering using v-for directive -->
      <li v-for="item in items" :key="item.id">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>
```

---

## 2. Angular: Enterprise TypeScript Framework

Angular is a complete, opinionated framework written natively in TypeScript. It enforces a strict model-driven architecture, using class decorators, TypeScript-first types, and built-in dependency injection services.

### Code Demonstration: Component & Services
```typescript
// item.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root' // Instantiated once globally as a singleton
})
export class ItemService {
  constructor(private http: HttpClient) {}

  getItems(): Observable<any[]> {
    return this.http.get<any[]>('/api/items');
  }
}
```

```typescript
// item.component.ts
import { Component, OnInit } from '@angular/core';
import { ItemService } from './item.service';

@Component({
  selector: 'app-items',
  template: `
    <div class="angular-list">
      <h3>Angular Catalog</h3>
      <li *ngFor="let item of items">
        {{ item.name }}
      </li>
    </div>
  `
})
export class ItemComponent implements OnInit {
  items: any[] = [];

  // Service injected via constructor dependency injection
  constructor(private itemService: ItemService) {}

  ngOnInit(): void {
    this.itemService.getItems().subscribe(data => this.items = data);
  }
}
```
