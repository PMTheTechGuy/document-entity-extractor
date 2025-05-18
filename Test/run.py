import uvicorn
from pathlib import Path
import sys

# Set root and ensure it's in PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    print("🚀 Launching FastAPI App")

    port_input = input("Enter port to run on (default is 8000): ").strip()
    try:
        port = int(port_input) if port_input else 8000
    except ValueError:
        print("⚠️ Invalid port, defaulting to 8000")
        port = 8000

    reload_input = input("Enable auto-reload? (y/n): ").strip().lower()
    reload = reload_input == 'y'

    if reload:
        config = uvicorn.Config(
            "api.main:app",
            host="127.0.0.1",
            port=port,
            reload=True,
            reload_dirs=[str(PROJECT_ROOT)],
            env_file=".env"
        )
    else:
        from api.main import app
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=port,
            reload=False,
            env_file=".env"
        )

    server = uvicorn.Server(config)
    server.run()  # this supports graceful shutdowns

if __name__ == "__main__":
    main()

