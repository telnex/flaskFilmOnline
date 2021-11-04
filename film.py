from flask import Flask, render_template, request, redirect, url_for, make_response
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)
AUTH = 'True45'

logging.basicConfig(level=logging.INFO, filename='./log/flask.log', filemode='a+', format='#%(levelname)s - %(asctime)s - %(message)s', datefmt='%d.%b %H:%M')
app = Flask(__name__)

@app.route('/')
def index():
    if request.cookies.get('pwd'):
        logging.info(str(request.remote_addr) + ' /index pwd is set - ' + str(request.cookies.get('pwd')))
        if request.cookies.get('pwd') == AUTH:
            link = True
            return render_template('film.html', link=link)
        else:
            return redirect(url_for('auth'))
    else:
        logging.info(str(request.remote_addr) + ' /index pwd is not set - ')
        return redirect(url_for('auth'))


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.cookies.get('pwd'):
        if request.cookies.get('pwd') == AUTH:
            link = ''
            if request.method == 'POST':
                f = request.form['link']
                id = f.split('/')
                for x in id:
                    if x.isdigit():
                        link = x
                if link == '':
                    logging.warning(str(request.remote_addr) + ' send request: ' + str(request.form))
                    return render_template('error.html')
                else:
                    return redirect(url_for('film', post_id=link))
            else:
                logging.warning(str(request.remote_addr) + ' send request: ' + str(request.form))
                return render_template('error.html')
        else:
            return redirect(url_for('auth'))
    else:
        return redirect(url_for('auth'))


@app.route('/film/<int:post_id>')
def film(post_id):
    if request.cookies.get('pwd'):
        if request.cookies.get('pwd') == AUTH:
            logging.info(str(request.remote_addr) + ' film id: ' + str(post_id))
            return render_template('film.html', id=str(post_id))
        else:
            return redirect(url_for('auth'))
    else:
        return redirect(url_for('auth'))


@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        f = request.form['wrd']
        logging.warning(str(request.remote_addr) + ' auth send: ' + str(f))
        if f == AUTH:
            res = make_response(redirect(url_for('index')))
            res.set_cookie('pwd', AUTH, max_age=60*60*24)
            return res
        pass
    return render_template('auth.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4040, debug=False)
