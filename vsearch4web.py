from flask import Flask, render_template, request, session
from DBcm import UseDatabase, ConnectionException
from checker import check_logged_in

import vsearch

app = Flask(__name__)
app.secret_key = 'YouWillNeverGuess'


def log_request(req: 'flask_request', res: str) -> None:
    # with open('vsearch.log', 'a') as log:
    #    print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

    with UseDatabase('vsearch.db') as cursor:
        _SQL = """insert into viewlog values (?,?,?,?,?)"""
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res, ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results'
    results = str(vsearch.search4letters(phrase, letters))

    try:
        log_request(request, results)
    except ConnectionException as e:
        print("Error logging request:" + str(e))

    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    content = []
    # with open('vsearch.log') as log:
    # for line in log:
    #    content.append([])
    #    for item in line.split('|'):
    #        content[-1].append(escape(item))

    try:
        with UseDatabase('vsearch.db') as cursor:
            _SQL = """select phrase, letters, remote_addr, user_agent, results from viewlog"""
            cursor.execute(_SQL)
            content = cursor.fetchall()
    except ConnectionException as e:
        print("Error logging request" + str(e))

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=content,)


@app.route('/login')
def login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def logout() -> str:
    if 'logged_in' in session:
        session.pop('logged_in')
        return 'You are now logged out.'
    else:
        return 'You are already logged out.'

if __name__ == '__main__':
    app.run(port=5001, debug=True)
