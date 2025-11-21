from flask import Flask, request, render_template
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("S3_BUCKET_NAME")

print("Loaded BUCKET from .env:", BUCKET)

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# ------------------------------
# 1. Login (Enter Name)
# ------------------------------
@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form.get("username")
    return render_template("dashboard.html", username=username)

# ------------------------------
# 2. Upload File
# ------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    if file:
        s3.upload_fileobj(file, BUCKET, file.filename)
        file_url = f"https://{BUCKET}.s3.amazonaws.com/{file.filename}"
        return f"File uploaded successfully! <br><br> File URL: <a href='{file_url}'>{file_url}</a>"

    return "Upload failed"

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)