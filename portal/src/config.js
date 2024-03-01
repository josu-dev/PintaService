/**
 * Default timeout for toast notifications.
 */
export const DEFAULT_TOAST_TIMEOUT = 3000;

/**
 * Base URL for the backend.
 * @type {string}
 */
export const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:5000';

/**
 * API URL for the backend.
 */
export const BACKEND_API_URL = `${BACKEND_BASE_URL}/api`;

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

/**
 * Default log level.
 *
 * - 0: No logs.
 * - 1: Errors.
 * - 2: Errors and warnings.
 * - 3: Errors, warnings and info.
 * - 4: Errors, warnings, info and debug.
 *
 * @type {number}
 */
export const logLevel = parseInt(import.meta.env.VITE_LOG_LEVEL || '2');
