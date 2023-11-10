from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Access form data
        data = request.form['input_field_name']
        # Do something with the data

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
