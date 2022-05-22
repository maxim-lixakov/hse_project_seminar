# import enum
#
# from sqlalchemy import Enum
# from sqlalchemy.dialects.postgresql import JSON
# from datetime import datetime
#
# from . import db
#
#
# class TaskStatus(str, enum.Enum):
#     new = 'NEW'
#     processing = 'PROCESSING'
#     processed = 'PROCESSED'
#     canceled = "CANCELED"
#     error = 'ERROR'
#
#
# class Callback(db.Model):
#     """Model for describing callback status for response from this server"""
#
#     __tablename__ = 'callback'
#
#     id = db.Column(db.Integer, primary_key=True)
#     task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
#     date_created = db.Column(db.DateTime(), default=datetime.utcnow)
#     callback_status = db.Column(db.Integer)
#
#
# class Task(db.Model):
#     """Model for describing incoming request and its current status"""
#
#     __tablename__ = 'task'
#
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(Enum(TaskStatus), default=TaskStatus.new)
#     response = db.Column(JSON)
#     url_id = db.Column(db.Integer)
#     price = db.Column(db.Float)
#     image_url = db.Column(db.String)
#     image_base64 = db.Column(db.String)
#     callback = db.Column(db.String)
#     server_callback = db.relationship('Callback')
#
#
# class Config(db.Model):
#     """Model to storage configs of promocode images"""
#
#     __tablename__ = 'config'
#
#     id = db.Column(db.Integer, primary_key=True)
#     locations = db.Column(JSON)
#     markers = db.Column(JSON)
#     date_created = db.Column(db.DateTime(), default=datetime.utcnow)
#
#
# db.create_all()
# db.session.commit()
