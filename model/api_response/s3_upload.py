from pydantic import BaseModel


class S3UploadResponse(BaseModel):
    filename: str
    bucket: str
    s3_path: str
