"""
Project Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.project import Project

bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """Get all projects"""
    status = request.args.get('status')
    include_stats = request.args.get('include_stats', 'false').lower() == 'true'
    
    query = Project.query
    
    if status:
        query = query.filter_by(status=status)
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    return jsonify([project.to_dict(include_stats=include_stats) for project in projects]), 200


@bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Get a specific project"""
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    include_stats = request.args.get('include_stats', 'false').lower() == 'true'
    return jsonify(project.to_dict(include_stats=include_stats)), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    print(f"[DEBUG] Received project data: {data}")  # Debug logging
    
    if not data or not data.get('name'):
        return jsonify({'message': 'Project name is required'}), 400
    
    try:
        project = Project(
            name=data['name'],
            description=data.get('description'),
            status=data.get('status', 'active'),
            color=data.get('color', '#3B82F6')
        )
        
        db.session.add(project)
        db.session.commit()
        
        print(f"[DEBUG] Project created successfully: {project.id}")  # Debug logging
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
    except Exception as e:
        print(f"[ERROR] Failed to create project: {str(e)}")  # Debug logging
        db.session.rollback()
        return jsonify({'message': f'Failed to create project: {str(e)}'}), 500


@bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update an existing project"""
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    if 'status' in data:
        project.status = data['status']
    if 'color' in data:
        project.color = data['color']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Project updated successfully',
        'project': project.to_dict()
    }), 200


@bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete a project"""
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({'message': 'Project deleted successfully'}), 200
