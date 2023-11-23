<script setup>
  import PaginationBar from '@/components/PaginationBar.vue';
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { requestStatus } from '@/utils/enums';
  import { onBeforeMount, ref, watch } from 'vue';
  import { useRouter } from 'vue-router';

  const props = defineProps({
    request_id: String
  });

  const PER_PAGE = 2;

  const router = useRouter();
  const toastStore = useToastStore();
  const userStore = useUserStore();

  /**
   * @typedef {{
   *  id: number,
   *  title: string,
   *  creation_date: string,
   *  close_date: string,
   *  status: import('@/utils/enums').RequestStatus,
   *  description: string,
   *  user_id: number,
   * }} ServiceRequest
   */

  /** @type {import('vue').Ref<ServiceRequest|undefined>} */
  const request = ref();

  /**
   * @typedef {{
   *  note: {
   *    id: number,
   *    text: string,
   *    creation_date: string,
   *  },
   *  user: {
   *    id: number,
   *    username: string,
   *    email: string,
   *    is_active: boolean
   *  },
   * }} Note
   */

  /** @type {import('vue').Ref<Note[]>} */
  const notes = ref([]);
  const loading = ref(false);
  const notesPage = ref(1);
  /** @type {import('vue').Ref<number | undefined>} */
  const notesPerPage = ref(PER_PAGE);
  const notesTotal = ref(0);

  const requestStatusBadgeClasses = {
    [requestStatus.ACCEPTED]: 'badge-success',
    [requestStatus.REJECTED]: 'badge-error',
    [requestStatus.IN_PROCESS]: 'badge-primary',
    [requestStatus.FINISHED]: 'badge-info',
    [requestStatus.CANCELED]: 'badge-neutral'
  };

  onBeforeMount(async () => {
    await APIService.get(`/me/requests/${props.request_id}`, {
      onJSON(json) {
        request.value = json;
      },
      onFailure(response) {
        console.error('failed to load request ', response);
        if (response.status == 403) {
          router.push('/me/requests');
          return;
        }
        toastStore.error('No se pudo cargar la solicitud de servicio');
        router.push('/me/requests');
      },
      onError(error) {
        console.error('error loading request ', error);
        toastStore.error('No se pudo cargar la solicitud de servicio');
        router.push('/me/requests');
      }
    });
    await loadNotes();
  });

  function loadNotes() {
    loading.value = true;
    let url = `/me/requests/${props.request_id}/notes?page=${notesPage.value}`;
    if (notesPerPage.value) {
      url += '&per_page=' + notesPerPage.value;
    }

    return APIService.get(url, {
      onJSON(json) {
        notes.value = json.data;
        notesPerPage.value = json.per_page;
        notesTotal.value = json.total;
        console.log('notes', notes.value);
        console.log('request', request.value);
      },
      onFailure() {
        notes.value = [];
        notesTotal.value = 0;
        toastStore.error('No se pudieron cargar las notas');
      },
      onError() {
        notes.value = [];
        notesTotal.value = 0;
        toastStore.error('No se pudieron cargar las notas');
      },
      afterRequest() {
        loading.value = false;
      }
    });
  }

  watch(notesPage, () => {
    loadNotes();
  });

  /** @type {import('vue').Ref<Note[]>} */
  const notesHistory = ref([]);

  watch(notes, () => {
    notesHistory.value.push(...notes.value);
  });
  // watch(
  //   [requestsPage, filterRequestOrder, filterRequestStatus],
  //   () => {
  //     console.log('watching');
  //     loading.value = true;
  //     let url = `/me/requests?page=${requestsPage.value}`;
  //     if (requestsPerPage.value) {
  //       url += '&per_page=' + requestsPerPage.value;
  //     }
  //     if (filterRequestStatus.value !== 'Todos') {
  //       url += '&status=' + filterRequestStatus.value;
  //     }
  //     url += '&order=' + filterRequestOrder.value;

  //     APIService.get(url, {
  //       onJSON(json) {
  //         requests.value = json.data;
  //         requestsPerPage.value = json.per_page;
  //         requestsTotal.value = json.total;
  //       },
  //       onFailure() {
  //         requests.value = [];
  //         requestsTotal.value = 0;
  //         toastStore.error('No se pudieron cargar las solicitudes');
  //       },
  //       onError() {
  //         requests.value = [];
  //         requestsTotal.value = 0;
  //         toastStore.error('No se pudieron cargar las solicitudes');
  //       },
  //       afterRequest() {
  //         loading.value = false;
  //       }
  //     });
  //   },
  //   { immediate: true }
  // );
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="flex flex-col p-2 py-4 md:py-8">
      <div class="flex flex-col md:flex-row justify-center items-center">
        <h1 class="text-2xl md:text-3xl font-bold leading-relaxed text-center">
          Solicitud de Servicio
        </h1>
        <button
          class="btn btn-primary ml-2"
          @click="
            notesHistory = [];
            notesPage = 1;
            loadNotes();
          "
        >
          Resetear
        </button>
      </div>
      <div class="flex flex-wrap gap-4 justify-center my-4"></div>

      <div class="my-4">
        <p
          v-show="loading"
          class="flex justify-center items-center text-sm font-medium text-neutral-500"
        >
          Cargando Notas...
        </p>
        <p
          v-show="!loading && notes.length === 0"
          class="flex justify-center items-center text-sm font-medium text-neutral-500"
        >
          No has realizado solicitudes
        </p>
        <ul
          v-show="notesHistory.length > 0"
          class="flex flex-col-reverse max-w-3xl mx-auto md:h-[50vh] overflow-auto"
        >
          <li v-for="note in notesHistory" :key="note.note.id">
            <div
              class="chat"
              :class="note.user.id === request?.user_id ? 'chat-end' : 'chat-start'"
            >
              <div class="chat-header">
                {{ note.user.username }}
                <time class="text-xs opacity-50">{{ note.note.creation_date }}</time>
              </div>
              <div class="chat-bubble chat-bubble-primary bg-base-200">
                {{ note.note.text }}
              </div>
            </div>
          </li>
        </ul>
        <!-- <ul
          v-show="notesHistory.length > 0"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 px-4 md:px-2"
        >
          <li v-for="note in notesHistory" :key="note.note.id">
            <div
              class="card card-compact bg-base-100 text-primary-content ring-1 ring-primary/50 shadow-md transition duration-150 hover:ring-2 hover:ring-primary hover:shadow-lg"
            >
              <div class="card-body">
                <h3 class="card-title text-base md:text-lg">{{ note.user.username }}</h3>
                <p class="text-pretty">
                  {{ note.note.text }}
                </p>
                <div class="card-actions justify-between">
                  <div class="badge self-center">
                    {{ note.note.creation_date }}
                  </div>
                  <div class="badge self-center">
                    {{ note.note.id }}
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul> -->
      </div>

      <div class="mx-auto mt-4" :class="{ hidden: notesTotal === 0 }">
        <PaginationBar
          v-model:value="notesPage"
          :total="notesTotal"
          :per-page="notesPerPage"
          :loading="loading"
        />
      </div>
    </main>
  </div>
</template>
