from src.web import create_app


def main() -> int:
    """Runs the application for development purposes."""
    app = create_app()
    app.run()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
