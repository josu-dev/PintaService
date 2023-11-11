import { API_URL } from '@/config.js';

/**
 * A class for making requests to the API and handling the responses.
 */
export class APIService {
  static apiURL = API_URL;

  /**
   * Gets JSON data from the API at the specified endpoint.
   *
   * @param {string} path - The path of the API endpoint to fetch data from.
   * @param {{
   *  onJSON: (json: any) => void,
   *  onFailure?: (result: Response) => void,
   *  onError?: (error: unknown) => void,
   * }} options - The options for handling the API response.
   */
  static async get(path, options) {
    let data;
    try {
      const response = await fetch(`${APIService.apiURL}${path}`, {
        headers: {
          Authorization: 'Bearer 1'
        }
      });
      if (!response.ok) {
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
   *  onFailure?: (result: Response) => void,
   *  onError?: (error: unknown) => void,
   * }} options - The options for handling the API response.
   */
  static async post(path, options) {
    let data;
    try {
      const response = await fetch(`${APIService.apiURL}${path}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer 1'
        },
        body: options.body === undefined ? undefined : JSON.stringify(options.body)
      });
      if (!response.ok) {
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
