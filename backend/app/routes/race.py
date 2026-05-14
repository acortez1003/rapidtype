from flask import Blueprint, request, jsonify
from flask_socketio import join_room, emit
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db
from app.models import User, Race, RaceResult, Passage
from datetime import datetime, timezone

race = Blueprint('race', __name__)

# Multiplayer room
@race.route('/api/race/join', methods=['POST'])
@jwt_required()
def join():
    user_id = get_jwt_identity()
    waiting_race = Race.query.filter_by(status='waiting', race_type='multi').first()
    if waiting_race:
        player_count = RaceResult.query.filter_by(race_id=waiting_race.id).count()
        if player_count >= 5:
            waiting_race = None # full
    
    if not waiting_race:
        selected_passage = Passage.query.order_by(func.random()).first()
        if not selected_passage:
            return jsonify({'error': 'No passages found'}), 404
        new_race = Race(passage_id=selected_passage.id, race_type='multi', status='waiting')
        try:
            db.session.add(new_race)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Something went wrong'}), 500
        waiting_race = new_race

    passage = Passage.query.get(waiting_race.passage_id)

    race_result = RaceResult(race_id=waiting_race.id, user_id=user_id)
    try:
        db.session.add(race_result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500

    return jsonify({
        'race_id': waiting_race.id,
        'passage_text': passage.text,
        'passage_title': passage.title,
        'passage_author': passage.author
    }), 200

@race.route('/api/race/solo', methods=['POST'])
@jwt_required()
def solo():
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
    
    race = Race(passage_id=selected_passage.id, race_type='solo', status='in progress', start_time=datetime.now(timezone.utc))
    try:
        db.session.add(race)
        db.session.commit()
        race_result = RaceResult(race_id=race.id, user_id=user_id)
        db.session.add(race_result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500
    
    return jsonify({
        'race_id': race.id,
        'passage_text': selected_passage.text,
        'passage_title': selected_passage.title,
        'passage_author': selected_passage.author
    }), 201

# Save the RaceResult when finished (solo only)
@race.route('/api/race/result', methods=['POST'])
@jwt_required()
def result():
    user_id = get_jwt_identity()
    data = request.get_json()
    race_id = data.get('race_id')
    wpm = data.get('wpm')
    accuracy = data.get('accuracy')
    if not race_id or not wpm or not accuracy is None:
        return jsonify({'error': 'Missing information'}), 400

    race = Race.query.filter_by(id=race_id).first()
    if not race:
        return jsonify({'error': 'Race not found'}), 404

    race_result = RaceResult.query.filter_by(race_id=race_id, user_id=user_id).first()
    if not race_result:
        return jsonify({'error': 'Race result not found'}), 404
    race_result.wpm = wpm
    race_result.accuracy = accuracy
    race_result.completed = True

    try:
        race.end_time = datetime.now(timezone.utc)
        race.status = 'finished'
        user = User.query.filter_by(id=user_id).first()
        user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500

    return jsonify({
        'race_result_id': race_result.id
    }), 201