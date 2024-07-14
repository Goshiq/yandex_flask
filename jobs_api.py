import flask
from flask import jsonify, make_response, request

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
                [job.to_dict(only=("job", "team_leader", "collaborators", "work_size")) for job in res]
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
            "jobs": res.to_dict(only=("job", "team_leader", "collaborators", "work_size"))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})
