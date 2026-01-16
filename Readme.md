# 🚀 KnoxDrive – Secure S3 Storage

KnoxDrive is a modern web app built with Python Flask that lets you upload and manage files in AWS S3 securely.

## 🌟 Features
- **Modern UI**: Glassmorphism design with drag-and-drop.
- **File Management**: List, download, and delete files.
- **Secure**: Uses S3 Presigned URLs and IAM Roles.
- **CI/CD**: Automated deployment to EC2 on push to main.

## 🛠️ Manual AWS Setup

To deploy this app, you need to manually set up these resources in AWS:

### 1. S3 Bucket
- Create a private S3 bucket (e.g., `my-knoxdrive-storage`).
- Block all public access.

### 2. IAM Role for EC2
- Create an IAM Role for **EC2**.
- Attach the policy: `AmazonS3FullAccess`.
- Name it (e.g., `KnoxDrive-EC2-Role`).

### 3. EC2 Instance
- Launch an instance (Amazon Linux 2023, t2.micro).
- **IAM Instance Profile**: Select the role you created above.
- **Security Group**: Allow **HTTP (80)** and **SSH (22)**.
- **Key Pair**: Create/use a `.pem` key for SSH.

## 🚀 CI/CD Setup (GitHub)

1. **GitHub Secrets**: Add these to your repo (`Settings > Secrets > Actions`):
   - `EC2_SSH_KEY`: Content of your `.pem` file.
   - `EC2_PUBLIC_IP`: Public IP of your EC2.
   - `S3_BUCKET_NAME`: Name of your S3 bucket.
   - `AWS_REGION`: e.g., `ap-south-1`.

2. **Deploy**:
   - Push your code to the `main` branch.
   - GitHub Actions will automatically deploy the code to `/home/ec2-user/app` and start the service.

## 📦 Local Development
1. Clone the repo.
2. Create a `.env` file with your local AWS keys.
3. Run `pip install -r requirements.txt`.
4. Run `python app.py`.

## � Security
- **IAM Roles**: The EC2 instance uses a role to access S3, so no AWS keys are stored on the server.
- **Presigned URLs**: Files are kept private; download links expire after 1 hour.
