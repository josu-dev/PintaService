# Backend


## Dev mode

### Dev server

To run the backend in Dev mode run:

```bash
python dev.py dev

# or

./dev.py dev
```

> The dev server generates the tailwindcss file on template changes and triggers the client reload to apply the changes.

### Build for production

After you are done with the templating changes, you can build the backend for production with:

```bash
python dev.py build

# or

./dev.py build
```

> The build only minimizes the tailwindcss file and does not minify any other files.
