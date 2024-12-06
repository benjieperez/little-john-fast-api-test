import os
import aiofiles
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

class UserFileHandler:
    def __init__(self):
        self.file_dir = os.path.join("resources", "uploads")

        # Ensure the directory exists
        os.makedirs(self.file_dir, exist_ok=True)

    async def upload_file(self, file: UploadFile = File(...)):
        try:
            file_path = os.path.join(self.file_dir, file.filename)  # Full path including the file name
            # Save the file to disk
            async with aiofiles.open(file_path, 'wb') as buffer:
                content = await file.read()
                await buffer.write(content)

            return JSONResponse(
                content={"filename": file.filename, "message": "File uploaded successfully"},
                status_code=200
            )
        except BaseException as e:
            return JSONResponse(
                content={"filename": file.filename, "message": "File Error"},
                status_code=500
            )
    
    async def stream_file(self, file_name: str):

        file_path = os.path.join(self.file_dir, file_name)  # Construct the file path

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Open the file and return as streaming response
        async def file_stream():
            async with aiofiles.open(file_path, mode='rb') as file:
                while chunk := await file.read(1024):
                    yield chunk
        
        return StreamingResponse(file_stream(), media_type="application/octet-stream")
