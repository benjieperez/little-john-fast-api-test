from fastapi import APIRouter, FastAPI

class Router:
    def __init__(self, custom_app: FastAPI):
        self.custom_app = custom_app
        self.router = None

    def prefix(self, prefix: str):
        self.router = APIRouter(prefix=f"/{prefix}")
        return self
    
    def get(self, path: str, handler):
        self.router.get(f"/{path}")(handler)
        return self

    def post(self, path: str, handler):
        self.router.post(f"/{path}")(handler)
        return self
    
    def put(self, path: str, handler):
        self.router.put(f"/{path}")(handler)
        return self
    
    def delete(self, path: str, handler):
        self.router.delete(f"/{path}")(handler)
        return self
    
    def route(self, path: str, handler):
        self.router.route(f"/{path}")(handler)
        return self
    
    def include_router(self):
        self.custom_app.include_router(self.router)