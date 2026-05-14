from flask_socketio import join_room, emit
from flask import request
from app.models import Race, RaceResult
from datetime import datetime, timezone
from app import db, socketio

player_rooms = {} # { session_id: race_id, user_id: user_id }
race_places = {}

@socketio.on('join_room')
def handle_join_room(data):
    race_id = data.get('race_id')
    user_id = data.get('user_id')
    player_rooms[request.sid] = {
        'race_id': race_id,
        'user_id': user_id
    }

    join_room(str(race_id))
    player_count = RaceResult.query.filter_by(race_id=race_id).count()
    emit('player_joined', {
        'player_count': player_count,
        'user_id': user_id
        }, room=str(race_id))

    if player_count >= 2:
        emit('countdown_start', {
            'countdown': 10
        }, room=str(race_id))

@socketio.on('disconnect')
def handle_disconnect():
    session_data = player_rooms.pop(request.sid, None)
    if not session_data:
        return
    race_id = session_data['race_id']
    user_id = session_data['user_id']

    # remove RaceResult if status was waiting
    if Race.query.filter_by(id=race_id, status='waiting').first():
        race_result = RaceResult.query.filter_by(race_id=race_id, user_id=user_id).first()
        try:
            db.session.delete(race_result)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    
    player_count = RaceResult.query.filter_by(race_id=race_id).count()
    if player_count < 2:
        emit('countdown_reset', {
            'countdown': 10
        }, room=str(race_id))

    emit('player_left', {
        'player_count': player_count,
        'user_id': user_id
    }, room=str(race_id))

@socketio.on('player_progress')
def handle_player_progress(data):
    race_id = data.get('race_id')
    user_id = data.get('user_id')
    progress = data.get('progress') # percentage 0 - 100
    emit('player_progress', {
        'user_id': user_id,
        'progress': progress
    }, room=str(race_id))

@socketio.on('race_start')
def handle_race_start(data):
    race_id = data.get('race_id')
    race_places[race_id] = 1
    # update race record
    race = Race.query.filter_by(id=race_id).first()
    race.status = 'in progress'
    race.start_time = datetime.now(timezone.utc)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    
    emit('race_start', {
        'race_id': race_id
    }, room=str(race_id))

@socketio.on('player_finished')
def handle_player_finished(data):
    race_id = data.get('race_id')
    user_id = data.get('user_id')
    wpm = data.get('wpm')
    accuracy = data.get('accuracy')

    place = race_places.get(race_id, 1)
    race_places[race_id] = place + 1

    race_result = RaceResult.query.filter_by(race_id=race_id, user_id=user_id).first()
    race_result.wpm = wpm
    race_result.accuracy = accuracy
    race_result.place = place
    race_result.completed = True
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    total_players = RaceResult.query.filter_by(race_id=race_id).count()
    finished_players = RaceResult.query.filter_by(race_id=race_id, completed=True).count()

    emit('player_finished', {
        'race_id': race_id,
        'user_id': user_id,
        'place': place
    }, room=str(race_id))

    if finished_players == total_players:
        race = Race.query.filter_by(id=race_id).first()
        race.status = 'finished'
        race.end_time = datetime.now(timezone.utc)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        emit('race_finished', {'race_id': race_id}, room=str(race_id))