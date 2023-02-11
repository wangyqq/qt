from flask import Flask
app = Flask(__name__)
from flask import Flask, request, render_template
@app.route('/')
def index():
	return render_template('index2.html')

@app.route("/backend-endpoint",methods=['POST'])
def backend_console():
    print("This is output from the backend console")
    return "This is output from the backend console"

if __name__ == "__main__":
    app.run()