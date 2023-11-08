<script setup>
  import { APIService } from '@/utils/api';
  import { ref } from 'vue';

  const form = ref({
    user: '',
    password: ''
  });

  /** @param {Event} event */
  async function submitLogin(event) {
    APIService.post('/auth', {
      body: form.value,
      onJSON(json) {
        console.log(json);
      },
      onFailure(response) {
        console.log(response);
      },
      onError(error) {
        console.log(error);
      }
    });
  }
</script>

<template>
  <main>
    <h1>Login</h1>
    <form class="flex flex-col gap-4 max-w-md text-zinc-200" @submit.prevent="submitLogin">
      <div class="flex flex-col">
        <label for="user">Email</label>
        <input v-model="form.user" type="email" id="user" name="user" class="bg-zinc-800" />
      </div>
      <div class="flex flex-col">
        <label for="password">Password</label>
        <input
          v-model="form.password"
          type="password"
          id="password"
          name="password"
          class="bg-zinc-800"
        />
      </div>
      <button type="submit" class="btn btn-success btn-sm">Login</button>
    </form>
  </main>
</template>
