from flask import Flask, render_template, request
import fitz  # PyMuPDF
from googletrans import Translator, LANGUAGES
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/translate", methods=["GET", "POST"])
def translate():
    languages = LANGUAGES  # Get all supported languages
    if request.method == "POST":
        pdf_file = request.files["pdf_file"]
        language = request.form["language"]
        # Save uploaded file
        file_path = f"./uploads/{pdf_file.filename}"
        pdf_file.save(file_path)
        # Extract text from PDF using PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        # Translate text using Google Translate
        translator = Translator()
        translated_text = translator.translate(text, dest=language).text
        return render_template("index.html", translated_text=translated_text, languages=languages)
    return render_template("index.html", languages=languages)

if __name__ == "__main__":
    app.run(debug=True)