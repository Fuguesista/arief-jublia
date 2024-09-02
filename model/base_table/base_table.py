
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()
db = SQLAlchemy(model_class=Base)

class Email(Base):
    __tablename__ = 'list_send_email'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    email_subject = db.Column(db.String(255), nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)  # Timestamp int for schedule send
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_sended = db.Column(db.Boolean, default=False, nullable=False)  # flag is finish sent
    time_send = db.Column(db.Integer, default=0)  # store the time the email was sent
    is_canceled = db.Column(db.Boolean, default=False, nullable=False)  # flag is canceled
    time_cancel = db.Column(db.Integer, default=0)  # store the time the email was sent

    def return_dict(self):
        return {
        'id': self.id,
        'event_id': self.event_id,
        'email_subject': self.email_subject,
        'email_content': self.email_content,
        'timestamp': self.timestamp,
        'created_at': self.created_at.isoformat(),
        'is_sended': self.is_sended,
        'time_send': datetime.fromtimestamp(self.time_send).strftime("%Y-%m-%d %H:%M:%S"),
        'is_canceled': self.is_canceled,
        'time_cancel': datetime.fromtimestamp(self.time_cancel).strftime("%Y-%m-%d %H:%M:%S")
        }

def give_pointer_db():
    global db
    return {"DB":db}