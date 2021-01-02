from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

# __name__ is literally the name of the file.
app = Flask(__name__)
app.secret_key = 'asldkfj;asdkj'        # Allows for secure connection to user

# Webpage and corresponding app below.
@app.route('/')
def home():
    return render_template('home.html', name='Michael')

# Webpage and corresponding app below.
@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        # check for repeating  entries
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # If there is a repeat, redirect back to the home page (regardless of the extention)
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another.')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            # Add the code and url to the urls dictionary
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)      # Making the file name a combination of the code and the original filename
            f.save('/Users/michael/documents/github/Flask-Projects/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
        return render_template('your_url.html', code=request.form['code'])      # request.args requests the code arguement from the form and displays it
    else:
        return redirect(url_for('home'))

# variable response
@app.route('/<string:code>')
def redirect_to_urls(code):
    if os.path.exists('urls.json'):         # Check if json file exists
        with open('urls.json') as urls_file:        # Open json file
            urls = json.load(urls_file)         # Load json file ino urls var
            if code in urls.keys():         # If the website extension is found in the keys of the dictionary...
                if 'url' in urls[code].keys():           # ... and if that code translates to a url address...
                    return redirect(urls[code]['url'])          # return the redirect to the user to the corresponding address.
