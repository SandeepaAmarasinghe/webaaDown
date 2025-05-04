from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os
import subprocess
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        flash("No URL provided!", "danger")
        return redirect(url_for('index'))

    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.%(ext)s")

    cmd = [
        "yt-dlp",
        "--cookies", "cookies.txt",
        "-o", output_path,
        url
    ]

    try:
        subprocess.run(cmd, check=True)
        # Find downloaded file
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(video_id):
                return send_file(os.path.join(DOWNLOAD_FOLDER, file), as_attachment=True)
        flash("Download failed!", "danger")
    except subprocess.CalledProcessError as e:
        flash(f"Error: {e}", "danger")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
