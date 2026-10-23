
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>India Quiz App</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #141e30, #243b55);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 25px;
            color: #222;
        }

        .quiz-container {
            width: 100%;
            max-width: 600px;
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header .icon {
            font-size: 45px;
        }

        h1 {
            color: #243b55;
            margin: 12px 0;
        }

        .subtitle {
            color: #777;
            font-size: 14px;
        }

        .question {
            background: #f7f9fc;
            padding: 22px;
            margin-bottom: 20px;
            border-radius: 12px;
            border: 1px solid #e5eaf1;
        }

        .question h3 {
            margin-bottom: 16px;
            color: #243b55;
            font-size: 17px;
        }

        .option {
            display: flex;
            align-items: center;
            gap: 10px;
            background: white;
            padding: 12px;
            border: 1px solid #e0e5ec;
            border-radius: 8px;
            margin-top: 10px;
            cursor: pointer;
            transition: 0.2s;
        }

        .option:hover {
            border-color: #4776e6;
            background: #f0f4ff;
        }

        .option input {
            accent-color: #4776e6;
            cursor: pointer;
        }

        .submit-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #4776e6, #8e54e9);
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 18px #4776e655;
        }

        .result {
            text-align: center;
            padding: 20px;
            margin-bottom: 22px;
            background: #eaf8ef;
            border: 1px solid #b9e8c7;
            border-radius: 12px;
        }

        .result h2 {
            color: #168344;
            margin-bottom: 8px;
        }

        .result p {
            margin-top: 8px;
        }

        .feedback {
            margin-top: 12px;
            font-size: 14px;
            line-height: 1.7;
            text-align: left;
        }

        .footer {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 22px;
        }

        @media (max-width: 480px) {
            .quiz-container {
                padding: 22px;
            }

            h1 {
                font-size: 25px;
            }
        }
    </style>
</head>

<body>
    <div class="quiz-container">

        <div class="header">
            <div class="icon">🧠</div>
            <h1>India Quiz Challenge</h1>
            <p class="subtitle">Test your knowledge of Indian capitals</p>
        </div>

        {% if score is not none %}
        <div class="result">
            <h2>🎉 Your Result</h2>
            <h1>{{ score }} / 2</h1>
            <p>You scored {{ score * 50 }}%</p>

            <div class="feedback">
                {% for message in feedback %}
                    <p>{{ message }}</p>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <form method="POST">

            <div class="question">
                <h3>1. What is the capital of India?</h3>

                {% for option in ["Delhi", "Mumbai", "Chennai", "Kolkata"] %}
                <label class="option">
                    <input type="radio" name="q1"
                           value="{{ option }}"
                           {% if answers and answers.q1 == option %}checked{% endif %}
                           required>
                    {{ option }}
                </label>
                {% endfor %}
            </div>

            <div class="question">
                <h3>2. What is the capital of Telangana?</h3>

                {% for option in ["Vellore", "Hyderabad", "Warangal", "Nizamabad"] %}
                <label class="option">
                    <input type="radio" name="q2"
                           value="{{ option }}"
                           {% if answers and answers.q2 == option %}checked{% endif %}
                           required>
                    {{ option }}
                </label>
                {% endfor %}
            </div>

            <button type="submit" class="submit-btn">
                Submit Answers →
            </button>

        </form>

        <div class="footer">
            Made with Python & Flask | Quiz App
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def quiz():
    score = None
    feedback = []
    answers = None

    if request.method == "POST":
        q1 = request.form.get("q1", "")
        q2 = request.form.get("q2", "")

        answers = {"q1": q1, "q2": q2}

        correct_answers = {
            "q1": "Delhi",
            "q2": "Hyderabad"
        }

        score = 0

        if q1 == correct_answers["q1"]:
            score += 1
            feedback.append("✅ Q1: Correct! Delhi is the capital of India.")
        else:
            feedback.append("❌ Q1: Incorrect. The correct answer is Delhi.")

        if q2 == correct_answers["q2"]:
            score += 1
            feedback.append(
                "✅ Q2: Correct! Hyderabad is the capital of Telangana."
            )
        else:
            feedback.append(
                "❌ Q2: Incorrect. The correct answer is Hyderabad."
            )

    return render_template_string(
        HTML, score=score, feedback=feedback, answers=answers
    )

if __name__ == "__main__":
    app.run(debug=True)
