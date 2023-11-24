import { logLevel } from '@/config';

const dev = import.meta.env.DEV;

/**
 * Logging utility (client-side).
 *
 * @type {Record<'info' | 'warn' | 'error' | 'debug', (where: string, ...args: any[]) => void>}
 */
export const log = {
  info(where, ...args) {
    if (dev || logLevel >= 3) {
      console['info'](`[${where}]`, ...args);
    }
  },
  warn(where, ...args) {
    if (dev || logLevel >= 2) {
      console['warn'](`[${where}]`, ...args);
    }
  },
  error(where, ...args) {
    if (logLevel >= 1) {
      console['error'](`[${where}]`, ...args);
    }
  },
  debug(where, ...args) {
    if (dev || logLevel >= 4) {
      console['debug'](`[${where}]`, ...args);
    }
  }
};
