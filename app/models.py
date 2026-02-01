from . import db
from datetime import datetime

class ATM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='ONLINE')  # ONLINE / OFFLINE
    cash_level = db.Column(db.Integer, default=100)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)

class NetworkStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latency_ms = db.Column(db.Integer)
    packet_loss = db.Column(db.Float)
    status = db.Column(db.String(20), default='STABLE')
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # ATM / NETWORK / APP
    message = db.Column(db.String(255))
    severity = db.Column(db.String(20))  # LOW / HIGH / CRITICAL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
