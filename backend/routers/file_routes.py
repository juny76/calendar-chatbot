from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

from backend.dependencies import get_db

router = APIRouter()

db = get_db()
fs = GridFS(db)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_id = fs.put(file.file, filename=file.filename, content_type=file.content_type)
    # Trả về thông tin về file đã tải lên
    return JSONResponse(content={"filename": file.filename, "file_id": str(file_id)})
