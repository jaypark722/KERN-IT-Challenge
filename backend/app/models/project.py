"""
Project Model
"""
from datetime import datetime
from app import db


class Project(db.Model):
    """Project model for organizing time entries"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active', nullable=False)  # active, archived, completed
    color = db.Column(db.String(7), default='#3B82F6')  # Hex color for UI
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    time_entries = db.relationship('TimeEntry', backref='project', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_stats=False):
        """Convert project object to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_stats:
            total_duration = sum(entry.duration for entry in self.time_entries if entry.duration)
            data['total_hours'] = round(total_duration / 3600, 2) if total_duration else 0
            data['entry_count'] = self.time_entries.count()
        
        return data

    def __repr__(self):
        return f'<Project {self.name}>'
