# push
Offical push server for the openSchool app. You're required to setup it, if you want to build custom app.

# Requirements
* Python 3
* An HTTP server (if running in production. we recommend to use Nginx)
* Firebase Cloud Messaging ( Cloud Messaging API (Legacy) )

# Setup
1. Install requirements with `pip install -r requirements.txt`
2. Rename `config.py.example` to `config.py` and fill in the values
3. Configure your web server to run the FastCGI application, if you are in the production environment. Otherwise, you can use the Flask built-in web server. In that case, run: `python main.py`