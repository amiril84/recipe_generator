from flask import Flask, render_template, request, Response
import openai
import os
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    data = request.get_json()
    ingredients = data['ingredients']

    def generate_stream():
        prompt = f"""Generate recipe based on the provided ingredients: {ingredients}
        include the title of the recipe, the number of servings, number of calories per serving, preparation time, cooking time, measurements, ingredients and detail instructions.
        format the output with bullet points, headings, and subheadings."""
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    return generate_stream(), {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)
