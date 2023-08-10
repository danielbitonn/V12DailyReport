from flask import Flask, render_template, request, Response
from src.scripts.system.applogger import APPLOGGER
import threading
import subprocess
from selenium import webdriver
import winreg
import psutil

should_shutdown = False

app = Flask(__name__)
app.logger = APPLOGGER
def get_default_browser_windows():
    path = r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice'
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
    value, _ = winreg.QueryValueEx(key, 'ProgId')
    browser_mapping = {
        "ChromeHTML": webdriver.Chrome,
        "FirefoxURL": webdriver.Firefox,
        "IE.HTTP": webdriver.Ie,
        "SafariURL": webdriver.Safari
    }
    return browser_mapping.get(value, webdriver.Firefox)()

def run_command(command):
    subprocess.run(command, shell=True)
@app.route('/')
def index():
    APPLOGGER.info('User accessed the index page.')
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_executable():
    command = request.form.get('command')
    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()
    return 'Running command: ' + command
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()
    return 'Server shutting down...'
def shutdown_server():
    a_shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if a_shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    a_shutdown_func()
def start_web_server(port):
    def shutdown_check():
        global should_shutdown
        if should_shutdown:
            shutdown_func = request.environ.get('werkzeug.server.shutdown')
            if shutdown_func is not None:
                shutdown_func()
        return Response(status=204)

    app.add_url_rule('/shutdown_check', 'shutdown_check', shutdown_check, methods=['POST'])
    app.run(host='127.0.0.1', port=port, debug=True, use_reloader=False, threaded=True)


def terminate_process_by_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            pid = conn.pid
            process = psutil.Process(pid)
            process_name = process.name()
            print(f"Port {port} is being used by {process_name}. Terminating...")
            process.terminate()
            return f"Process {process_name} using port {port} has been terminated."
    return f"Port {port} is not being used."

