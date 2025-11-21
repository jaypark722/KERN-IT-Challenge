"""
Time Entry Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.time_entry import TimeEntry
from app.models.project import Project

bp = Blueprint('time_entries', __name__, url_prefix='/api/entries')


@bp.route('', methods=['GET'])
@jwt_required()
def get_time_entries():
    """Get all time entries for the current user"""
    current_user_id = int(get_jwt_identity())
    
    # Query parameters for filtering
    project_id = request.args.get('project_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    is_billable = request.args.get('is_billable')
    
    query = TimeEntry.query.filter_by(user_id=current_user_id)
    
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(TimeEntry.start_time >= start_dt)
        except ValueError:
            return jsonify({'message': 'Invalid start_date format'}), 400
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(TimeEntry.start_time <= end_dt)
        except ValueError:
            return jsonify({'message': 'Invalid end_date format'}), 400
    
    if is_billable is not None:
        query = query.filter_by(is_billable=is_billable.lower() == 'true')
    
    entries = query.order_by(TimeEntry.start_time.desc()).all()
    
    return jsonify([entry.to_dict() for entry in entries]), 200


@bp.route('/<int:entry_id>', methods=['GET'])
@jwt_required()
def get_time_entry(entry_id):
    """Get a specific time entry"""
    current_user_id = int(get_jwt_identity())
    entry = TimeEntry.query.filter_by(id=entry_id, user_id=current_user_id).first()
    
    if not entry:
        return jsonify({'message': 'Time entry not found'}), 404
    
    return jsonify(entry.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_time_entry():
    """Create a new time entry"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('project_id') or not data.get('start_time'):
        return jsonify({'message': 'project_id and start_time are required'}), 400
    
    # Verify project exists
    project = Project.query.get(data['project_id'])
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    # Parse datetime strings
    try:
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        end_time = None
        if data.get('end_time'):
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
    except ValueError as e:
        return jsonify({'message': f'Invalid datetime format: {str(e)}'}), 400
    
    entry = TimeEntry(
        user_id=current_user_id,
        project_id=data['project_id'],
        start_time=start_time,
        end_time=end_time,
        notes=data.get('notes'),
        is_billable=data.get('is_billable', True)
    )
    
    # Calculate duration if end_time is provided
    if end_time:
        entry.calculate_duration()
    
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Time entry created successfully',
        'entry': entry.to_dict()
    }), 201


@bp.route('/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_time_entry(entry_id):
    """Update an existing time entry"""
    current_user_id = int(get_jwt_identity())
    entry = TimeEntry.query.filter_by(id=entry_id, user_id=current_user_id).first()
    
    if not entry:
        return jsonify({'message': 'Time entry not found'}), 404
    
    data = request.get_json()
    
    if 'project_id' in data:
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        entry.project_id = data['project_id']
    
    if 'start_time' in data:
        try:
            entry.start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        except ValueError as e:
            return jsonify({'message': f'Invalid start_time format: {str(e)}'}), 400
    
    if 'end_time' in data:
        try:
            entry.end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        except ValueError as e:
            return jsonify({'message': f'Invalid end_time format: {str(e)}'}), 400
    
    if 'notes' in data:
        entry.notes = data['notes']
    
    if 'is_billable' in data:
        entry.is_billable = data['is_billable']
    
    # Recalculate duration
    if entry.end_time:
        entry.calculate_duration()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Time entry updated successfully',
        'entry': entry.to_dict()
    }), 200


@bp.route('/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_time_entry(entry_id):
    """Delete a time entry"""
    current_user_id = int(get_jwt_identity())
    entry = TimeEntry.query.filter_by(id=entry_id, user_id=current_user_id).first()
    
    if not entry:
        return jsonify({'message': 'Time entry not found'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Time entry deleted successfully'}), 200


@bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Get summary statistics for time entries"""
    current_user_id = int(get_jwt_identity())
    
    # Query parameters for filtering
    project_id = request.args.get('project_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = TimeEntry.query.filter_by(user_id=current_user_id)
    
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(TimeEntry.start_time >= start_dt)
        except ValueError:
            return jsonify({'message': 'Invalid start_date format'}), 400
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(TimeEntry.start_time <= end_dt)
        except ValueError:
            return jsonify({'message': 'Invalid end_date format'}), 400
    
    entries = query.all()
    
    total_duration = sum(entry.duration for entry in entries if entry.duration)
    billable_duration = sum(entry.duration for entry in entries if entry.duration and entry.is_billable)
    
    return jsonify({
        'total_entries': len(entries),
        'total_hours': round(total_duration / 3600, 2) if total_duration else 0,
        'billable_hours': round(billable_duration / 3600, 2) if billable_duration else 0,
        'non_billable_hours': round((total_duration - billable_duration) / 3600, 2) if total_duration else 0
    }), 200
