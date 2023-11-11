import { DEFAULT_TOAST_TIMEOUT } from '@/config.js';
import { defineStore } from 'pinia';
import { ref } from 'vue';

const DEFAULT_TOAST_CLOSEABLE = false;

/**
 * @typedef {"default" | "info" | "success" | "warning"| "error"} NotificationType
 *
 * @typedef {object} Notification
 * @property {number} id - The unique id of the notification.
 * @property {string} message - The message to display in the notification.
 * @property {NotificationType} type - The type of notification.
 * @property {number} timeout - The timeout of the notification.
 * @property {ReturnType<typeof setTimeout>} [timeoutID] - The timeout id of the notification.
 * @property {boolean} closeable - Whether the notification can be closed.
 *
 * @typedef {object} State
 * @property {Notification[]} notifications - The notifications to display.
 * @property {Notification[]} notificationsArchive - The notifications that have been displayed.
 *
 * @typedef {object} ToastOptions
 * @property {number} [timeout] - The time the notification will be displayed.
 * @property {boolean} [closeable] - Whether the notification can be closed.
 */

let toastAIID = 0;

export const useToastStore = defineStore('toast', () => {
  const notifications = ref(/** @type {Notification[]} */ ([]));
  const notificationsArchive = ref(/** @type {Notification[]} */ ([]));

  /**
   * @param {Notification} notification
   */
  function remove(notification) {
    const nots = /** @type {Notification[]} */ ([]);
    for (let i = 0; i < notifications.value.length; i++) {
      if (notifications.value[i].id !== notification.id) {
        nots.push(notifications.value[i]);
      }
    }
    notifications.value = nots;
    notificationsArchive.value.push(notification);
    clearTimeout(notification.timeoutID);
  }

  /**
   * @param {Notification} notification
   */
  function _toast(notification) {
    notifications.value.push(notification);
    notification.timeoutID = setTimeout(remove, notification.timeout, notification);
  }

  /**
   * @param {string} message
   * @param {ToastOptions} [options]
   */
  function toast(message, options) {
    _toast({
      id: toastAIID++,
      message,
      type: 'default',
      timeout: options?.timeout ?? DEFAULT_TOAST_TIMEOUT,
      closeable: options?.closeable ?? DEFAULT_TOAST_CLOSEABLE
    });
  }

  /**
   * @param {string} message
   * @param {ToastOptions} [options]
   */
  function info(message, options) {
    _toast({
      id: toastAIID++,
      message,
      type: 'info',
      timeout: options?.timeout ?? DEFAULT_TOAST_TIMEOUT,
      closeable: options?.closeable ?? DEFAULT_TOAST_CLOSEABLE
    });
  }

  /**
   * @param {string} message
   * @param {ToastOptions} [options]
   */
  function success(message, options) {
    _toast({
      id: toastAIID++,
      message,
      type: 'success',
      timeout: options?.timeout ?? DEFAULT_TOAST_TIMEOUT,
      closeable: options?.closeable ?? DEFAULT_TOAST_CLOSEABLE
    });
  }

  /**
   * @param {string} message
   * @param {ToastOptions} [options]
   */
  function warning(message, options) {
    _toast({
      id: toastAIID++,
      message,
      type: 'warning',
      timeout: options?.timeout ?? DEFAULT_TOAST_TIMEOUT,
      closeable: options?.closeable ?? DEFAULT_TOAST_CLOSEABLE
    });
  }

  /**
   * @param {string} message
   * @param {ToastOptions} [options]
   */
  function error(message, options) {
    _toast({
      id: toastAIID++,
      message,
      type: 'error',
      timeout: options?.timeout ?? DEFAULT_TOAST_TIMEOUT,
      closeable: options?.closeable ?? DEFAULT_TOAST_CLOSEABLE
    });
  }

  return {
    notifications,
    notificationsArchive,
    remove,
    toast,
    info,
    success,
    warning,
    error
  };
});
