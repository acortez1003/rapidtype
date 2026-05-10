from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Race, RaceResult
from sqlalchemy import func

stats = Blueprint('stats', __name__)

@stats.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()

    avg_wpm = db.session.query(func.avg(RaceResult.wpm)).filter_by(user_id=user_id).scalar()
    best_wpm = db.session.query(func.max(RaceResult.wpm)).filter_by(user_id=user_id).scalar()
    avg_accuracy = db.session.query(func.avg(RaceResult.accuracy)).filter_by(user_id=user_id).scalar()
    total_races = db.session.query(func.count(RaceResult.id)).filter_by(user_id=user_id, completed=True).scalar()
    avg_place = db.session.query(func.avg(RaceResult.place))\
        .join(Race)\
        .filter(RaceResult.user_id == user_id, Race.race_type == 'multi')\
        .scalar()

    return jsonify({
        'avg_wpm': round(float(avg_wpm or 0), 2),
        'best_wpm': best_wpm or 0,
        'avg_accuracy': round(float(avg_accuracy or 0), 2),
        'total_races': total_races or 0,
        'avg_place': round(avg_place, 2) if avg_place else None
    })
