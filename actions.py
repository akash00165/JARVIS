"""
J.A.R.V.I.S System Actions
Handles file/app/URL opening and system commands
"""

import os
import sys
import subprocess
import platform
import re
import glob
from pathlib import Path


class SystemActions:

    @staticmethod
    def parse_actions(response_text: str):
        """Extract action tags from JARVIS response."""
        actions = []
        pattern = r'\[ACTION:(\w+):(.+?)\]'
        matches = re.findall(pattern, response_text)
        for action_type, action_value in matches:
            actions.append((action_type, action_value.strip()))
        # Clean response text
        clean = re.sub(r'\[ACTION:\w+:.+?\]', '', response_text).strip()
        return clean, actions

    @staticmethod
    def execute_action(action_type: str, action_value: str) -> str:
        """Execute a system action and return result message."""
        try:
            if action_type == "open_file":
                return SystemActions.open_file(action_value)
            elif action_type == "open_url":
                return SystemActions.open_url(action_value)
            elif action_type == "open_app":
                return SystemActions.open_app(action_value)
            elif action_type == "run_command":
                return SystemActions.run_command(action_value)
            elif action_type == "list_dir":
                return SystemActions.list_directory(action_value)
            else:
                return f"Unknown action: {action_type}"
        except Exception as e:
            return f"Action failed: {str(e)}"

    @staticmethod
    def open_file(path: str) -> str:
        """Open a file with the default application."""
        # Expand ~ and environment variables
        path = os.path.expandvars(os.path.expanduser(path))

        # Try to find the file if exact path doesn't exist
        if not os.path.exists(path):
            # Try searching common locations
            found = SystemActions.find_file(path)
            if found:
                path = found
            else:
                return f"File not found: {path}"

        system = platform.system()
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])

        return f"Opening: {path}"

    @staticmethod
    def open_url(url: str) -> str:
        """Open a URL in the default browser."""
        import webbrowser
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening browser: {url}"

    @staticmethod
    def open_app(app_name: str) -> str:
        """Launch an application by name."""
        system = platform.system()
        app_lower = app_name.lower()

        try:
            if system == "Windows":
                # Common Windows app shortcuts
                win_apps = {
                    "chrome": "chrome",
                    "firefox": "firefox",
                    "notepad": "notepad",
                    "calculator": "calc",
                    "explorer": "explorer",
                    "task manager": "taskmgr",
                    "cmd": "cmd",
                    "powershell": "powershell",
                    "word": "winword",
                    "excel": "excel",
                    "paint": "mspaint",
                    "spotify": "spotify",
                    "vscode": "code",
                    "vs code": "code",
                }
                cmd = win_apps.get(app_lower, app_name)
                subprocess.Popen(cmd, shell=True)

            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])

            else:  # Linux
                linux_apps = {
                    "chrome": "google-chrome",
                    "google chrome": "google-chrome",
                    "firefox": "firefox",
                    "files": "nautilus",
                    "terminal": "gnome-terminal",
                    "calculator": "gnome-calculator",
                    "text editor": "gedit",
                    "vscode": "code",
                    "vs code": "code",
                    "spotify": "spotify",
                }
                cmd = linux_apps.get(app_lower, app_lower.replace(" ", "-"))
                subprocess.Popen([cmd])

            return f"Launching {app_name}..."

        except FileNotFoundError:
            return f"Could not find application: {app_name}"

    @staticmethod
    def run_command(command: str) -> str:
        """Run a shell command and return output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout or result.stderr or "Command executed."
            return output[:500]  # Limit output length
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except Exception as e:
            return f"Command error: {str(e)}"

    @staticmethod
    def list_directory(path: str) -> str:
        """List contents of a directory."""
        path = os.path.expandvars(os.path.expanduser(path))
        if not os.path.exists(path):
            return f"Directory not found: {path}"
        try:
            items = os.listdir(path)
            dirs = [f"📁 {i}" for i in items if os.path.isdir(os.path.join(path, i))]
            files = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(path, i))]
            result = f"Contents of {path}:\n"
            result += "\n".join(sorted(dirs) + sorted(files))
            return result
        except PermissionError:
            return f"Permission denied: {path}"

    @staticmethod
    def find_file(filename: str) -> str:
        """Search for a file in common locations."""
        home = Path.home()
        search_dirs = [
            home,
            home / "Desktop",
            home / "Documents",
            home / "Downloads",
            home / "Pictures",
            home / "Videos",
            home / "Music",
        ]
        name = os.path.basename(filename)
        for directory in search_dirs:
            if directory.exists():
                matches = list(directory.glob(f"**/{name}"))
                if matches:
                    return str(matches[0])
        return None

    @staticmethod
    def get_system_info() -> dict:
        """Get current system information."""
        return {
            "os": f"{platform.system()} {platform.release()}",
            "python": platform.python_version(),
            "home": str(Path.home()),
            "cwd": os.getcwd(),
            "desktop": str(Path.home() / "Desktop"),
            "documents": str(Path.home() / "Documents"),
            "downloads": str(Path.home() / "Downloads"),
        }
