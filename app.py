import os
from flask import Flask, request, render_template, redirect, url_for
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

# Load AWS credentials from .env and clean them
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "").strip().strip("'").strip('"')
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "").strip().strip("'").strip('"')
region = os.getenv("AWS_REGION", "").strip().strip("'").strip('"')
bucket_name = os.getenv("S3_BUCKET", "").strip().strip("'").strip('"')
cloudfront_domain = os.getenv("CLOUDFRONT_DOMAIN", "").strip().strip("'").strip('"')

# Debug: Print loaded credentials (masked for security)
print("--- Debug: AWS Credentials ---")
print(f"Access Key ID: {aws_access_key_id[:5]}...{aws_access_key_id[-5:] if aws_access_key_id else 'None'}")
print(f"Secret Access Key: {'Set' if aws_secret_access_key else 'Not Set'}")
print(f"Region: {region}")
print(f"Bucket: {bucket_name}")
print("------------------------------")

from botocore.config import Config

try:
    # Explicitly set endpoint_url for the region to avoid any ambiguity
    endpoint_url = f"https://s3.{region}.amazonaws.com"
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
        endpoint_url=endpoint_url,
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'}
        )
    )
except Exception as e:
    print(f"Error initializing S3 client: {e}")
    s3 = None

def get_file_url(filename):
    """Generate file URL (CloudFront if available, otherwise S3 presigned URL)"""
    if cloudfront_domain:
        return f"https://{cloudfront_domain}/{filename}"
    else:
        # Generate presigned URL for private buckets (valid for 1 hour)
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': filename},
            ExpiresIn=3600
        )
        print(f"--- Debug: Generated URL for {filename} ---")
        print(url)
        print("------------------------------------------")
        return url

def format_file_size(size_bytes):
    """Format file size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    try:
        s3.upload_fileobj(file, bucket_name, file.filename)
        file_url = get_file_url(file.filename)
        return render_template('success.html', filename=file.filename, file_url=file_url)
    except ClientError as e:
        print(f"Upload error: {e}")
        return f"❌ Upload failed: {e}", 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"❌ An unexpected error occurred: {e}", 500

@app.route('/files')
def list_files():
    """List all files in the S3 bucket"""
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = []
        
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'name': obj['Key'],
                    'size': format_file_size(obj['Size']),
                    'last_modified': obj['LastModified'].strftime('%Y-%m-%d %H:%M'),
                    'download_url': get_file_url(obj['Key'])
                })
        
        return render_template('files.html', files=files)
    except ClientError as e:
        return render_template('files.html', files=[], error=str(e))

@app.route('/delete/<filename>')
def delete_file(filename):
    """Delete a file from S3"""
    try:
        s3.delete_object(Bucket=bucket_name, Key=filename)
    except ClientError:
        pass
    return redirect(url_for('list_files'))

if __name__ == '__main__':
    app.run(debug=True)
