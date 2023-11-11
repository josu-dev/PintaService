import { defineStore } from 'pinia';
import { ref } from 'vue';

/**
 * @typedef {object} User
 * @property {string} user - The username of the user.
 * @property {string} email - The email of the user.
 * @property {string} address - The address of the user.
 * @property {string} phone - The phone number of the user.
 * @property {import('@/utils/enums').DocumentTypes} document_type - The type of document of the user.
 * @property {string} document_number - The document number of the user.
 * @property {import('@/utils/enums').GenderOptions} gender - The gender of the user.
 * @property {string} gender_other - The other gender of the user if the gender is "Other".
 */

export const useUserStore = defineStore('user', () => {
  /** @type {import('vue').Ref<User | null>} */
  const user = ref(null);

  /** @param {User} newUser */
  function setUser(newUser) {
    user.value = newUser;
  }

  function clearUser() {
    user.value = null;
  }

  return { user, setUser, clearUser };
});
