from flask import Flask, render_template
from _utils.officers import parse_data
import sys

# Initialize Flask app
app = Flask(__name__)

f = open('officers.txt')
data = f.read()
f.close()
officers = parse_data(data)
#print(officers, file=sys.stdout)

# PAGES
@app.route('/')
@app.route('/index.html')
def page_index():    
    return render_template('index.html')

@app.route('/about.html')
def page_about():
    return render_template('about.html')

@app.route('/officers.html')
def page_officers():
    f = open('officers.txt')
    data = f.read()
    f.close()
    officers = parse_data(data)
    return render_template('officers.html', officers=officers)

@app.route('/test.html')
def page_test():
    return render_template('test.html')

# TESTING
#'''
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 2020))
    app.run(debug=True, threaded=False, host='0.0.0.0', port=port)
#'''