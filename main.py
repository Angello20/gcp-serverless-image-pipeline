import os
import io
import json
import base64
import functions_framework
from google.cloud import storage
from PIL import Image

storage_client = storage.Client()

DESTINATION_BUCKET_NAME = os.environ.get(
    'DESTINATION_BUCKET', 
    'destination-bucket-project-1ae03431-c8a2-44f6-996'
)

@functions_framework.cloud_event
def process_image(cloud_event):
    try:
        pubsub_data = base64.b64decode(cloud_event.data["message"]["data"]).decode()
        event_payload = json.loads(pubsub_data)
        
        src_bucket_name = event_payload['bucket']
        file_name = event_payload['name']
        
        print(f"Starting processing for file: {file_name} in bucket: {src_bucket_name}")



        # Avoid processing loop if file is already processed
        if src_bucket_name == DESTINATION_BUCKET_NAME and file_name.startswith('processed-'):
            print("File is already processed. Skipping...")
            return



        # Download image from Cloud Storage
        src_bucket = storage_client.bucket(src_bucket_name)
        blob = src_bucket.blob(file_name)
        image_bytes = blob.download_as_bytes()

        img = Image.open(io.BytesIO(image_bytes))



        # Image Processing Tasks
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail((800, 800))

        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG", quality=75, optimize=True)
        output_buffer.seek(0)



        # Upload processed image to Destination Bucket
        dest_bucket = storage_client.bucket(DESTINATION_BUCKET_NAME)
        dest_file_name = f"processed-{file_name}"
        dest_blob = dest_bucket.blob(dest_file_name)
        
        dest_blob.upload_from_file(
            output_buffer, 
            content_type=blob.content_type if blob.content_type else 'image/jpeg'
        )

        print(f"Success: Image processed and saved as '{dest_file_name}' in '{DESTINATION_BUCKET_NAME}'.")

    except Exception as e:
        print(f"Error processing image {file_name}: {str(e)}")
        raise e