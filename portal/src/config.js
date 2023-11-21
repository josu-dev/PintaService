/**
 * Default timeout for toast notifications.
 */
export const DEFAULT_TOAST_TIMEOUT = 3000;

/**
 * API URL to be used in the application.
 * @type {string}
 */
export const API_URL =
  import.meta.env.VITE_API_URL ?? 'https://admin-grupo04.proyecto2023.linti.unlp.edu.ar/api';

/**
 * Default key for the jwt error message.
 */
export const DEFAULT_API_JWT_ERROR_MESSAGE_KEY = 'jwt_error_message';

/**
 * Default mode for api jwt error handling.
 * @type {import('@/utils/api').JWTErrorOptions}
 */
export const DEFAULT_API_JWT_ERROR = 'toast';

/**
 * Default mode for api maintenance error handling.
 * @type {import('@/utils/api').MaintenanceErrorOptions}
 */
export const DEFAULT_API_MAINTEINANCE_ERROR = 'toast';
