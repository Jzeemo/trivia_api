import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest

from flaskr import create_app
from models import Category, Question, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:123@localhost:5432', self.database_name) 
        setup_db(self.app, self.database_path)       
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    #test for get all categories
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


    #test for paginated question
    def test_paginated_questions(self): 
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)        
        self.assertTrue(data['total_questions'])

    def test_404_valid_page(self):        
        
        response = self.client().get('/questions?page=2000')
        data = json.loads(response.data)    

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)       


    def test_delete_question(self):   

        question = Question("Test Question For Deletion", "No answer",
                            4, 1)
        question.insert()        
        
        response = self.client().delete('/questions/'+str(question.id))
        data = json.loads(response.data)    
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question.id)   
    
    def test_question_creation_fails(self):

        wrong_question = {
            'question': 'What is the day after Sunday?',
            'category': '0',
            'answer':'',
            'difficulty': 1,
            }
       
        response = self.client().post('/questions', json=wrong_question)
        data = json.loads(response.data)        
        
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 422)        

    def test_create_question(self):      
        
        question = {
        'question': 'Why me?',
        'answer': 'Becoz your suck',
        'category': '1',
        'difficulty': 1,
        }

        response = self.client().post('/questions', json=question)
        data = json.loads(response.data)               
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True) 
        self.assertIsNotNone(question)
    

    def test_search_questions(self):
        
        response = self.client().post('/search_question',json={'searchTerm': 'Africa'})
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        

    def test_search_questions_fails(self):
        response = self.client().post('/search_question',json={'searchTerm': 'this is invalid question to test serach team'})
        
        data = json.loads(response.data)
       
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')    

    def test_quiz_game(self):
       
        response = self.client().post('/quizzes',json={'previous_questions': [9, 12],'quiz_category': {'type': 'History', 'id': '4'}})
        
        data = json.loads(response.data)
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)        
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 23)
       

    def test_quiz_fails(self): 
      
        response = self.client().post('/quizzes')
       
        data = json.loads(response.data)
      
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request!')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
