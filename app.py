from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Input from the form
    arrival_rate = float(request.form['arrivalRate'])  # λ
    service_rate = float(request.form['serviceRate'])  # μ

    # Number of servers (for M/M/2)
    num_servers = 2

    # Traffic intensity
    rho = arrival_rate / (num_servers * service_rate)

    # Stability condition check
    if rho >= 1:
        L = LQ = W = WQ = float('inf')  # System is unstable
    else:
        # Calculate P0 (probability of zero customers in the system)
        sum_term = sum((arrival_rate / service_rate) ** n / math.factorial(n) for n in range(num_servers))
        p0_denom = sum_term + ((arrival_rate / service_rate) ** num_servers / math.factorial(num_servers)) * \
                   (1 / (1 - rho))
        P0 = 1 / p0_denom

        # Average number in the queue (LQ)
        LQ = (P0 * ((arrival_rate / service_rate) ** num_servers) * rho) / \
             (math.factorial(num_servers) * ((1 - rho) ** 2))

        # Average number in the system (L)
        L = LQ + (arrival_rate / service_rate)

        # Average time in the system (W)
        W = L / arrival_rate

        # Average time in the queue (WQ)
        WQ = LQ / arrival_rate

    # Detailed calculation steps (if needed)
    steps = [
        {
            'title': "Step 1: Traffic Intensity (ρ)",
            'equation': f"ρ = λ / (c * μ) = {arrival_rate} / ({num_servers} * {service_rate}) = {rho:.2f}"
        },
        {
            'title': "Step 2: Probability of Zero Customers (P0)",
            'equation': f"P0 = 1 / (sum_terms + ...)"
        },
        {
            'title': "Step 3: Average Number of Customers in Queue (LQ)",
            'equation': f"LQ = (P0 * (λ/μ)^c * ρ) / (c! * (1-ρ)^2) = {LQ:.2f}"
        },
        {
            'title': "Step 4: Average Number of Customers in System (L)",
            'equation': f"L = LQ + (λ/μ) = {LQ:.2f} + ({arrival_rate}/{service_rate}) = {L:.2f}"
        },
        {
            'title': "Step 5: Average Time in System (W)",
            'equation': f"W = L / λ = {L:.2f} / {arrival_rate} = {W:.2f} hours"
        },
        {
            'title': "Step 6: Average Time in Queue (WQ)",
            'equation': f"WQ = LQ / λ = {LQ:.2f} / {arrival_rate} = {WQ:.2f} hours"
        }
    ]

    # Render results to the HTML template
    return render_template('result.html', rho=rho, L=L, LQ=LQ, W=W, WQ=WQ, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)
