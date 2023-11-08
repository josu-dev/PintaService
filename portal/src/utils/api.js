import { apiURL } from '../config.js';


export class APIService {
  static #apiURL = apiURL;

  static async get(path) {
    const response = await fetch(`${this.#apiURL}${path}`,{
    headers: {
      'Authorization': 'Bearer 1',
    }});
    return response.json();
  }

  static async post(path, body) {
    const response = await fetch(`${this.#apiURL}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 12'
      },
      body: JSON.stringify(body),
    });

    return response.json();
  }
}
