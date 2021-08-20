from flask import Flask, render_template, request, redirect, url_for
import logging


log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO, filename='./log/log.log', filemode='a+', format='#%(levelname)s - %(asctime)s - %(message)s', datefmt='%d.%b %H:%M')
app = Flask(__name__)

@app.route('/')
def index():
    link = True
    return render_template('film.html', link=link)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    link = ''
    if request.method == 'POST':
        f = request.form['link']
        id = f.split('/')
        for x in id:
            if x.isdigit():
                link = x
        if link == '':
            logging.warning('Неправильный запрос: ' + str(request.form))
            return render_template('error.html')
        else:
            return redirect(url_for('film', post_id=link))
    else:
        logging.warning('Неправильный запрос: ' + str(request.form))
        return render_template('error.html')



@app.route('/film/<int:post_id>')
def film(post_id):
    return render_template('film.html', id=str(post_id))


if __name__ == "__main__":
    app.run()