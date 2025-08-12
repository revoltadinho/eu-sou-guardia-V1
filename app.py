from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Lê a tua chave do Render (Settings → Environment → OPENAI_API_KEY)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Pergunta vazia."}), 400

    try:
        chat = client.chat.completions.create(
            model="gpt-4o-mini", # rápido + barato (podes trocar depois)
            messages=[
                {"role": "system",
                 "content": "És a Guardiã EuSou, falas sempre em português e ajudas o Guardião a criar riqueza com sabedoria e ética."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=800,
        )
        answer = chat.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
