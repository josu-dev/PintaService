import { defineStore } from 'pinia';
import { ref } from 'vue';

/**
 * @typedef {object} UserProfile
 * @property {string} user - The username of the user.
 * @property {string} email - The email of the user.
 * @property {string} address - The address of the user.
 * @property {string} phone - The phone number of the user.
 * @property {import('@/utils/enums').DocumentTypes} document_type - The type of document of the user.
 * @property {string} document_number - The document number of the user.
 * @property {import('@/utils/enums').GenderOptions} gender - The gender of the user.
 * @property {string} gender_other - The other gender of the user if the gender is "Other".
 */

/**
 * @typedef {object} userRols
 * @property {boolean} [is_site_admin] - If the user is a site admin.
 * @property {boolean} [is_institution_owner] - If the user is an institution owner.
 */

/**
 * @typedef {object} User
 * @property {string} username - The username of the user.
 * @property {string} email - The email of the user.
 * @property {string} address - The address of the user.
 * @property {string} phone - The phone number of the user.
 * @property {import('@/utils/enums').DocumentTypes} document_type - The type of document of the user.
 * @property {string} document_number - The document number of the user.
 * @property {import('@/utils/enums').GenderOptions} gender - The gender of the user.
 * @property {string} gender_other - The other gender of the user if the gender is "Other".
 * @property {boolean} is_site_admin - If the user is a site admin.
 * @property {boolean} is_institution_owner - If the user is an institution owner.
 */

export const useUserStore = defineStore('user', () => {
  /** @type {import('vue').Ref<User | null>} */
  const user = ref(null);

  /**
   * @param {UserProfile} userProfile
   * @param {userRols} [userRol]
   * @returns {void}
   */
  function setUser(userProfile, userRol) {
    const isSiteAdmin = userRol?.is_site_admin === true;
    const isInstitutionOwner = userRol?.is_institution_owner === true;

    user.value = {
      username: userProfile.user,
      email: userProfile.email,
      address: userProfile.address,
      phone: userProfile.phone,
      document_type: userProfile.document_type,
      document_number: userProfile.document_number,
      gender: userProfile.gender,
      gender_other: userProfile.gender_other,
      is_site_admin: isSiteAdmin,
      is_institution_owner: isInstitutionOwner
    };
  }

  /**
   * @returns {void}
   */
  function clearUser() {
    user.value = null;
  }

  return { user, setUser, clearUser };
});
