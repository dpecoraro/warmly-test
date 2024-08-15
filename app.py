import logging
import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Query

from services.dynamo_service_facade import get_data_by_phone, get_data_by_email
from services.s3_service_facade import upload_to_s3
from model.api_response.s3_upload import S3UploadResponse


app = FastAPI()


@app.post("/upload/", response_model=S3UploadResponse)
async def upload(file: UploadFile = File(...)):
    print('chegou aqui')
    file_size = await file.read()
    if len(file_size) > 1 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 1MB")

    await file.seek(0)

    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="File must be a JSON file")

    os.makedirs(".temp", exist_ok=True)
    file_location = f".temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file_size)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    bucket_name = "warmly-test"
    s3_object_name = f"{str(uuid.uuid4())}_{file.filename}_{timestamp}"
    upload_to_s3(file_location, bucket_name, s3_object_name)

    return S3UploadResponse(
        filename=file.filename,
        bucket=bucket_name,
        s3_path=s3_object_name
    )


@app.get("/search")
async def search_object(phone: Optional[str] = Query(None),
                        email: Optional[str] = Query(None)):
    if not phone and not email:
        raise HTTPException(status_code=400, detail="Phone or email must be provided")
    result = []
    if phone:
        return await get_data_by_phone(phone)
    if email:
        return await get_data_by_email(email)
    raise HTTPException(status_code=404, detail="No data found")