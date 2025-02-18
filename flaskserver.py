from flask import Flask, request, send_file, jsonify
import os
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return f"File saved at {file_path}", 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    return send_file(file_path, as_attachment=True)

@app.route("/delete/caption", methods=['DELETE'])
def delete_caption():
    if os.path.exists("D:\\apk1\\imgrecpy\\uploads\\caption.txt"):
        os.remove("D:\\apk1\\imgrecpy\\uploads\\caption.txt")
        return jsonify({"message": "Caption deleted"}), 200
    return jsonify({"error": "Caption not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)