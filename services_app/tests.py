from django.test import TestCase, Client
from django.urls import reverse
import pymysql

class SignupViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

        # Database connection for checking insert
        self.conn = pymysql.connect(
            host='x24112682-utility-rds.cid6gtv3k6ak.ap-southeast-2.rds.amazonaws.com',
            user='admin',
            password='x24112682-utility-rds',
            database='x24112682-utility-rds'
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        """Cleanup after test"""
        self.cursor.execute("DELETE FROM mstr_user WHERE username = %s", ('testuser',))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_signup_success(self):
        """Test successful signup and database insertion."""
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'city': 'New York',
            'password': 'password123',
            'usertype': 'customer'
        }
        response = self.client.post(self.signup_url, data)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verify that data is inserted in mstr_user
        self.cursor.execute("SELECT * FROM mstr_user WHERE username = %s", ('testuser',))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)

        # Check session variables
        session = self.client.session
        self.assertEqual(session['username'], 'testuser')
        self.assertEqual(session['password'], 'password123')
