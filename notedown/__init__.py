# this file contain the application factory, and it tells python that
# notedown directory should be treated as a package.

import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # __name__ is the name of the current python module. the app need to know where it is located to set up some paths.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'notedown.sqlite'), 
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # registering database
    from . import db
    db.init_app(app)

    # registering blueprint
    from . import auth
    app.register_blueprint(auth.bp)



    return app