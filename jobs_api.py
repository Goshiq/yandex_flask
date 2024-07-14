import flask
from flask import jsonify, make_response

from data import db_session
from data.jobs import Jobs
from main import app

blueprint = flask.Blueprint(
    "jobs_api",
    __name__,
    template_folder="templates"
)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@blueprint.route("/api/jobs")
def get_jobs():
    db_sess = db_session.create_session()
    res = db_sess.query(Jobs).all()
    return jsonify(
        {
            "jobs":
                [job.to_dict(only=("job", "team_leader", "collaborators")) for job in res]
        }
    )


@blueprint.route("/api/job/<job_id>", methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    res = db_sess.query(Jobs).get(job_id)
    if not res:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            "jobs": res.to_dict(only=("job", "team_leader", "collaborators"))
        }
    )
