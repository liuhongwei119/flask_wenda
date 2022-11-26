from flask import Flask, session, g
import config
from exts import db, mail
from models import UserModel
from blueprint.qa import bp as qa_bp
from blueprint.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
# set_config from config.py
app.config.from_object(config)
# init_db,mail
db.init_app(app)
mail.init_app(app)
# ORM_migrate
migrate = Migrate(app, db)
# register blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)


# before_request/ before_first_request/ after_request
# hook
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
