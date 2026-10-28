
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

services = {
    "Basic Wash": 299,
    "Premium Wash": 599,
    "Interior Cleaning": 799,
    "Full Car Detailing": 1499
}

bookings = []

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ShinePro Car Wash</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #f3f7fc;
    color: #172b4d;
}

nav {
    background: #092b50;
    color: white;
    padding: 20px 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

nav h2 {
    color: #39c6ff;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 18px;
}

.hero {
    padding: 65px 8%;
    background: linear-gradient(120deg, #092b50, #087cbd);
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
    flex-wrap: wrap;
}

.hero-content {
    max-width: 560px;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 52px);
    margin-bottom: 18px;
}

.hero p {
    line-height: 1.7;
    color: #e1efff;
}

.hero img {
    width: 100%;
    max-width: 380px;
    border-radius: 18px;
}

.btn {
    display: inline-block;
    background: #23c5f5;
    color: #062a49;
    padding: 13px 22px;
    border: none;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
    margin-top: 22px;
}

section {
    padding: 48px 8%;
}

.heading {
    text-align: center;
    margin-bottom: 28px;
}

.heading h2 {
    font-size: 30px;
    margin-bottom: 10px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 5px 20px #0a315012;
    border: 1px solid #e3ebf4;
}

.card .emoji {
    font-size: 38px;
}

.card h3 {
    margin: 15px 0 10px;
}

.price {
    font-size: 25px;
    color: #087cbd;
    font-weight: bold;
    margin-top: 15px;
}

.booking-section {
    background: #e8f2fc;
}

.booking-box {
    max-width: 650px;
    margin: auto;
    padding: 30px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 5px 20px #0a315012;
}

label {
    display: block;
    margin: 15px 0 7px;
    font-weight: bold;
}

input, select {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd6e3;
    border-radius: 7px;
    font-size: 15px;
}

input:focus, select:focus {
    outline: 2px solid #23a9e8;
}

.booking-box button {
    width: 100%;
}

.notice {
    background: #e4f9ed;
    color: #12663b;
    padding: 16px;
    border-radius: 9px;
    margin-bottom: 20px;
    line-height: 1.8;
}

.error {
    background: #fff0ed;
    color: #a32716;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 15px;
}

footer {
    background: #092b50;
    color: white;
    padding: 25px;
    text-align: center;
}

@media (max-width: 600px) {
    nav {
        padding: 18px 5%;
    }
    nav a {
        margin-left: 0;
        margin-right: 12px;
    }
    .hero, section {
        padding: 38px 5%;
    }
    .booking-box {
        padding: 20px;
    }
}
</style>
</head>

<body>

<nav>
    <h2>🚘 ShinePro</h2>
    <div>
        <a href="#home">Home</a>
        <a href="#services">Services</a>
        <a href="#booking">Book Now</a>
    </div>
</nav>

<div class="hero" id="home">
    <div class="hero-content">
        <h1>Your Car Deserves a Perfect Shine!</h1>
        <p>
            Professional car washing and detailing services.
            Book your appointment online and let us make
            your car look fresh, clean and beautiful.
        </p>
        <a href="#booking" class="btn">Book Your Wash →</a>
    </div>

    <img
      src="https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=800&q=85"
      alt="Professional car wash">
</div>

<section id="services">
    <div class="heading">
        <h2>Our Services</h2>
        <p>Choose the perfect wash for your car.</p>
    </div>

    <div class="cards">
        <div class="card">
            <div class="emoji">🚿</div>
            <h3>Basic Wash</h3>
            <p>Exterior wash and basic cleaning.</p>
            <div class="price">₹299</div>
        </div>

        <div class="card">
            <div class="emoji">✨</div>
            <h3>Premium Wash</h3>
            <p>Exterior wash, wheel cleaning and polish.</p>
            <div class="price">₹599</div>
        </div>

        <div class="card">
            <div class="emoji">🧽</div>
            <h3>Interior Cleaning</h3>
            <p>Seats, dashboard and interior cleaning.</p>
            <div class="price">₹799</div>
        </div>

        <div class="card">
            <div class="emoji">🚘</div>
            <h3>Full Detailing</h3>
            <p>Complete interior and exterior detailing.</p>
            <div class="price">₹1499</div>
        </div>
    </div>
</section>

<section class="booking-section" id="booking">
    <div class="heading">
        <h2>Book Your Car Wash</h2>
        <p>Enter your details to schedule a service.</p>
    </div>

    <div class="booking-box">

        {% if success %}
        <div class="notice">
            <h3>✅ Booking Submitted Successfully!</h3>
            <p>Booking ID: #{{ booking.id }}</p>
            <p>Customer: {{ booking.name }}</p>
            <p>Car: {{ booking.car }}</p>
            <p>Service: {{ booking.service }}</p>
            <p>Date: {{ booking.date }}</p>
            <p>Total Price: ₹{{ booking.price }}</p>
            <p>Please contact the service provider to confirm
            your appointment.</p>
        </div>
        {% endif %}

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <form action="/book" method="POST">
            <label for="name">Customer Name</label>
            <input id="name" type="text" name="name"
                   placeholder="Enter your full name"
                   maxlength="80" required>

            <label for="phone">Phone Number</label>
            <input id="phone" type="tel" name="phone"
                   placeholder="Enter 10-digit mobile number"
                   pattern="[0-9]{10}" maxlength="10" required>

            <label for="car">Car Model</label>
            <input id="car" type="text" name="car"
                   placeholder="e.g. Hyundai i20"
                   maxlength="80" required>

            <label for="service">Select Service</label>
            <select id="service" name="service" required>
                <option value="">-- Choose a service --</option>
                {% for service, price in services.items() %}
                <option value="{{ service }}">
                    {{ service }} - ₹{{ price }}
                </option>
                {% endfor %}
            </select>

            <label for="date">Appointment Date</label>
            <input id="date" type="date" name="date"
                   min="{{ today }}" required>

            <button type="submit" class="btn">
                Confirm Booking
            </button>
        </form>
    </div>
</section>

<footer>
    <p>© 2026 ShinePro Car Wash | Keep Your Car Shining ✨</p>
</footer>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        services=services,
        success=False,
        error=None,
        today=datetime.today().strftime("%Y-%m-%d")
    )


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    car = request.form.get("car", "").strip()
    service = request.form.get("service", "")
    date = request.form.get("date", "")

    error = None
    booking = None

    if not name or not car:
        error = "Please enter your name and car model."
    elif not phone.isdigit() or len(phone) != 10:
        error = "Please enter a valid 10-digit phone number."
    elif service not in services:
        error = "Please select a valid service."
    else:
        try:
            appointment = datetime.strptime(date, "%Y-%m-%d").date()
            if appointment < datetime.today().date():
                error = "Please select today or a future date."
        except ValueError:
            error = "Please select a valid appointment date."

    if not error:
        booking = {
            "id": len(bookings) + 1,
            "name": name,
            "phone": phone,
            "car": car,
            "service": service,
            "date": date,
            "price": services[service]
        }
        bookings.append(booking)

    return render_template_string(
        HTML,
        services=services,
        success=booking is not None,
        booking=booking,
        error=error,
        today=datetime.today().strftime("%Y-%m-%d")
    )


if __name__ == "__main__":
    app.run(debug=True)
