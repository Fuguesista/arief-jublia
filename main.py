from model.scheduller_mailler.scheduller_mailler import *
from flask import Flask, render_template, jsonify, request, redirect, url_for
from config.read_config import read_config
from model.base_table.base_table import *
from datetime import datetime
from time import gmtime, strftime

app = Flask(__name__)


data_config = read_config("config/base_config.ini")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + data_config["SQLLITE_FILE_NAME"]
global_var = give_pointer_db()
db = global_var["DB"]
db.init_app(app)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(value).strftime(format)

@app.post("/save_emails")
@app.post("/save_emails/")
def save_emails():
    # data = request.get_json()
    try:
        event_id = request.form['event_id']
        email_subject = request.form['email_subject']
        email_content = request.form['email_content']
        timestamp = request.form['timestamp']

        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp_int = int(timestamp.timestamp())

        # Create an Email object
        email = Email(
            event_id=event_id,
            email_subject=email_subject,
            email_content=email_content,
            timestamp=timestamp_int  # Store as Unix timestamp
        )

        # Save to the database
        db.session.add(email)
        db.session.commit()

        return jsonify({"error":0, 'message': 'Email saved and scheduled successfully!', 'id': email.id}), 201
    
    except Exception as e:
        return jsonify({"error":1, 'message': str(e)}), 400

@app.route('/')
def manage_emails():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    emails_query = Email.query.order_by(Email.id.asc())
    paginated_emails = emails_query.paginate(page=page, per_page=per_page, error_out=False)
    str_gmt = "GMT"+ strftime("%z", gmtime())
    return render_template('main.html', emails=paginated_emails, server_timezone=str_gmt)

@app.route('/cancel_email/<int:email_id>', methods=['GET'])
@app.route('/cancel_email/<int:email_id>/', methods=['GET'])
def cancel_email(email_id):
    try:
        email = Email.query.get_or_404(email_id)
        
        if email.is_sended:
            return redirect(url_for('manage_emails'))
        
        if email.is_canceled:
            return redirect(url_for('manage_emails'))

        email.is_canceled = True
        email.time_cancel = int(datetime.utcnow().timestamp())
        db.session.commit()

        return redirect(url_for('manage_emails'))

    except Exception as e:
        return redirect(url_for('manage_emails'))

@app.route('/delete_email/<int:email_id>', methods=['GET'])
@app.route('/delete_email/<int:email_id>/', methods=['GET'])
def delete_email(email_id):
    try:
        email = Email.query.get_or_404(email_id)
        db.session.delete(email)
        db.session.commit()
        return redirect(url_for('manage_emails'))

    except Exception as e:
        return redirect(url_for('manage_emails'))
    
@app.get('/emails')
@app.get('/emails/')
def get_emails():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        sort_by = request.args.get('sort_by', 'id', type=str)
        order = request.args.get('order', 'asc', type=str)

        if sort_by not in ['id', 'event_id', 'timestamp', 'created_at', 'is_sended', 'time_send', 'is_canceled', 'time_cancel']:
            return jsonify({'error': 'Invalid sort_by parameter'}), 400
        
        if order not in ['asc', 'desc']:
            return jsonify({'error': 'Invalid order parameter'}), 400
        
        emails_query = Email.query.order_by(getattr(getattr(Email, sort_by), order)())
        paginated_emails = emails_query.paginate(page=page, per_page=per_page, error_out=False)
        
        emails = [email.return_dict() for email in paginated_emails.items]
        
        return jsonify({
            'emails': emails,
            'total': paginated_emails.total,
            'pages': paginated_emails.pages,
            'current_page': paginated_emails.page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=8000, debug=True)