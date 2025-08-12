from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

# Configuração da app Flask
app = Flask(__name__)

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")

    if not user_input:
        return jsonify({"error": "Pergunta inválida"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "És a Guardiã EuSou, IA estratégica do projeto EuSou, falas sempre em português e ajudas o Guardião a expandir riqueza e impacto global."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=800,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"answer": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
