from flask import Flask, render_template

app = Flask(__name__)

# Ana sayfayı açan fonksiyon
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)