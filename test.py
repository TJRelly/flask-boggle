from unittest import TestCase
from app import app
from flask import session



class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
  
    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("board", session)
            self.assertIn("High Score:", html)
            self.assertIn("Games Played:", html)
            self.assertIn("<table>", html)
            self.assertIn('<form method="POST">', html)
            self.assertIsNone(session.get("high_score"))
            self.assertIsNone(session.get("games_played"))
            
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        
        response = self.client.post('/guess', json={'guess': 'cat'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.post('/guess', json={'guess': 'boggle'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.post('/guess', json={'guess': 'hsjdoibnsodn'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'not-word')
        
    def test_high_score(self):
        """Test if high score is updated"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['high_score'] = 100

        response = self.client.post('/score', json={'score': 50})
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json['high_score'], 100)

    def test_games_played(self):
        """Test if games played is incremented by 1"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['games_played'] = 100

        response = self.client.post('/score', json={'score': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['games_played'], 101)
            
        

