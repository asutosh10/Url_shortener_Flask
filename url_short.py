from flask import Flask,render_template,request,redirect,url_for,flash,abort,session
import json
import os.path

app=Flask(__name__)
app.secret_key='abracadabra'

@app.route('/')
def index():
    return render_template('index.html',codes=session.keys())

@app.route('/process',methods=['GET','POST'])
def process():
    if request.method=='POST':
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls=json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash('already taken brother')
            return redirect(url_for('index'))

        urls[request.form['code']]={'url':request.form['url']}
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']]=True #session activated
        return render_template('your_url.html',code=request.form['code'],url=request.form['url'])
    else:
        return redirect(url_for('index'))

@app.route('/<code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls=json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                  return redirect(urls[code]['url'])
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
