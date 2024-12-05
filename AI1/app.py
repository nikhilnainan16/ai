from flask import Flask, request, jsonify, render_template
import openai
app = Flask(__name__)
openai.api_key = ""


def get_openai_answer(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": question}]
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except openai.error.AuthenticationError:
        return "Authentication failed. Invalid API key."
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            answer = get_openai_answer(question)
    return render_template('index.html', answer=answer)
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if user_input:
        bot_response = get_openai_answer(user_input)
        return jsonify({'bot': bot_response})
    else:
        return jsonify({'bot': "Please provide a valid input."})

if __name__ == '__main__':
    app.run(debug=True)
