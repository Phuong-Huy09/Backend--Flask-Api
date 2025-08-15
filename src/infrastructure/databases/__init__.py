from infrastructure.databases.mssql import init_mssql
from infrastructure.models import (
    todo_model, 
    user_model,
    student_profile_model,
    tutor_profile_model,
    subject_model,
    tutor_subject_model,
    service_listing_model,
    booking_model,
    review_model,
    chat_thread_model,
    message_model,
    complaint_model,
    moderation_action_model,
    notification_model
)

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base