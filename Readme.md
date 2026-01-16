# 🚀 KnoxDrive – Enhanced S3 Storage with CloudFront & CI/CD

KnoxDrive is a modern web app built with Python Flask that lets you upload and manage files in AWS S3 securely, delivered via CloudFront CDN.

This enhanced version features **Infrastructure as Code (IaC)** and an automated **CI/CD pipeline**.

## 🌟 Features

- **Modern UI**: Glassmorphism design with drag-and-drop uploads.
- **File Management**: List, download (via presigned URLs), and delete files.
- **CloudFront CDN**: Fast global delivery of your files.
- **Automated Infrastructure**: One-click deployment using AWS CloudFormation.
- **CI/CD**: Automated infrastructure updates via GitHub Actions.

## 🌩️ 1. AWS Setup (Automated)

Instead of manual setup, we use CloudFormation:

1. **Create IAM User**:
   - Go to IAM → Users → Create user (e.g., `knoxdrive-admin`).
   - Attach policy: `AdministratorAccess` (for initial setup) or specific permissions for S3, CloudFront, and CloudFormation.
   - Create Access Key for **"Third-party service"** (GitHub Actions).

2. **Configure GitHub Secrets**:
   In your GitHub Repo → Settings → Secrets and variables → Actions, add:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` (e.g., `ap-south-1`)

3. **Deploy**:
   Pushing to the `main` branch will automatically trigger the GitHub Action to deploy the `cloudformation.yaml` stack.

## 📦 2. Local Development

### Installation
```bash
git clone https://github.com/your-username/knoxdrive.git
cd knoxdrive
pip install -r requirements.txt
```

### Environment Variables (`.env`)
Create a `.env` file:
```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
S3_BUCKET=knoxdrive-storage-youraccountid
CLOUDFRONT_DOMAIN=your-distribution-id.cloudfront.net (Optional)
```

### Run
```bash
python app.py
```

## 📁 Project Structure
```
knoxdrive/
├── .github/workflows/
│   └── deploy.yml          # CI/CD Pipeline
├── templates/
│   ├── index.html          # Upload UI
│   ├── files.html          # File List UI
│   └── success.html        # Success UI
├── app.py                  # Flask Backend
├── cloudformation.yaml     # Infrastructure as Code
├── requirements.txt        # Dependencies
└── README.md
```

## 🔒 Security
- **OAC (Origin Access Control)**: S3 bucket is private; only CloudFront can access it.
- **Presigned URLs**: Secure, time-limited download links.
- **Least Privilege**: IAM roles are scoped to specific resources.

## 👨‍💻 Author
**Knox (Rupesh)**
