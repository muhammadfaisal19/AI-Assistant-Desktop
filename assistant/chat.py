from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                response = completion.choices[0].message.content
            except openai.RateLimitError:
                response = "⚠️ Rate Limit Error: You’ve exceeded your quota. Please check your OpenAI usage and billing."
            except openai.OpenAIError as e:
                response = f"⚠️ OpenAI Error: {str(e)}"
            except Exception as e:
                response = f"⚠️ Unexpected Error: {str(e)}"
        else:
            response = "⚠️ Please enter a prompt."
    return render_template("index.html", response=response)


@app.route("/voice_query", methods=["POST"])
def voice_query():
    try:
        data = request.get_json()
        transcript = data.get("text", "").strip()
        if not transcript:
            return jsonify({"error": "Empty voice input."}), 400

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": transcript}]
        )
        return jsonify({"response": completion.choices[0].message.content})

    except openai.RateLimitError:
        return jsonify({
            "error": "⚠️ RateLimitError: You’ve exceeded your quota. Please check your OpenAI usage and billing."
        }), 429
    except openai.OpenAIError as e:
        return jsonify({"error": f"⚠️ OpenAI API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"⚠️ Unexpected Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
