from os import getcwd, remove
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import JSONResponse, FileResponse
from random import randint
import uuid
from typing import List


IMAGEDIR = "fastapi-images/"

router = APIRouter(
    prefix="/img",
    tags=["File"],
    responses={404: {"message": "Not found"}}
)


@router.post("/")
async def up_img(file: UploadFile = File(...)):
    size = await file.read()
    return {"File Name": file.filename, "size": len(size)}


@router.post("/multi")
async def up_multi_file(files: List[UploadFile] = File(...)):
    file = [
        {
            "File Name": file.filename,
            "Size": len(await file.read())
        } for file in files]
    return file


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as image:
        content = await file.read()
        image.write(content)
        image.close()
    return JSONResponse(content={"filename": file.filename},
                        status_code=200)


@router.get("/file/{name_file}")
async def get_file(name_file: str):
    return FileResponse(path=getcwd() + "/" + name_file)


@router.delete("/delete/file/{name_file}")
async def delete_file(name_file: str):
    try:
        remove(getcwd() + "/" + name_file)
        return JSONResponse(content={
            "removed": True}, status_code=200)

    except FileNotFoundError:

        return JSONResponse(content={
            "removed": False, "error_message": "File not found"
        }, status_code=404)


@router.post("/images/")
async def create_upload_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


@router.get("/images/")
async def read_random_file():

    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"

    return FileResponse(path)
