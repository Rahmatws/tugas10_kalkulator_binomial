from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def binomial_probability(n, p, k):
    def factorial(x):
        return 1 if x == 0 else x * factorial(x - 1)

    comb = factorial(n) / (factorial(k) * factorial(n - k))
    probability = comb * (p ** k) * ((1 - p) ** (n - k))
    return probability

def generate_pmf_plot(n, p):
    x = list(range(n + 1))
    y = [binomial_probability(n, p, k) for k in x]

    plt.figure()
    plt.bar(x, y, color='blue', alpha=0.7)
    plt.title('Probability Mass Function (PMF)')
    plt.xlabel('Number of Successes (k)')
    plt.ylabel('Probability')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    pmf_plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return pmf_plot_url

def generate_cdf_plot(n, p):
    x = list(range(n + 1))
    y = [sum(binomial_probability(n, p, i) for i in range(k + 1)) for k in x]

    plt.figure()
    plt.step(x, y, where='post', color='green', alpha=0.7)
    plt.title('Cumulative Distribution Function (CDF)')
    plt.xlabel('Number of Successes (k)')
    plt.ylabel('Cumulative Probability')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    cdf_plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return cdf_plot_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])

        if n < 0 or p < 0 or p > 1 or k < 0 or k > n:
            return "Invalid input. Please ensure 0 <= p <= 1, 0 <= k <= n, and n >= 0."

        # Calculate the probability for P(X = 0) to P(X = k)
        probabilities = [binomial_probability(n, p, i) for i in range(k + 1)]
        cumulative_probability = sum(probabilities)

        # Generate PMF and CDF plots
        pmf_plot_url = generate_pmf_plot(n, p)
        cdf_plot_url = generate_cdf_plot(n, p)

        # Steps for calculation
        step_details = ""
        for i in range(k + 1):
            comb = math.comb(n, i)
            step = (
                f"P(X={i}) = C(n={n}, k={i}) * (p^{i}) * ((1-p)^{n-i}) = "
                f"{comb} * ({p}^{i}) * ({1 - p}^{n - i}) = {probabilities[i]:.4f}\n"
            )
            step_details += step

        return render_template(
            'index.html',
            result=round(probabilities[k], 4),
            steps=step_details.strip(),
            cumulative_probability=round(cumulative_probability, 4),
            pmf_plot_url=pmf_plot_url,
            cdf_plot_url=cdf_plot_url,
            n=n, p=p, k=k
        )
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
