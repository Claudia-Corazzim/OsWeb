from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bem-vindo à documentação do OsWeb! <a href="/docs/api">API</a> | <a href="/docs/manual">Manual</a> | <a href="/docs/deploy">Deploy</a>'

@app.route('/docs/api')
def api_docs():
    return render_template('docs/api.html')

@app.route('/docs/manual')
def user_manual():
    return render_template('docs/manual.html')

@app.route('/docs/deploy')
def deploy_guide():
    return render_template('docs/deploy.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
