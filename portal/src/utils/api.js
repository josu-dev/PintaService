import {
  BACKEND_API_URL,
  DEFAULT_API_JWT_ERROR,
  DEFAULT_API_JWT_ERROR_MESSAGE_KEY,
  DEFAULT_API_MAINTEINANCE_ERROR
} from '@/config.js';

/**
 * @typedef {'toast' | 'fail' | 'ignore' | 'throw'} MaintenanceErrorOptions
 */

/**
 * @typedef {'toast' | 'fail' | 'ignore' | 'throw'} JWTErrorOptions
 */

/**
 * @typedef {Object} GetOptions
 * @property {(json: any) => void} [onJSON] - The callback for when the API returns JSON data.
 * @property {(response: Response) => void} [onFailure] - The callback for when the API returns a non-200 response.
 * @property {(error: unknown) => void} [onError] - The callback for when an error occurs.
 * @property {MaintenanceErrorOptions} [maintenanceError] - The option for how to handle maintenance failures.
 * @property {JWTErrorOptions} [jwtError] - The option for how to handle JWT errors.
 * @property {() => void} [afterRequest] - The callback for after the request is made, regardless of whether it succeeded or not.
 */

/**
 * @typedef {Object} PostOptions
 * @property {any} body - The body of the POST request.
 * @property {(json: any) => void} [onJSON] - The callback for when the API returns JSON data.
 * @property {(response: Response) => void} [onFailure] - The callback for when the API returns a non-200 response.
 * @property {(error: unknown) => void} [onError] - The callback for when an error occurs.
 * @property {MaintenanceErrorOptions} [maintenanceError] - The option for how to handle maintenance failures.
 * @property {JWTErrorOptions} [jwtError] - The option for how to handle JWT errors.
 * @property {() => void} [afterRequest] - The callback for after the request is made, regardless of whether it succeeded or not.
 */

const JWT_LS_KEY = 'LAST_JWT';

/**
 * A class for making requests to the API and handling the responses.
 */
export class APIService {
  static apiURL = BACKEND_API_URL;
  /** @type {Record<string, string>} */
  static defaultHeaders = {};

  /**
   * The default handler for when a maintenance error occurs.
   *
   * @param {Response} response - The original response from the API.
   */
  static onMaintenanceError(response) {
    throw new Error('Method not implemented.');
  }

  /**
   * The default handler for when a JWT error occurs.
   *
   * @param {Response} response - The original response from the API.
   */
  static onJWTError(response) {
    throw new Error('Method not implemented.');
  }

  /**
   * Gets JSON data from the API at the specified endpoint.
   *
   * @param {string} path - The path of the API endpoint to fetch data from.
   * @param {GetOptions} [options] - The options for handling the API response.
   */
  static async get(path, options) {
    if (!options) {
      options = {};
    }
    if (!options.maintenanceError) {
      options.maintenanceError = DEFAULT_API_MAINTEINANCE_ERROR;
    }
    if (!options.jwtError) {
      options.jwtError = DEFAULT_API_JWT_ERROR;
    }

    let data;
    try {
      const response = await fetch(`${APIService.apiURL}${path}`, {
        headers: { ...APIService.defaultHeaders }
      });
      if (!response.ok) {
        if (response.status === 503) {
          if (options.maintenanceError === 'ignore') {
            return;
          }
          if (options.maintenanceError === 'toast') {
            APIService.onMaintenanceError(response);
            return;
          }
          if (options.maintenanceError === 'throw') {
            throw new Error(response.statusText);
          }
        } else if (response.headers.get('content-type')?.startsWith('application/json')) {
          const json = await response.json();
          if (json[DEFAULT_API_JWT_ERROR_MESSAGE_KEY]) {
            if (options.jwtError === 'ignore') {
              return;
            }
            if (options.jwtError === 'toast') {
              APIService.onJWTError(response);
              return;
            }
            if (options.jwtError === 'throw') {
              throw new Error(response.statusText);
            }
          }
        }

        options.onFailure?.(response);
        return;
      }

      data = await response.json();
      options.onJSON?.(data);
    } catch (error) {
      if (options.onError) {
        options.onError(error);
        return;
      }

      throw error;
    } finally {
      options.afterRequest?.();
    }

    return data;
  }

  /**
   * Posts JSON data to the API at the specified endpoint.
   *
   * @param {string} path - The path of the API endpoint to post data to.
   * @param {PostOptions} options - The options for handling the API response.
   */
  static async post(path, options) {
    if (!options.maintenanceError) {
      options.maintenanceError = DEFAULT_API_MAINTEINANCE_ERROR;
    }
    if (!options.jwtError) {
      options.jwtError = DEFAULT_API_JWT_ERROR;
    }

    let data;
    try {
      const response = await fetch(`${APIService.apiURL}${path}`, {
        method: 'POST',
        headers: {
          ...APIService.defaultHeaders,
          'Content-Type': 'application/json'
        },
        body: options.body === undefined ? undefined : JSON.stringify(options.body)
      });
      if (!response.ok) {
        if (response.status === 503) {
          if (options.maintenanceError === 'ignore') {
            return;
          }
          if (options.maintenanceError === 'toast') {
            APIService.onMaintenanceError(response);
            return;
          }
          if (options.maintenanceError === 'throw') {
            throw new Error(response.statusText);
          }
        } else if (response.headers.get('content-type')?.startsWith('application/json')) {
          const json = await response.json();
          if (json[DEFAULT_API_JWT_ERROR_MESSAGE_KEY]) {
            if (options.jwtError === 'ignore') {
              return;
            }
            if (options.jwtError === 'toast') {
              APIService.onJWTError(response);
              return;
            }
            if (options.jwtError === 'throw') {
              throw new Error(response.statusText);
            }
          }
        }

        options.onFailure?.(response);
        return;
      }

      data = await response.json();
      options.onJSON?.(data);
    } catch (error) {
      if (options.onError) {
        options.onError(error);
        return;
      }

      throw error;
    } finally {
      options.afterRequest?.();
    }

    return data;
  }

  /**
   * Sets the JWT token to be used in future API requests.
   *
   * @param {string} token - The JWT token to use.
   */
  static setJWT(token) {
    APIService.defaultHeaders.Authorization = `JWT ${token}`;
    try {
      localStorage.setItem(JWT_LS_KEY, token);
    } catch (error) {
      console.error('Error while saving JWT token to local storage: ', error);
    }
  }

  /**
   * Clears the JWT token from local storage and removes it from being used in future API requests.
   */
  static clearJWT() {
    try {
      localStorage.removeItem(JWT_LS_KEY);
    } catch (error) {
      console.error('Error while removing JWT token from local storage: ', error);
    }
    delete APIService.defaultHeaders.Authorization;
  }

  /**
   * Gets the JWT token from local storage and sets it to be used in future API requests.
   * Returns true if the JWT token was found in local storage, false otherwise.
   *
   * @returns {boolean}
   */
  static setJWTFromLS() {
    const token = localStorage.getItem(JWT_LS_KEY);
    if (token === null) {
      return false;
    }
    APIService.setJWT(token);
    return true;
  }

  /**
   * Saves the current JWT token to local storage.
   */
  static saveJWTToLS() {
    const JWTHeader = APIService.defaultHeaders.Authorization;
    if (!JWTHeader) {
      return;
    }
    const token = JWTHeader.split(' ')[1];
    try {
      localStorage.setItem(JWT_LS_KEY, token);
    } catch (error) {
      console.error('Error while saving JWT token to local storage: ', error);
    }
  }
}
