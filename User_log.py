
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Login credentials
USERNAME = "admin"
PASSWORD = "admin123"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cartoon Login</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Trebuchet MS", Arial, sans-serif;
}

body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 25px;
    background: linear-gradient(135deg, #a8e5ff, #e4f6ff, #c6e3ff);
    overflow-x: hidden;
}

.cloud {
    position: fixed;
    width: 180px;
    height: 60px;
    background: #ffffff80;
    border-radius: 50px;
    filter: blur(1px);
    z-index: 0;
}

.cloud::before,
.cloud::after {
    content: "";
    position: absolute;
    background: inherit;
    border-radius: 50%;
}

.cloud::before {
    width: 75px;
    height: 75px;
    top: -35px;
    left: 25px;
}

.cloud::after {
    width: 95px;
    height: 95px;
    top: -45px;
    right: 20px;
}

.cloud.one {
    top: 12%;
    left: 5%;
}

.cloud.two {
    right: 4%;
    bottom: 12%;
    transform: scale(.7);
}

.login-card {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 420px;
    padding: 38px;
    background: #ffffff;
    border: 4px solid #ffffff;
    border-radius: 30px;
    box-shadow: 0 18px 45px #3980b530;
    animation: floatIn .7s ease;
}

@keyframes floatIn {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.avatar {
    width: 100px;
    height: 100px;
    margin: 0 auto 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 57px;
    background: #d8f0ff;
    border: 3px solid #83c5ff;
    box-shadow: 0 6px 15px #80baff35;
}

h1 {
    text-align: center;
    font-size: 29px;
    color: #203563;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    color: #7c8bad;
    margin-bottom: 28px;
}

label {
    display: block;
    font-size: 14px;
    font-weight: bold;
    color: #34466f;
    margin-bottom: 9px;
}

.input-group {
    display: flex;
    align-items: center;
    border: 2px solid #dce6fb;
    border-radius: 14px;
    padding: 0 13px;
    margin-bottom: 20px;
    transition: .25s;
    background: #fbfdff;
}

.input-group:focus-within {
    border-color: #5790ff;
    box-shadow: 0 0 0 4px #5790ff15;
}

.input-icon {
    font-size: 21px;
    margin-right: 10px;
}

input {
    width: 100%;
    min-width: 0;
    border: none;
    outline: none;
    padding: 15px 0;
    background: transparent;
    color: #253858;
    font-size: 14px;
}

input::placeholder {
    color: #9aa9c7;
}

.show-btn {
    border: none;
    background: transparent;
    color: #4079ef;
    font-weight: bold;
    font-size: 11px;
    cursor: pointer;
}

.login-btn {
    width: 100%;
    padding: 16px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(100deg, #4d8cff, #3269ed);
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 7px 15px #4d8cff45;
    transition: .25s;
}

.login-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 11px 22px #4d8cff60;
}

.login-btn:active {
    transform: scale(.98);
}

.message {
    padding: 13px;
    margin-top: 18px;
    border-radius: 12px;
    text-align: center;
    font-size: 13px;
    line-height: 1.5;
}

.success {
    color: #197348;
    background: #e8fff1;
    border: 1px solid #b4efcb;
}

.error {
    color: #c73333;
    background: #fff0f0;
    border: 1px solid #ffd0d0;
}

.footer {
    text-align: center;
    margin-top: 26px;
    color: #93a0bc;
    font-size: 11px;
}

.footer span {
    color: #4386f5;
    font-weight: bold;
}

@media (max-width: 480px) {
    .login-card {
        padding: 30px 22px;
    }

    h1 {
        font-size: 25px;
    }
}
</style>
</head>

<body>

<div class="cloud one"></div>
<div class="cloud two"></div>

<div class="login-card">

    <div class="avatar">👦🏻</div>

    <h1>Welcome Back! 👋</h1>
    <p class="subtitle">Login to your account</p>

    <form method="POST">

        <label for="username">Username</label>
        <div class="input-group">
            <span class="input-icon">👤</span>
            <input
                type="text"
                id="username"
                name="username"
                placeholder="Enter your username"
                autocomplete="username"
                required
            >
        </div>

        <label for="password">Password</label>
        <div class="input-group">
            <span class="input-icon">🔒</span>
            <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                autocomplete="current-password"
                required
            >
            <button
                type="button"
                class="show-btn"
                onclick="togglePassword()"
            >SHOW</button>
        </div>

        <button class="login-btn" type="submit">
            Login &nbsp; →
        </button>

    </form>

    {% if message %}
    <div class="message {{ status }}">
        {{ message }}
    </div>
    {% endif %}

    <div class="footer">
        Powered by <span>Flask</span> ☁ |
        Cartoon Login App
    </div>

</div>

<script>
function togglePassword() {
    const password = document.getElementById("password");
    const button = document.querySelector(".show-btn");

    if (password.type === "password") {
        password.type = "text";
        button.textContent = "HIDE";
    } else {
        password.type = "password";
        button.textContent = "SHOW";
    }
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            message = "🎉 Login successful! Welcome back, admin!"
            status = "success"
        else:
            message = "❌ Invalid username or password!"
            status = "error"

    return render_template_string(
        HTML,
        message=message,
        status=status
    )

if __name__ == "__main__":
    app.run(debug=True)
