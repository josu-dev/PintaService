import { API_URL, DEFAULT_API_MAINTEINANCE_FAILURE } from '@/config.js';

/**
 * @typedef {'toast' | 'fail' | 'ignore' | 'throw'} MaintenanceFailureOptions
 */

/**
 * A class for making requests to the API and handling the responses.
 */
export class APIService {
  static apiURL = API_URL;


  /**
   * The default handler for when a maintenance failure occurs.
   *
   * @param {Response} response - The original response from the API.
   */
  static onMaintenanceFailure(response) {
    throw new Error('Method not implemented.');
  }

  /**
   * Gets JSON data from the API at the specified endpoint.
   *
   * @param {string} path - The path of the API endpoint to fetch data from.
   * @param {{
   *  onJSON: (json: any) => void,
   *  onFailure?: (response: Response) => void,
   *  onError?: (error: unknown) => void,
   *  maintenanceFailure?: MaintenanceFailureOptions,
   *  token?: string,
   * }} options - The options for handling the API response.
   */
  static async get(path, options) {
    if (!options.maintenanceFailure) {
      options.maintenanceFailure = DEFAULT_API_MAINTEINANCE_FAILURE;
    }

    let data;
    try {
      const token = options.token || localStorage.getItem('token');
      const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      };

      const response = await fetch(`${APIService.apiURL}${path}`, {
        headers,
      });
      if (!response.ok) {
        if ((response.status === 401) && ((localStorage.getItem('token')!== null))){
          localStorage.removeItem('token');
        }
        if (response.status === 503) {
          if (options.maintenanceFailure === 'ignore') {
            return;
          }
          if (options.maintenanceFailure === 'toast') {
            APIService.onMaintenanceFailure(response);
            return;
          }
          if (options.maintenanceFailure === 'throw') {
            throw new Error(response.statusText);
          }
        }

        options.onFailure?.(response);
        return;
      }

      data = await response.json();
      options.onJSON(data);
    } catch (error) {
      if (options.onError) {
        options.onError(error);
        return;
      }

      throw error;
    }

    return data;
  }

  /**
   * Posts JSON data to the API at the specified endpoint.
   *
   * @param {string} path - The path of the API endpoint to post data to.
   * @param {{
   *  body: any,
   *  onJSON: (json: any) => void,
   *  onFailure?: (response: Response) => void,
   *  onError?: (error: unknown) => void,
   *  maintenanceFailure?: MaintenanceFailureOptions,
   *  token?: string,
   * }} options - The options for handling the API response.
   */
  static async post(path, options) {
    if (!options.maintenanceFailure) {
      options.maintenanceFailure = DEFAULT_API_MAINTEINANCE_FAILURE;
    }

    let data;
    try {
      const token = options.token || localStorage.getItem('token');
      const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      };
      const response = await fetch(`${APIService.apiURL}${path}`, {
        method: 'POST',
        headers,
        body: options.body === undefined ? undefined : JSON.stringify(options.body)
      });
      if (!response.ok) {
        if ((response.status === 401) && ((localStorage.getItem('token')!== null))){
            localStorage.removeItem('token');
        }
        if (response.status === 503) {
          if (options.maintenanceFailure === 'ignore') {
            return;
          }
          if (options.maintenanceFailure === 'toast') {
            APIService.onMaintenanceFailure(response);
            return;
          }
          if (options.maintenanceFailure === 'throw') {
            throw new Error(response.statusText);
          }
        }

        options.onFailure?.(response);
        return;
      }

      data = await response.json();
      options.onJSON(data);
    } catch (error) {
      if (options.onError) {
        options.onError(error);
        return;
      }

      throw error;
    }

    return data;
  }
}
