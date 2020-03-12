from flask import Flask, render_template, request, redirect, escape
import vsearch
import mysql.connector as driver

app = Flask(__name__)

#@app.route('/')
#def hello() -> '302':
#    return redirect('/entry')


def log_request(req_form: 'phrase&letters', req_ip: 'IP address',browser: str, res: str) -> None:
    dbconfig = { 'host': '127.0.0.1',
                 'user': 'vsearch',
                 'password': 'vsearchpasswd',
                 'database': 'vsearchlogDB', }
    conn = driver.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req_form['phrase'],
                          req_form['letters'],
                          req_ip,
                          browser,
                          res ))
    conn.commit()
    cursor.close()
    conn.close()
    
        
@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    result = str(vsearch.search4letters(request.form['phrase'],request.form['letters']))
    log_request(request.form,request.remote_addr,request.user_agent.browser,result)
    return render_template('results.html',
                            the_title='Here are your results:',
                            the_phrase=request.form['phrase'],
                            the_letters=request.form['letters'],
                            the_results=result)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')
    
@app.route('/viewlog')
def view_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents)
        
if __name__ == '__main__':
    app.run(debug=True)
