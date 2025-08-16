import jwt
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from infrastructure.models.user_model import UserModel
from infrastructure.models.subject_model import SubjectModel
from infrastructure.repositories.subject_repository import SubjectRepository
from infrastructure.databases.mssql import session
from domain.models.subject import Subject, SubjectLevel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET'])
def login():
    return jsonify({'message': 'Hot reload test - Login endpoint is working!'}), 200


@auth_bp.route('/test-subject-repository', methods=['GET'])
def test_subject_repository():
    """Test endpoint để kiểm tra Subject Repository methods"""
    try:
        # Test SubjectRepository với shared session
        subject_repo = SubjectRepository(session=session)
        
        # Test get all subjects
        subject = subject_repo.get_by_id(1)
        return jsonify({
            "id": subject.id,
            "name": subject.name,
            "level": subject.level.value if hasattr(subject.level, "value") else str(subject.level),
            "created_at": subject.created_at.isoformat() if subject.created_at else None
        }), 200        
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'id': subject.id if hasattr(subject, 'id') else 'unknown',
                'name': subject.name if hasattr(subject, 'name') else 'unknown',
                'level': str(subject.level) if hasattr(subject, 'level') else 'unknown'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total_subjects': len(subjects),
                'subjects': subjects_data,
                'repository_type': 'SubjectRepository',
                'session_management': 'Shared session from controller'
            },
            'message': 'SubjectRepository test completed successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error testing SubjectRepository'
        }), 500
