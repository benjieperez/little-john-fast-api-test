import json, logging, traceback
from fastapi import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from starlette.requests import Request as StarletteRequest
from app.Models.Users import *

class AuthenticationHandler:
    def __init__(self):
        # Set the path for redirect URL (where Google sends the user after authentication)
        self.redirect_uri = "http://localhost:8080/auth/callback"

        # Google OAuth 2.0 credentials file
        self.GOOGLE_CLIENT_CREDENTIALS_FILE = "credentials.json"
        with open("credentials.json") as google_creds:
            self.GOOGLE_CLIENT_CREDENTIALS_DATA = json.load(google_creds)

        self.SCOPES = [
            "openid",  # OpenID Connect scope for authentication
            "https://www.googleapis.com/auth/userinfo.profile",  # User's profile information
            "https://www.googleapis.com/auth/userinfo.email",  # User's email address
        ]

    async def login(self):
        flow = Flow.from_client_config(
            client_config=self.GOOGLE_CLIENT_CREDENTIALS_DATA,
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return RedirectResponse(authorization_url)

    async def callback(self, request: StarletteRequest):

        flow = InstalledAppFlow.from_client_config(
            self.GOOGLE_CLIENT_CREDENTIALS_DATA, self.SCOPES, redirect_uri=self.redirect_uri
        )
        # Get the authorization response and exchange it for credentials
        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)

        # Get credentials and store them for future use
        credentials = flow.credentials

        # Get user info
        from googleapiclient.discovery import build

        try:
            service = build("oauth2", "v2", credentials=credentials)
            user_info = service.userinfo().get().execute()
            
            # Create a Pydantic model with the response data
            google_user = GoogleOAuthResponse(
                name=user_info["name"],
                email=user_info["email"],
                picture_url=user_info["picture"],
                token=credentials.token,
            )

            # return {"user_info": user_info}

            # Validate the data using UserCreate Pydantic model
            user_data = UserCreate(**google_user.model_dump())

            # Save the user to the database (Tortoise ORM)
            existing_user = await UsersModel.filter(email=user_data.email).first()
            if existing_user:
                return JSONResponse(
                    content={"message": "User already existing.", "status": "error"},
                    status_code=409
                )
            else:
                # Create a new user
                await UsersModel.create(**user_data.model_dump())
            
            return JSONResponse(
                content={"message": "User registered successfully", "status": "ok"},
                status_code=201
            )
        except Exception as e:
            logging.error(f"Failed to fetch user info: {e}")
            return JSONResponse({"error": "Unable to fetch user information"}, status_code=500)