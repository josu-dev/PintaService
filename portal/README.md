# Portal

The Portal module serves as the public application for requesting services available in the private [Admin](../admin/README.md) application.

## Quick Start

Ensure you have [Node.js](https://nodejs.org/en/) `v14.21.3` and [npm](https://www.npmjs.com/) installed before proceeding.

1. Install dependencies: Run `npm install`.
2. Create a `.env` file from the provided `.env.example`.
3. Run Docker Compose: Navigate to the admin directory (`cd ../admin`) and start the backend profile (`docker compose --profile backend up -d`). Alternatively, you can add a custom database and mail server in the `.env` file.
4. Start the application: Use `npm run dev` for development or `npm run build && npm run preview` for a production-like environment.
5. Open the application in your browser at `http://localhost:5173` for development or `http://localhost:4173/` for a production-like environment.

## Detailed Guide

For more information, refer to the detailed guide in the [Frontend Documentation](../docs/FRONTEND.md).
