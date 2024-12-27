import logging
from rest_framework.exceptions import APIException
from django.http import JsonResponse
from .utils import get_minio_client
from django.conf import settings

logger = logging.getLogger(__name__)

class FileUploadException(APIException):
    status_code = 400
    default_detail = 'File upload failed.'
    default_code = 'file_upload_failed'

def upload_file(request):
    try:
        file = request.FILES.get('file')
        if not file:
            raise FileUploadException("No file provided")

        client = get_minio_client()
        bucket = settings.MINIO_BUCKET_NAME

        client.upload_fileobj(file, bucket, file.name)
        url = f"{settings.MINIO_ENDPOINT}/{bucket}/{file.name}"
        logger.info(f"File uploaded: {file.name}")
        return JsonResponse({'url': url})

    except FileUploadException as e:
        logger.error(f"Error uploading file: {e}")
        return JsonResponse({'error': str(e)}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'error': 'Unexpected error occurred'}, status=500)
