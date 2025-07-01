"""
Development server with hot reload capabilities.
"""

import os
import time
import threading
import subprocess
from pathlib import Path
from typing import Optional, List, Callable, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import http.server
import socketserver
from urllib.parse import urlparse


class DevServer:
    """Development server with hot reload functionality."""

    def __init__(
        self,
        port: int = 8000,
        host: str = "localhost",
        hot_reload: bool = True,
        watch_dirs: Optional[List[str]] = None,
        ignore_patterns: Optional[List[str]] = None,
        command: Optional[str] = None,
        static_dir: Optional[str] = None,
    ):
        """
        Initialize development server.

        Args:
            port: Server port
            host: Server host
            hot_reload: Enable hot reload
            watch_dirs: Directories to watch for changes
            ignore_patterns: Patterns to ignore
            command: Command to run (if not serving static files)
            static_dir: Directory to serve static files from
        """
        self.port = port
        self.host = host
        self.hot_reload = hot_reload
        self.watch_dirs = watch_dirs or ["."]
        self.ignore_patterns = ignore_patterns or [
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            ".pytest_cache",
        ]
        self.command = command
        self.static_dir = static_dir

        self.server = None
        self.process = None
        self.observer = None
        self.reload_callbacks = []
        self.is_running = False

    def add_reload_callback(self, callback: Callable) -> None:
        """Add a callback to be called on file changes."""
        self.reload_callbacks.append(callback)

    def start(self) -> None:
        """Start the development server."""
        print(f"🚀 Starting development server on {self.host}:{self.port}")

        if self.command:
            self._start_command_server()
        elif self.static_dir:
            self._start_static_server()
        else:
            self._start_simple_server()

        if self.hot_reload:
            self._start_file_watcher()

        self.is_running = True
        print(f"✅ Server running at http://{self.host}:{self.port}")

        try:
            # Keep the main thread alive
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Stop the development server."""
        print("\n🛑 Stopping development server...")

        self.is_running = False

        if self.observer:
            self.observer.stop()
            self.observer.join()

        if self.process:
            self.process.terminate()
            self.process.wait()

        if self.server:
            self.server.shutdown()

        print("✅ Server stopped")

    def _start_command_server(self) -> None:
        """Start server using a custom command."""

        def run_command():
            try:
                self.process = subprocess.Popen(
                    self.command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                # Read output in real-time
                for line in iter(self.process.stdout.readline, ""):
                    if line:
                        print(f"[SERVER] {line.strip()}")

            except Exception as e:
                print(f"❌ Error running command: {e}")

        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()

    def _start_static_server(self) -> None:
        """Start a static file server."""
        os.chdir(self.static_dir)

        handler = http.server.SimpleHTTPRequestHandler

        def run_server():
            with socketserver.TCPServer((self.host, self.port), handler) as httpd:
                self.server = httpd
                httpd.serve_forever()

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    def _start_simple_server(self) -> None:
        """Start a simple HTTP server."""

        class DevServerHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=".", **kwargs)

            def do_GET(self):
                if self.path == "/":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                    html = (
                        """
<!DOCTYPE html>
<html>
<head>
    <title>DevTools Helper - Development Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .feature { background: #f0f8ff; padding: 15px; margin: 10px 0; border-left: 4px solid #007acc; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        .footer { margin-top: 40px; text-align: center; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 DevTools Helper Development Server</h1>
        
        <div class="status">
            <strong>✅ Server Status:</strong> Running successfully<br>
            <strong>🌐 Address:</strong> http://localhost:"""
                        + str(self.server.server_port)
                        + """<br>
            <strong>🔄 Hot Reload:</strong> """
                        + ("Enabled" if self.hot_reload else "Disabled")
                        + """
        </div>
        
        <h2>🛠️ Available Features</h2>
        
        <div class="feature">
            <h3>📁 Project Generator</h3>
            <p>Create new projects with predefined templates:</p>
            <code>devtools create-project my-project --template webapp</code>
        </div>
        
        <div class="feature">
            <h3>🔍 Code Quality Checker</h3>
            <p>Analyze your code quality and get detailed reports:</p>
            <code>devtools check-quality ./src</code>
        </div>
        
        <div class="feature">
            <h3>⚙️ Configuration Manager</h3>
            <p>Manage application configuration easily:</p>
            <code>devtools init-config --type web</code>
        </div>
        
        <div class="feature">
            <h3>🔥 Hot Reload</h3>
            <p>This server automatically reloads when you change files in your project.</p>
        </div>
        
        <h2>📚 Quick Start</h2>
        <p>To get started with DevTools Helper:</p>
        <ol>
            <li>Install: <code>pip install devtools-helper</code></li>
            <li>Create project: <code>devtools create-project my-app</code></li>
            <li>Check quality: <code>devtools check-quality ./my-app</code></li>
            <li>Start server: <code>devtools serve --hot-reload</code></li>
        </ol>
        
        <div class="footer">
            <p>Powered by DevTools Helper | Press Ctrl+C to stop the server</p>
        </div>
    </div>
    
    """
                        + (
                            """
    <script>
        // Hot reload functionality
        if (window.location.hostname === 'localhost') {
            const eventSource = new EventSource('/events');
            eventSource.onmessage = function(event) {
                if (event.data === 'reload') {
                    window.location.reload();
                }
            };
        }
    </script>
    """
                            if self.hot_reload
                            else ""
                        )
                        + """
</body>
</html>
                    """
                    )

                    self.wfile.write(html.encode())
                else:
                    super().do_GET()

        def run_server():
            with socketserver.TCPServer(
                (self.host, self.port), DevServerHandler
            ) as httpd:
                self.server = httpd
                httpd.serve_forever()

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    def _start_file_watcher(self) -> None:
        """Start watching files for changes."""
        if not self.hot_reload:
            return

        class ReloadHandler(FileSystemEventHandler):
            def __init__(self, dev_server):
                self.dev_server = dev_server
                self.last_reload = 0
                self.reload_delay = 1  # seconds

            def on_modified(self, event):
                if event.is_directory:
                    return

                # Check if file should be ignored
                file_path = Path(event.src_path)
                if self._should_ignore(file_path):
                    return

                # Rate limit reloads
                current_time = time.time()
                if current_time - self.last_reload < self.reload_delay:
                    return

                self.last_reload = current_time
                print(f"🔄 File changed: {file_path}")

                # Call reload callbacks
                for callback in self.dev_server.reload_callbacks:
                    try:
                        callback(file_path)
                    except Exception as e:
                        print(f"❌ Reload callback error: {e}")

                # Restart command if running
                if self.dev_server.command and self.dev_server.process:
                    print("🔄 Restarting server...")
                    self.dev_server.process.terminate()
                    self.dev_server.process.wait()

                    # Start new process
                    try:
                        self.dev_server.process = subprocess.Popen(
                            self.dev_server.command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )
                        print("✅ Server restarted")
                    except Exception as e:
                        print(f"❌ Error restarting server: {e}")

            def _should_ignore(self, file_path: Path) -> bool:
                """Check if file should be ignored."""
                path_str = str(file_path)

                for pattern in self.dev_server.ignore_patterns:
                    if pattern in path_str:
                        return True

                # Ignore certain file types
                ignored_extensions = [".pyc", ".pyo", ".swp", ".tmp", ".log"]
                if file_path.suffix in ignored_extensions:
                    return True

                return False

        self.observer = Observer()

        for watch_dir in self.watch_dirs:
            if os.path.exists(watch_dir):
                self.observer.schedule(ReloadHandler(self), watch_dir, recursive=True)
                print(f"👀 Watching {watch_dir} for changes...")

        self.observer.start()


class LiveReloadServer:
    """Specialized server for live reload functionality."""

    def __init__(self, port: int = 35729):
        self.port = port
        self.clients = set()
        self.server = None

    def start(self):
        """Start the live reload server."""
        # This would implement WebSocket server for live reload
        # For now, we'll use file watching approach
        pass

    def reload(self):
        """Trigger reload for all connected clients."""
        # Send reload signal to all connected clients
        pass


class ProjectRunner:
    """Helper class to run different types of projects."""

    @staticmethod
    def detect_project_type(path: str = ".") -> str:
        """Detect the type of project in the given path."""
        path_obj = Path(path)

        # Check for specific files that indicate project type
        if (path_obj / "manage.py").exists():
            return "django"
        elif (path_obj / "app.py").exists() or (path_obj / "main.py").exists():
            return "flask"
        elif (path_obj / "pyproject.toml").exists() or (path_obj / "setup.py").exists():
            return "package"
        elif (path_obj / "requirements.txt").exists():
            return "python"
        elif (path_obj / "package.json").exists():
            return "node"
        else:
            return "static"

    @staticmethod
    def get_run_command(project_type: str, path: str = ".") -> Optional[str]:
        """Get the appropriate run command for a project type."""
        commands = {
            "django": "python manage.py runserver",
            "flask": "python app.py",
            "fastapi": "uvicorn main:app --reload",
            "package": "python -m pip install -e .",
            "python": "python main.py",
            "node": "npm start",
            "static": None,  # Will use built-in static server
        }

        return commands.get(project_type)

    @staticmethod
    def get_watch_dirs(project_type: str, path: str = ".") -> List[str]:
        """Get directories to watch for different project types."""
        base_dirs = [path]

        project_dirs = {
            "django": [".", "templates", "static"],
            "flask": [".", "templates", "static"],
            "fastapi": [".", "templates", "static"],
            "package": [".", "src"],
            "python": ["."],
            "node": [".", "src", "public"],
            "static": ["."],
        }

        return project_dirs.get(project_type, ["."])
