from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def home():
    return render_template(
        "index.html",
        review=None,
        code=""
    )

@app.route("/review", methods=["POST"])
def review():

    code = request.form.get("code")

    prompt = f"""
You are an expert senior software engineer.

Review this code and provide:

1. Bugs
2. Improvements
3. Security issues
4. Best practices
5. Optimized version if needed

Code:
{code}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI code reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        review = response.choices[0].message.content

    except Exception as e:

        review = f"Error: {str(e)}"

    return render_template(
        "index.html",
        review=review,
        code=code
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
