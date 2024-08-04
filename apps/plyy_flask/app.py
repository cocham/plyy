# app.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'plyy_page'

    from views import main, logout, mypage, login, curator, api_curator, like_curator, unlike_curator, like_plyy, unlike_plyy

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(logout, url_prefix='/')
    app.register_blueprint(mypage, url_prefix='/')
    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(curator, url_prefix='/')
    app.register_blueprint(api_curator, url_prefix='/')
    app.register_blueprint(like_curator, url_prefix='/')
    app.register_blueprint(unlike_curator, url_prefix='/')
    app.register_blueprint(like_plyy, url_prefix='/')
    app.register_blueprint(unlike_plyy, url_prefix='/')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
