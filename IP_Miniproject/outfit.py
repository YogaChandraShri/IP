from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def dress(layout, material):
    # Convert layout to grayscale
    gray = cv2.cvtColor(layout, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    dress_area = cv2.bitwise_and(material, material, mask=mask)
    
    # Save the output in uploads folder
    output_filename = 'output.jpg'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    cv2.imwrite(output_path, dress_area)
    
    return output_filename  # return the filename to use in HTML

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home/<username>')
def home_login(username):
    return render_template('design.html', username=username)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded"
    username = request.form['username']
    file = request.files['file']
    style = request.form['style']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    if style == 'chudidhar':
        layout = cv2.imread(r"C:\Users\syoga\AppData\Local\Programs\Python\Python313\chudithar.jpg")
        img = cv2.imread(filepath)
        material = cv2.resize(img, (layout.shape[1], layout.shape[0]))
        output_filename = dress(layout, material)  # get saved filename
    
    if style == 'frock':
        layout = cv2.imread(r"C:\Users\syoga\AppData\Local\Programs\Python\Python313\frock.jpg")
        img = cv2.imread(filepath)
        material = cv2.resize(img, (layout.shape[1], layout.shape[0]))
        output_filename = dress(layout, material)  # get saved filename

    if style == 'Tshirt':
        layout = cv2.imread(r"C:\Users\syoga\AppData\Local\Programs\Python\Python313\tshirt.jpg")
        img = cv2.imread(filepath)
        material = cv2.resize(img, (layout.shape[1], layout.shape[0]))
        output_filename = dress(layout, material)  # get saved filename

    

    return render_template('result.html', username=username,
                           input_image=file.filename,
                           output_image=output_filename,
                           style=style)

if __name__ == "__main__":
    app.run(debug=True,port=5000)
#now this is my code whether the output image is stored in uploads