import tomllib, os
from config.database import Database

class APIHandler:
    def __init__(self):
        pass

    @staticmethod
    def read_pyproject():
        # Get the current directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Navigate to the pyproject.toml file (one level up from `app`)
        pyproject_path = os.path.join(current_dir, "../../pyproject.toml")

        # Normalize the path for the operating system
        pyproject_path = os.path.normpath(pyproject_path)

        # Check if the file exists
        if not os.path.exists(pyproject_path):
            raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}")

        # Reading and parsing the file
        with open(pyproject_path, "rb") as file:
            pyproject_data = tomllib.load(file)

        return pyproject_data
    
    async def health_check(self):
        pyproject = self.read_pyproject()

        # Ensure to await the asynchronous DB status check
        postgresql_status = await Database().check_postgresql_status()

        return {
            "APP_NAME": pyproject["project"]["name"],
            "VERSION": pyproject["project"]["version"],
            "DESCRIPTION": pyproject["project"]["description"],
            "DEVS": pyproject["project"]["authors"],
            "DB_STATUS": "OK" if postgresql_status else "ERROR"
        }
