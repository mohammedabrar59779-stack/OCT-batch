
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background:
                radial-gradient(circle at top left, #4338ca, transparent 45%),
                linear-gradient(135deg, #080b20, #111b3b, #090d20);
        }

        .login-container {
            width: 100%;
            max-width: 410px;
            padding: 40px 35px;
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 22px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(18px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            color: white;
        }

        .logo {
            width: 65px;
            height: 65px;
            margin: 0 auto 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 20px;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            font-size: 30px;
            box-shadow: 0 8px 25px rgba(99,102,241,0.4);
        }

        h1 {
            text-align: center;
            font-size: 30px;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #b8c2df;
            font-size: 14px;
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-size: 14px;
            margin-bottom: 9px;
            color: #e0e7ff;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 14px 15px;
            border: 1px solid #354265;
            border-radius: 10px;
            outline: none;
            background: rgba(8,13,35,0.7);
            color: white;
            font-size: 14px;
            transition: 0.3s;
        }

        input:focus {
            border-color: #818cf8;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
        }

        input::placeholder {
            color: #7784a7;
        }

        .options {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            font-size: 12px;
            color: #cbd5e1;
        }

        .remember {
            display: flex;
            align-items: center;
            gap: 7px;
        }

        .options a,
        .signup a {
            color: #a5b4fc;
            text-decoration: none;
        }

        .options a:hover,
        .signup a:hover {
            text-decoration: underline;
        }

        button {
            width: 100%;
            padding: 14px;
            margin-top: 25px;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            background: linear-gradient(90deg, #6366f1, #9333ea);
            transition: 0.3s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99,102,241,0.35);
        }

        .message {
            margin-top: 18px;
            text-align: center;
            font-size: 14px;
            color: #c4b5fd;
        }

        .signup {
            text-align: center;
            margin-top: 28px;
            color: #b8c2df;
            font-size: 13px;
        }

        .footer {
            margin-top: 28px;
            text-align: center;
            color: #7582a5;
            font-size: 11px;
        }

        @media (max-width: 450px) {
            .login-container {
                padding: 32px 23px;
            }

            h1 {
                font-size: 26px;
            }
        }
    </style>
</head>

<body>
    <div class="login-container">

        <div class="logo">✦</div>

        <h1>Welcome Back</h1>
        <p class="subtitle">Sign in to continue to your account</p>

        <form method="POST">

            <div class="form-group">
                <label for="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    placeholder="Enter your username"
                    required
                >
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Enter your password"
                    required
                >
            </div>

            <div class="options">
                <label class="remember">
                    <input type="checkbox" name="remember">
                    Remember me
                </label>

                <a href="#" onclick="alert('Please contact the administrator to reset your password.'); return false;">Forgot password?</a>
            </div>

            <button type="submit">Sign In →</button>

        </form>

        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}

        <p class="signup">
            Secure access to your account
        </p>

        <p class="footer">
            © 2026 • LOGIN PORTAL
        </p>

    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()

        if username:
            message = f"Welcome, {username}! Form submitted successfully."

    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(debug=True)
