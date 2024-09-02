import unittest
from main import app, db
from model.base_table.base_table import *
from config.read_config import read_config
import json
from datetime import datetime

data_config = read_config("config/base_config.ini")
class SaveEmailsTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a temporary database
        app.config['TESTING'] = True
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Delete DB After test
        # with app.app_context():
        #     db.session.remove()
        #     db.drop_all()
        # Delete new ID After Test
        with app.app_context():
            email = Email.query.get_or_404(self.id_delete)
            db.session.delete(email)
            db.session.commit()

    def test_save_emails(self):
        response = self.app.post('/save_emails', data={
            'event_id': 1,
            'email_subject': 'Test Subject',
            'email_content': 'Test Content',
            'timestamp': datetime.fromtimestamp(1700000000).strftime('%Y-%m-%d %H:%M:%S')
        })
        # Verify no error with status code 201
        self.assertEqual(response.status_code, 201)


        # verify if the id is contain in return data 
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
        self.id_delete = response_data['id']
        # Check if the data is inserted properly
        with app.app_context():
            email = Email.query.get_or_404(response_data['id'])
            self.assertIsNotNone(email)
            self.assertEqual(email.event_id, 1)
            self.assertEqual(email.email_subject, 'Test Subject')
            self.assertEqual(email.email_content, 'Test Content')
            self.assertEqual(email.timestamp, 1700000000)
            self.assertFalse(email.is_sended)
            self.assertFalse(email.is_canceled)
            self.assertEqual(email.time_send, 0)
            self.assertEqual(email.time_cancel, 0)

if __name__ == '__main__':
    unittest.main()