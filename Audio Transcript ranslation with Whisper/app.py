import openai 
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
# Audio that user will upload
app.config["UPLOAD_FOLDER"] = "static"


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        language = request.form["language"]  # Get the language, user input from backend
        file = request.files["file"] # Audio , File type input(Html)
        if file:
            filename = file.filename # File name
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Save
            
            audio_file = open("static/Recording.mp3", "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file) # Getting the result

            # Convert to another language
            response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages = [{ "role": "system", "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}" }, 
                                { "role": "user", "content": transcript.text }],
                    temperature=0,
                    max_tokens=256
                  )
            
            # For Getting the whole response
            return jsonify(response) # For rendering in html format,in json format
        
            # For getting only the content part
            # return jsonify(response["choices"][0]['message']['content']) # 
    
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)