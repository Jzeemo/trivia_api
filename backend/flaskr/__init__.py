import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Category, Question, setup_db
from sqlalchemy.sql.expression import false


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app) 
    
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        '''
        Sets access control.
        '''
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate_questions(request, selection):
        pages = request.args.get('page', 1, type=int)
        start_value = (pages - 1) * 10
        end_value = start_value + 10

        questions = [question.format() for question in selection]
        current_questions = questions[start_value:end_value]

        return current_questions

    @app.route('/categories')
    def get_all_categories():   


        #get all category
        categories = Category.query.all()

        #conver to dict
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        # return 404 if not category found
        if (len(categories_dict) == 0):
            abort(404)

        return jsonify({'success': True,'categories': categories_dict}) 


        

    @app.route('/questions')
    def get_all_questions():

        #get all question
        questions = Question.query.all()

        #paginate the questions
        current_questions = paginate_questions(request,questions)
        total_questions = len(questions)  

                

        #check question and if len 0, just return 404
        if (len(current_questions) == 0):
            abort(404)

        
        #get all categories 
        categories = Category.query.all()

        #convert to category type dict
        category_type_dict = {}
        for category in categories:
            category_type_dict[category.id] = category.type        

        

        return jsonify({'success': True,'questions': current_questions,'total_questions': total_questions,'categories': category_type_dict})
        

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):

        
            
        #get question by id
        question_byid = Question.query.filter(Question.id == id).one_or_none()

        #return 404 if question not found
        if question_byid is None:
            abort(404)

        # delete the question
        question_byid.delete()

        # return success response
        return jsonify({'success': True,'deleted': id})

        
    
    @app.route('/questions', methods=['POST'])
    def add_question():
        
        #get the request_data
        request_body = request.get_json()
        
        difficulty = request_body['difficulty']
        category = request_body['category']
        question = request_body['question']
        answer = request_body['answer']

        #check the request data is correct or not
        if ((question is None) or (answer is None)
                or (difficulty is None) or (category is None)):
            abort(500)

        
        try:

            #question create
            question = Question(question, answer,category,difficulty)
            question.insert()
            
            #get total question and current question
            total_question = len(Question.query.all())
            current_questions = paginate_questions(request, Question.query.order_by(Question.id).all())
            
            return jsonify({'success': True,'created': question.id,'question_created': question.question,'questions': current_questions,'total_questions': total_question })
        except Exception:
            abort(422)
          
   

    @app.route('/search_question', methods=['POST'])
    def search_questions():  

        
        #get the request_data
        request_body = request.get_json()
        
        #get the search_value from request_body
        search_value = request_body['searchTerm']           

        # get the data by search value
        selection_questions = Question.query.filter(Question.question.ilike(f'%{search_value}%')).all()

        # return 404 if no data has found
        if (len(selection_questions) == 0):
            abort(404)
        
        #get the total question and paginated questions 
        total_question = len(Question.query.all())
        paginated_questions = paginate_questions(request, selection_questions)
        
        return jsonify({'success': True,'questions': paginated_questions,'total_questions': total_question})
           
    
    @app.route('/categories/<int:id>/questions')
    def get_all_question_by_categories(id):        
        
        
        #get the category by id
        category_by_id = Category.query.filter_by(id = id).one_or_none()

        print("here")

        # return 404 if no data has found
        if (category_by_id is None):
            abort(400)

        # get the questions by categories
        selection_list = Question.query.filter_by(category=category_by_id.id).all()

        # get the paginated list
        total_question = len(Question.query.all())
        paginated_list = paginate_questions(request, selection_list)
        
        return jsonify({'success': True,'questions': paginated_list,'total_questions': total_question,'current_category': category_by_id.type})

    

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():        

    
        # get the request data
        request_body = request.get_json()

        if(request_body is None):
            abort(400)        

        categories_data = request_body['quiz_category']

        # get the previous questions list
        previous_questions = request_body['previous_questions']

        category_id = categories_data['id']

        # return 404 if question has no found
        if ((categories_data is None) or (previous_questions is None) or (category_id is None)):
            abort(400)            

        # get all questions by categories
        if (category_id == 0):
            questions_list = Question.query.all()        
        else:
            questions_list = Question.query.filter_by(category=category_id).all()            

        if (len(previous_questions) == len(questions_list)):
            return jsonify({'success': True,'message': "No more questions!"})

        #this part is to get the random question            
                    
        random_question = random.choice(questions_list).format()                      

        while(random_question['id'] in previous_questions): 
            random_question = random.choice(questions_list).format()
            print(random_question['question'])

        return jsonify({'success': True,'question': random_question})


    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable, input syntex error"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request!"
        }), 400
    return app

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error! Sry"
        }), 400
    return app


    