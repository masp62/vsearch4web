from flask import Flask, render_template, request
from DBcm import UseDatabase
import vsearch

app = Flask(__name__)


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
    log_request(request, results)

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
def view_the_log() -> 'html':
    content = []
    # with open('vsearch.log') as log:
    # for line in log:
    #    content.append([])
    #    for item in line.split('|'):
    #        content[-1].append(escape(item))
    with UseDatabase('vsearch.db') as cursor:
        _SQL = """select phrase, letters, remote_addr, user_agent, results from viewlog"""
        cursor.execute(_SQL)
        content = cursor.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=content,)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
