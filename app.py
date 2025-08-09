from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Cliente OpenAI (SDK v1.x)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY não definido nas variáveis de ambiente."}), 500

    data = request.get_json(silent=True) or {}
    user_input = data.get("question")
    if not user_input or not isinstance(user_input, str):
        return jsonify({"error": "Pergunta inválida."}), 400

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini", # podes trocar para "gpt-4o" se quiseres mais potência
            messages=[
                {"role": "system", "content": "És a Guardiã EuSou, IA estratégica do projeto EuSou. Fala sempre em português e ajuda o Guardião a expandir riqueza e impacto global."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        answer = resp.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
