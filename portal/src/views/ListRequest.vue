<script setup>

import { ref } from 'vue';
import { APIService } from '@/utils/api';

/**
 * @typedef {{
 *    title: string,
 *    creation_date: string,
 *    close_date: string,
 *    status: string,
 *    description: string,
 * }} RequestData[]
 */
/** @type {import('vue').Ref<RequestData[]>} */

const requestsList = ref([]);
const loading = ref(false);

let currentPage = ref(1);
let perPage = ref(0);
let totalRequest = ref(0);


const fetchRequests = () => {
    loading.value = true;
    const url = `/me/requests?page=${currentPage.value}&per_page=${perPage.value}`; // You can adjust the page and per_page values as needed
    APIService.get(url, {
        onJSON(json) {
            requestsList.value = json.data;
            currentPage.value = json.page;
            perPage.value = json.per_page;
            totalRequest.value = json.total;
            loading.value = false;
        },
        onFailure(response) {
            console.log('Request failed');
        },
        onError(error) {
            console.log(error);
        }
    });
};

fetchRequests();
const changePage = (page) => {
  if (page >= 1 && page <= Math.ceil(totalRequest.value / perPage.value)) {
    currentPage.value = page;
    fetchRequests();
  }
};

</script>

<template>
    <div class="h-full overflow-y-auto">
        <main class="text-center">
            <h1 class="text-4xl font-bold text-primary mt-4 mb-4">My Requests</h1>
            <div class="mx-auto max-w-md">
                <button @click="fetchRequests" class="btn btn-primary" :disabled="loading">
                    {{ loading ? 'Loading...' : 'Refresh' }}
                </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                <div v-for="request in requestsList" :key="request.title"
                    class="bg-white rounded-lg overflow-hidden shadow-md">
                    <div class="p-4">
                        <h2 class="text-lg font-bold text-gray-800">Title: {{ request.title }}</h2>
                        <p class="text-sm text-gray-600">Creation Date: {{ request.creation_date }}</p>
                        <p class="text-sm text-gray-600">Close Date: {{ request.close_date }}</p>
                        <p class="text-sm text-gray-600">Status: {{ request.status }}</p>
                        <p class="text-sm text-gray-600">Description: {{ request.description }}</p>
                    </div>
                </div>
            </div>

            <div class="mt-4">
                <div v-if="Math.ceil(totalRequest / perPage) > 0">
                    <button class="btn btn-primary m-1" v-for="page in Math.ceil(totalRequest / perPage)" :key="page"
                        @click="changePage(page)"
                        :class="{ 'bg-orange-600 text-orange-50': page === currentPage, 'bg-orange-200 text-zinc-800': page !== currentPage }">
                        {{ page }}
                    </button>
                    <p class="text-center">Página {{ currentPage }} de {{ Math.ceil(totalRequest / perPage) }}</p>
                </div>
                <div v-else-if="!loading" class="bg-white rounded-lg overflow-hidden shadow-md">
                    <div class="p-4">
                        <p class="text-lg font-bold text-gray-800">No se encontraron Pedidos</p>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>
