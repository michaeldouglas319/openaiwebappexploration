import openai
from flask import Flask, render_template, request, redirect, url_for, jsonify
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_key_points(text):
    doc = nlp(text)
    key_points = [chunk.text for chunk in doc.noun_chunks]
    return key_points

@app.route('/extract_key_points', methods=['POST'])
def extract_key_points_route():
    text = request.json['text']
    key_points = extract_key_points(text)
    return jsonify(key_points)



# Replace 'your_openai_api_key' with your actual API key
openai.api_key = "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"

class Message:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text

chat = []

@app.route('/', methods=['GET'])
def index():
    chat.reverse()
    return render_template('index.html', chat=reversed(chat[::-1]))
    


@app.route('/chat', methods=['POST'])
def chat_submit():
    user_input = request.form.get('user_input') or request.json and request.json.get('user_input')
    
    if user_input is None:
        return jsonify(error="User input not found"), 400

    chat.insert(0, Message('User', user_input))
    
    # Set the model and prompt
    model_engine = "text-davinci-003"
    prompt = user_input

    # Set the maximum number of tokens to generate in the response
    max_tokens = 1500

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_text = completion.choices[0].text.strip()
    chat.insert(0, Message('Chatbot', response_text))

    if request.json:
        return jsonify(response_text=response_text)
    else:
        return redirect(url_for('index'))



@app.route('/chat', methods=['GET'])
def chat_redirect():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

