import sys
from src.application.launcher_application import LauncherApplication


def main() -> int:
    app = LauncherApplication(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
