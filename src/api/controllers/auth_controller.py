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
    
    return jsonify({'message': 'Ô mai gót!'}),400


@auth_bp.route('/test-subject-repository', methods=['GET'])
def test_subject_repository():
    try:
        subject_repo = SubjectRepository(session=session)
        
        subject = subject_repo.count()
        return jsonify({
            'success': True,
            'data': {
                'total_subjects': subject,
                'repository_type': 'SubjectRepository',
                'session_management': 'Shared session from controller'
            },
            'message': '123456789'
        }), 200       
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error testing SubjectRepository'
        }), 500
