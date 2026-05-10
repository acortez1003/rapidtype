from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db
from app.models import User, Race, RaceResult, Passage
from datetime import datetime, timezone

race = Blueprint('race', __name__)

# Fetch passage
@race.route('/api/race/passage', methods=['GET'])
@jwt_required()
def passage():
    user_id = get_jwt_identity()
    avg_wpm = db.session.query(func.avg(RaceResult.wpm)).filter_by(user_id=user_id).scalar()

    if not avg_wpm or avg_wpm < 40:
        difficulty = 'beginner'
    elif avg_wpm < 70:
        difficulty = 'intermediate'
    else:
        difficulty = 'advanced'

    selected_passage = Passage.query.filter_by(difficulty=difficulty).order_by(func.random()).first()
    if not selected_passage:
        return jsonify({'error': 'No passages found'}), 404

    return jsonify({
        'text': selected_passage.text,
        'title': selected_passage.title,
        'author': selected_passage.author,
        'passage_id': selected_passage.id
    })


# Create race record
@race.route('/api/race/start', methods=['POST'])
@jwt_required()
def start():
    data = request.get_json()
    passage_id = data.get('passage_id')
    race_type = data.get('race_type')

    if not passage_id or not race_type:
        return jsonify({'error': 'Missing information'}), 400

    new_race = Race(passage_id=passage_id, race_type=race_type, status='in progress', start_time=datetime.now(timezone.utc))
    try:
        db.session.add(new_race)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500

    return jsonify({
        'race_id': new_race.id
    }), 201


# Save the RaceResult when finished
@race.route('/api/race/result', methods=['POST'])
@jwt_required()
def result():
    data = request.get_json()
    race_id = data.get('race_id')
    wpm = data.get('wpm')
    accuracy = data.get('accuracy')
    completed = data.get('completed')

    if not race_id or not wpm or not accuracy or completed is None:
        return jsonify({'error': 'Missing information'}), 400

    user_id = get_jwt_identity()

    race = Race.query.filter_by(id=race_id).first()
    if not race:
        return jsonify({'error': 'Race not found'}), 404

    race_result = RaceResult(race_id=race_id, user_id=user_id, wpm=wpm, accuracy=accuracy, completed=completed)
    
    try:
        race.end_time = datetime.now(timezone.utc)
        race.status = 'finished'
        user = User.query.filter_by(id=user_id).first()
        user.last_seen = datetime.now(timezone.utc)
        db.session.add(race_result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500

    return jsonify({
        'race_result_id': race_result.id
    }), 201