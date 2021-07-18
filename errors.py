from flask import render_template, request
from flaskblog import app, db


@app.errorhandler(403)
def forbidden(error):
    app.logger.error(f'Forbidden access: {error}, route: {request.url}')
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
# second value after the template, which is the error code number

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server error: {error}, route: {request.url}')
    return render_template('500.html'), 500
# rollback resets the session to a clean state