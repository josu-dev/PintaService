/**
 * API URL to be used in the application.
 * @type {string}
 */
export const API_URL =
  import.meta.env.VITE_API_URL ?? 'https://admin-grupo04.proyecto2023.linti.unlp.edu.ar/api';

/**
 * Default timeout for toast notifications.
 * @type {3000}
 */
export const DEFAULT_TOAST_TIMEOUT = 3000;

/**
 * Default mode for api maintenance failure handling.
 * @type {import('@/utils/api').MaintenanceFailureOptions}
 */
export const DEFAULT_API_MAINTEINANCE_FAILURE = 'toast';
