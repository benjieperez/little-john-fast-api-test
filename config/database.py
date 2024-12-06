import logging
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
from decouple import config as env

class Database:
    def __init__(self):
        self.db_user = env("DB_USER")
        self.db_password = env("DB_PASSWORD")
        self.db_name = env("DB_NAME")
        self.db_host = env('DB_HOST', default='localhost')  # with default fallback
        self.db_port = env("DB_PORT")

    def postgres_db_url(self, username, password, database_name):
        """Generate the PostgreSQL database URL with SSL."""
        if env("ENV") == "develop": 
            return f"postgres://{username}:{password}@{self.db_host}:{self.db_port}/{database_name}"
        else:
            # Staging or Prod
            return f"postgres://{username}:{password}@{self.db_host}:{self.db_port}/{database_name}?ssl=true"
        
    async def init_db(self):
        """Initialize the database connection and generate the schemas."""
        postgres_db_url = self.postgres_db_url(
            username=self.db_user,
            password=self.db_password,
            database_name=self.db_name,
        )

        DATABASE_CONFIG = {
            "connections": {
                "default": postgres_db_url
            },
            "apps": {
                "models": {
                    "models": ["app.Models"],
                    "default_connection": "default",
                }
            }
        }

        # Initialize the database connection with models (make sure to add your models)
        await Tortoise.init(config=DATABASE_CONFIG)
        await Tortoise.generate_schemas()

    async def shutdown_db(self):
        await Tortoise.close_connections()

    async def check_postgresql_status(self):
        """Check PostgreSQL database status."""
        try:
            # Initialize the database connection first
            await self.init_db()

            # Test the connection by executing a simple query
            await Tortoise.get_connection("default").execute_query("SELECT 1")

            logging.info("PostgreSQL is up and reachable!")
            status = True
        except DBConnectionError as e:
            logging.info(f"Failed to connect to PostgreSQL: {e}")
            status = False
        except Exception as e:
            logging.info(f"An unexpected error occurred: {e}")
            status = False
        finally:
            # Close the connection to avoid resource leaks
            await Tortoise.close_connections()

        return status
