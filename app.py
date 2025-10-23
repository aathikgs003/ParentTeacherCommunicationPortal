from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from models import db

login_manager = LoginManager()
mail = Mail()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.teacher_routes import teacher_bp
    from routes.parent_routes import parent_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(parent_bp, url_prefix='/parent')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from models.user_model import User
    return User.query.get(int(user_id))

# -----------------------------------------------
# Gunicorn fix: Instantiate the application here
# -----------------------------------------------
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
