from datetime import datetime
from model.base_table.base_table import *

def get_due_emails():
    """
    Retrieves all emails where the timestamp is less than the current Unix timestamp 
    and the email has not been sent or canceled.
    """
    current_timestamp = int(datetime.utcnow().timestamp())
    
    due_emails = Email.query.filter(
        Email.timestamp <= current_timestamp,
        Email.is_sended == False,
        Email.is_canceled == False
    ).all()
    
    return due_emails