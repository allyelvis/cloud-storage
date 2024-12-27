from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_minio_client
from django.conf import settings
from django.http import HttpResponse

@api_view(['POST'])
def upload_file(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file provided'}, status=400)
    
    client = get_minio_client()
    bucket = settings.MINIO_BUCKET_NAME
    
    client.upload_fileobj(file, bucket, file.name)
    url = f"{settings.MINIO_ENDPOINT}/{bucket}/{file.name}"
    return Response({'url': url})

@api_view(['GET'])
def download_file(request, file_name):
    client = get_minio_client()
    bucket = settings.MINIO_BUCKET_NAME
    
    file = client.get_object(Bucket=bucket, Key=file_name)
    return HttpResponse(file['Body'].read(), content_type='application/octet-stream')
