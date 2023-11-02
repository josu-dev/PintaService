<script setup>
  import { ref } from 'vue'
  import { apiURL } from '../config.js'

  const user = ref('')
  const password = ref('')
  const apiEndpoint = `${apiURL}/auth`

  /** @type {(event:SubmitEvent) => Promise<void>} */
  async function submitLogin(event) {
    event.preventDefault()

    const response = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user: user.value,
        password: password.value
      })
    })

    const data = await response.json()
    console.log(data)
    // Handle the response data here
  }
</script>

<template>
  <main>
    <h1>Login</h1>
    <form class="flex flex-col gap-4 max-w-md text-zinc-200" @submit="submitLogin">
      <div class="flex flex-col">
        <label for="user">Email</label>
        <input v-model="user" type="email" id="user" name="user" class="bg-zinc-800" />
      </div>
      <div class="flex flex-col">
        <label for="password">Password</label>
        <input
          v-model="password"
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
