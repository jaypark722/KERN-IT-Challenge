"""
Time Entry Model
"""
from datetime import datetime
from app import db


class TimeEntry(db.Model):
    """Time entry model for tracking work hours"""
    __tablename__ = 'time_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # Duration in seconds (calculated)
    
    notes = db.Column(db.Text)
    is_billable = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_duration(self):
        """Calculate duration in seconds from start_time and end_time"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration = int(delta.total_seconds())
        return self.duration

    def to_dict(self):
        """Convert time entry object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'duration_hours': round(self.duration / 3600, 2) if self.duration else None,
            'notes': self.notes,
            'is_billable': self.is_billable,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<TimeEntry {self.id} - Project {self.project_id}>'
