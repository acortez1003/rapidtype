from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Race, RaceResult
from sqlalchemy import func

leaderboard = Blueprint('leaderboard', __name__)

@leaderboard.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    results = db.session.query(
        User.username,
        func.avg(RaceResult.wpm).label('avg_wpm')
    )\
    .join(RaceResult, User.id == RaceResult.user_id)\
    .filter(RaceResult.completed == True)\
    .group_by(User.id)\
    .order_by(func.avg(RaceResult.wpm).desc())\
    .limit(10)\
    .all()

    return jsonify({
        'leaderboard': [
        {
            'username': row.username,
            'avg_wpm': round(float(row.avg_wpm), 2)
        }
        for row in results
        ]
})