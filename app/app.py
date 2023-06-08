from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Hello, world! Current time is: {current_time}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)