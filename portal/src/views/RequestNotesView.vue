<script setup>
  import GoBackButton from '@/components/GoBackButton.vue';
  import IconListend from '@/components/icons/IconListend.vue';
  import IconLoader from '@/components/icons/IconLoader.vue';
  import IconPlus from '@/components/icons/IconPlus.vue';
  import IconSend from '@/components/icons/IconSend.vue';
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { requestStatus } from '@/utils/enums';
  import { computed, nextTick, onBeforeMount, onBeforeUnmount, onMounted, ref, watch } from 'vue';
  import { RouterLink, useRouter } from 'vue-router';

  const props = defineProps({
    request_id: String
  });

  const PER_PAGE = undefined;

  const router = useRouter();
  const toastStore = useToastStore();
  const userStore = useUserStore();

  /** @type {import('vue').Ref<HTMLDivElement | undefined>} */
  const chatBottomEl = ref();
  const chatBottomOutOfView = ref(false);

  watch(chatBottomEl, (el) => {
    if (el) {
      observer.observe(el);
    }
  });

  /** @type {IntersectionObserver} */
  let observer;

  onMounted(() => {
    observer = new IntersectionObserver(
      (entries) => {
        chatBottomOutOfView.value = !entries[0].isIntersecting;
      },
      { threshold: 0.25 }
    );
  });

  onBeforeUnmount(() => {
    if (chatBottomEl.value) {
      observer.unobserve(chatBottomEl.value);
    }
  });

  const initialized = ref(false);
  /**
   * @typedef {{
   *  id: number,
   *  title: string,
   *  creation_date: string,
   *  close_date: string,
   *  status: import('@/utils/enums').RequestStatus,
   *  description: string,
   *  user_id: number,
   *  service_id: number,
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
   *  }
   * }} Note
   *
   * @typedef {Note & {
   *  meta: {
   *    is_owner: boolean
   *  }
   * }} NoteHistory
   */

  /** @type {import('vue').Ref<Note[]>} */
  const notes = ref([]);
  const loadingNotes = ref(false);
  const notesPage = ref(1);
  /** @type {import('vue').Ref<number | undefined>} */
  const notesPerPage = ref(PER_PAGE);
  /** @type {import('vue').Ref<number | undefined>} */
  const notesTotal = ref();

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
    loadingNotes.value = true;
    let url = `/me/requests/${props.request_id}/notes?page=${notesPage.value}`;
    if (notesPerPage.value) {
      url += '&per_page=' + notesPerPage.value;
    }

    return APIService.get(url, {
      onJSON(json) {
        notes.value = json.data;
        notesPerPage.value = json.per_page;
        notesTotal.value = json.total;
        initialized.value = true;
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
        loadingNotes.value = false;
      }
    });
  }

  function loadOlderNotes() {
    loadingNotes.value = true;
    const nextPage = notesPage.value + 1;
    let url = `/me/requests/${props.request_id}/notes?page=${nextPage}`;
    if (notesPerPage.value) {
      url += '&per_page=' + notesPerPage.value;
    }

    return APIService.get(url, {
      onJSON(json) {
        notes.value = json.data;
        notesPerPage.value = json.per_page;
        notesTotal.value = json.total;
        if (notesPage.value * (notesPerPage.value || 1) < (notesTotal.value || 1)) {
          notesPage.value = nextPage;
        }
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
        loadingNotes.value = false;
      }
    });
  }

  /** @type {import('vue').Ref<NoteHistory[]>} */
  const notesHistory = ref([]);

  watch(notes, () => {
    const owner_id = request.value?.user_id;
    for (const note of notes.value) {
      notesHistory.value.push({
        ...note,
        meta: {
          is_owner: note.user.id === owner_id
        }
      });
    }
  });

  const requestIsActive = computed(() => {
    const status = request.value?.status;
    return status === requestStatus.ACCEPTED || status === requestStatus.IN_PROCESS;
  });
  const requestIsFinished = computed(() => {
    const status = request.value?.status;
    return (
      status === requestStatus.FINISHED ||
      status === requestStatus.CANCELED ||
      status === requestStatus.REJECTED
    );
  });
  const allNotesLoaded = computed(() => {
    return notesHistory.value.length === notesTotal.value;
  });

  const noteForm = ref({
    text: ''
  });
  const submitingNote = ref(false);

  function submitNote(event) {
    if (noteForm.value.text.length === 0) {
      return;
    }
    submitingNote.value = true;
    APIService.post(`/me/requests/${props.request_id}/notes`, {
      body: {
        text: noteForm.value.text
      },
      onJSON(json) {
        noteForm.value.text = '';
        notesTotal.value = (notesTotal.value ?? 0) + 1;
        notesHistory.value.unshift({
          note: json,
          user: {
            id: json.user_id,
            username: userStore.user?.username || '',
            email: userStore.user?.email || '',
            is_active: true
          },
          meta: {
            is_owner: true
          }
        });

        nextTick(() => {
          chatBottomEl.value?.scrollIntoView({ behavior: 'smooth' });
        });
      },
      onFailure() {
        toastStore.error('No se pudo enviar la nota');
      },
      onError() {
        toastStore.error('No se pudo enviar la nota');
      },
      afterRequest() {
        submitingNote.value = false;
      }
    });
  }
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="h-full flex flex-col px-2 py-4 md:py-8">
      <template v-if="!initialized">
        <div class="flex-1 grid place-items-center">
          <p
            class="text-lg md:text-xl flex flex-wrap max-w-[80%] justify-center text-balance items-center gap-2 font-semibold text-center text-neutral-800"
          >
            <IconLoader class="animate-spin inline-flex" />
            <span class=""> Cargando solicitud de servicio </span>
          </p>
        </div>
      </template>
      <template v-else>
        <div class="flex-none flex flex-col justify-center items-center">
          <h1 class="text-2xl md:text-3xl font-bold text-center text-primary leading-relaxed">
            Solicitud de Servicio
          </h1>
          <div class="mt-2 md:mt-4 flex flex-wrap justify-center gap-x-2">
            <p class="text-lg md:text-xl font-semibold text-neutral-800">
              {{ request?.title }}
            </p>
            <span
              class="badge badge-sm md:badge-md mt-1"
              :class="requestStatusBadgeClasses[request?.status]"
            >
              {{ request?.status }}
            </span>
          </div>
          <p
            class="mt-1 md:mt-2 text-sm md:text-base text-neutral-600 text-center text-balance line-clamp-2 max-w-[90%] xs:max-w-[75%]"
          >
            {{ request?.description }}
          </p>
        </div>

        <div class="flex-1 flex flex-col my-4 md:my-6">
          <section
            class="flex flex-col w-full xs:max-w-[95%] md:max-w-[80%] mx-auto bg-base-100 ring-1 ring-primary/50 rounded-md"
          >
            <div class="overflow-hidden rounded-md">
              <ul class="flex flex-col-reverse h-[50vh] overflow-auto rounded-md py-2">
                <div ref="chatBottomEl"></div>
                <li v-for="note in notesHistory" :key="note.note.id">
                  <div class="chat" :class="note.meta.is_owner ? 'chat-end' : 'chat-start'">
                    <div class="chat-header">
                      {{ note.user.username }}
                      <time class="text-xs text-neutral-400">{{ note.note.creation_date }}</time>
                    </div>
                    <div class="chat-bubble chat-bubble-primary bg-base-200">
                      {{ note.note.text }}
                    </div>
                  </div>
                </li>
                <li class="flex flex-col justify-center items-center mt-2">
                  <p
                    v-show="allNotesLoaded"
                    class="my-4 text-sm font-medium text-center text-neutral-600"
                  >
                    Comienzo de la solicitud de servicio <br />
                    <time class="text-xs text-neutral-400">{{ request?.creation_date }}</time>
                  </p>
                  <p v-show="notesTotal === 0" class="my-4 text-sm font-medium text-neutral-600">
                    No has realizado solicitudes
                  </p>
                  <button
                    class="btn btn-primary btn-ghost btn-sm my-4 normal-case ring-1 ring-primary-content/50"
                    v-show="!allNotesLoaded"
                    :disabled="loadingNotes"
                    @click="loadOlderNotes()"
                  >
                    <IconLoader v-show="loadingNotes" class="animate-spin xs:mr-2" />
                    <IconPlus v-show="!loadingNotes" class="xs:mr-2" />
                    <span class="sr-only xs:not-sr-only">Notas Anteriores</span>
                  </button>
                </li>
              </ul>

              <div class="border-t border-primary/50 bg-base-200/25">
                <form
                  class="grid grid-cols-[auto_1fr_auto] gap-x-1 md:gap-x-2 p-1 md:px-2 items-center justify-center"
                  @submit.prevent="submitNote"
                >
                  <button
                    :disabled="!chatBottomOutOfView"
                    @click="() => chatBottomEl?.scrollIntoView({ behavior: 'smooth' })"
                    type="button"
                    class="btn btn-ghost p-2"
                  >
                    <IconListend />
                  </button>
                  <textarea
                    class="textarea border-primary/50 textarea-sm w-full leading-normal resize-none"
                    v-model="noteForm.text"
                    :disabled="!requestIsActive"
                    required
                    minlength="1"
                    placeholder="Nueva nota"
                  ></textarea>

                  <button type="submit" :disabled="!requestIsActive" class="btn btn-ghost p-2">
                    <IconSend v-show="!submitingNote" />
                    <IconLoader v-show="submitingNote" class="animate-spin" />
                  </button>
                </form>
              </div>
            </div>
          </section>

          <div class="flex flex-wrap justify-center gap-2 md:gap-4 mt-auto pt-2">
            <GoBackButton
              class="btn-sm w-40 max-w-[95%] btn-ghost bg-base-content bg-opacity-10 normal-case"
            >
              Volver a Solicitudes
            </GoBackButton>

            <RouterLink
              v-if="request?.service_id !== undefined"
              :to="`/services/${request.service_id}`"
              class="btn btn-sm w-40 max-w-[95%] btn-primary normal-case"
            >
              Ver Servicio
            </RouterLink>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>
