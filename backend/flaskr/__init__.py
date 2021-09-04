import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

COUNT_PER_PAGE = 10

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
        start_value = (pages - 1) * COUNT_PER_PAGE
        end_value = start_value + COUNT_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start_value:end_value]

        return current_questions

    @app.route('/categories')
    def get_all_categories():          
        
        categories_list = Category.query.all()
        categories_dict = {}
        for category in categories_list:
            categories_dict[category.id] = category.type

        # return 404 if not category found
        if (len(categories_dict) == 0):
            abort(404)

        return jsonify({'success': True,'categories': categories_dict})

    @app.route('/questions')
    def get_all_questions():

        question_list = Question.query.all()
        current_questions = paginate_questions(request,question_list)
        total_questions = len(question_list)        

        categories_list = Category.query.all()
        categories_dict = {}
        for category in categories_list:
            categories_dict[category.id] = category.type

        if (len(current_questions) == 0):
                abort(404)

        return jsonify({'success': True,'questions': current_questions,'total_questions': total_questions,'categories': categories_dict})

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):

        try:
            
            question_byid = Question.query.filter_by(id=id).one_or_none()

            #return 404 if question not found
            if question_byid is None:
                abort(404)

            # delete the question
            question_byid.delete()

            # return success response
            return jsonify({'success': True,'deleted': id})

        except:
            # return 422 if some error has happen
            abort(422)
    
    @app.route('/questions', methods=['POST'])
    def add_question():
        '''
        Handles POST requests for creating new questions and searching questions.
        '''
        #get the date
        data = request.get_json()
        
        difficulty = data.get('difficulty')
        category = data.get('category')
        question = data.get('question')
        answer = data.get('answer')
        
        if ((question is None) or (answer is None)
                or (difficulty is None) or (category is None)):
            abort(422)

        try:
            
            new_question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            new_question.insert()
            
            selection_question = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection_question)
            
            return jsonify({'success': True,'created': question.id,'question_created': question.question,'questions': current_questions,'total_questions': len(Question.query.all())})

        except:           
            abort(422)  
   

    @app.route('/search_question', methods=['POST'])
    def search_questions():        
        
        data = request.get_json()
        
        search_value = data.get('searchTerm')

        # get the data by search value
        selection_questions = Question.query.filter(Question.question.ilike(f'%{search_value}%')).all()

        # return 404 if no data has found
        if (len(selection_questions) == 0):
            abort(404)

        paginated_question_list = paginate_questions(request, selection_questions)
        
        return jsonify({'success': True,'questions': paginated_question_list,'total_questions': len(Question.query.all())})        

    
    @app.route('/categories/<int:id>/questions')
    def get_all_question_by_categories(id):        
        
        category_by_id = Category.query.filter_by(id=id).one_or_none()

        # return 404 if no data has found
        if (category_by_id is None):
            abort(400)

        # get the questions by categories
        selection_list = Question.query.filter_by(category=category_by_id.id).all()

        # get the paginated list
        paginated_list = paginate_questions(request, selection_list)
        
        return jsonify({'success': True,'questions': paginated_list,'total_questions': len(Question.query.all()),'current_category': category_by_id.type})

    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():        

        # get the request data
        data = request.get_json()

        categories_data = data.get('quiz_category')

        # get the previous questions list
        previous_questions = data.get('previous_questions')        

        # return 404 if question has no found
        if ((categories_data is None) or (previous_questions is None)):
            abort(400)

        # get all questions by categories
        if (categories_data['id'] == 0):
            questions_list = Question.query.all()        
        else:
            questions_list = Question.query.filter_by(category=categories_data['id']).all()

        # get total number of questions
        total_question = len(questions_list)        

        # check the question if already used
        def check_if_used(question):
            used_question = False
            for prev in previous_questions:
                if (prev == question.id):
                    used_question = True

            return used_question

        # get random question
        random_question = questions_list[random.randrange(0, len(questions_list), 1)]
        
        while (check_if_used(random_question)):
            random_question = questions_list[random.randrange(0, len(questions_list), 1)]
           
            if (len(previous_questions) == total_question):
                return jsonify({'success': True})
       
        return jsonify({'success': True,'question': random_question.format()})
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    return app

    