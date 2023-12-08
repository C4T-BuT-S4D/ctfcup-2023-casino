import os
import re
import stat
import subprocess
import uuid

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
            [
                "timeout",
                "0.5",
                os.path.join("formatters", re.sub("[^a-z]", "", formatter)),
            ],
            stdin=file.stream,
        )
    except:
        return jsonify({"error": "Formatting failed... Sorry!"}), 500

    saved_path = f"uploads/{uuid.uuid4()}-{formatter}"
    os.makedirs(saved_path, exist_ok=True)
    saved_path = os.path.join(saved_path, secure_filename(file.filename))

    with open(saved_path, "xb") as f:
        f.write(output)

    return jsonify({"path": saved_path})


@app.get("/uploads/<path:path>")
def uploads(path):
    return send_from_directory("uploads", path)


@app.get("/")
def index():
    return send_file("index.html")
