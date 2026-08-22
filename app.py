from flask import Flask, render_template
from proj.Quantum_Chess.app import chess_bp

app = Flask(__name__)
app.register_blueprint(chess_bp, url_prefix='/chess')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)