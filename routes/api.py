from fastapi import FastAPI
from routes.handlers import *
from routes.router import Router
#Fast API Libs

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

class API:

    def __init__(self):
        self.db = Database()

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            
            # Code to execute during app startup
            await self.db.init_db()

            yield  # Allows the app to run
            
            # Code to execute during app shutdown
            await self.db.shutdown_db()

        self.app = FastAPI(lifespan=lifespan)
        self.setup_cors()  # Add CORS configuration
        self.auth_handler = AuthenticationHandler()
        self.user_file_handler = UserFileHandler()
        self.api_handler = APIHandler()
        self.setup_routes()

    def setup_cors(self):
        # Define allowed origins, methods, and headers
        origins = [
            "http://localhost:3000",  # Replace with your frontend URL
            "https://example.com",    # Add other allowed origins if needed
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,  # List of allowed origins
            allow_credentials=True,
            allow_methods=["*"],    # Allow all HTTP methods
            allow_headers=["*"],    # Allow all headers
        )

    def setup_routes(self):
         
        Router(self.app).prefix("api")\
            .get("health-check", self.api_handler.health_check)\
            .include_router()

        # Setup custom router with prefix and routes
        Router(self.app).prefix("auth")\
            .get("register", self.auth_handler.register)\
            .get("callback", self.auth_handler.callback)\
            .include_router()

        Router(self.app).prefix("user")\
            .post("upload_file", self.user_file_handler.upload_file)\
            .get("stream_file", self.user_file_handler.stream_file)\
            .include_router()
        
        
