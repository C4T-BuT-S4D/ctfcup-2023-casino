import os
import stat
import subprocess
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 << 14

for formatter in os.listdir("formatters"):
    path = f"formatters/{formatter}"
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


@app.post("/format")
def format():
    formatter = request.form["formatter"]
    file = request.files["file"]

    try:
        output = subprocess.check_output(
            os.path.abspath(Path("formatters") / formatter),
            stdin=file.stream,
        )
    except:
        return jsonify({"error": "Formatting failed... Sorry!"}), 500

    saved_path = Path("uploads")
    saved_path /= f"{uuid.uuid4()}-{formatter}"
    saved_path /= secure_filename(file.filename)
    saved_path = str(saved_path)[:100]
    os.makedirs(os.path.dirname(saved_path), exist_ok=True)

    with open(saved_path, "xb") as f:
        f.write(output)

    return jsonify({"path": saved_path})


@app.get("/uploads/<path:path>")
def uploads(path):
    return send_from_directory("uploads", path)


@app.get("/")
def index():
    return send_file("index.html")
