# Full Stack Trivia API Project
This project is to play the game where user can test their knowledge by answering trivia questions. This is project for Udacity Nano Degree project and task is to create an API and
test suite for implementating the following functionality:

- Display questions - User can see the all question by category and difficulty rating.
- Delete questions - User can delete the question.
- Add question - User can add the question and their answers.
- Search question - User can search the questions
- Play the quiz game - User can see the question by randomizing either all question or within a specific category

## Getting Started

### Installing Dependencies
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

Directory to flaskr and then

At Window :

```bash
$env:FLASK_APP = "__init__.py"
flask run
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started
#### GET /categories

* Description: Returns a list categories.
* Sample: `http://localhost:5000/categories`<br>

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "success": true
        }


#### GET /questions?page=<page_number>

* Description:
  * Returns a list questions.
  * Page is the page number u want to see

* Sample: `http://localhost:5000/questions`<br>

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "questions": [
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Tom Cruise",
                    "category": 5,
                    "difficulty": 4,
                    "id": 4,
                    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                    "answer": "Edward Scissorhands",
                    "category": 5,
                    "difficulty": 3,
                    "id": 6,
                    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                }
            ],
            "success": true,
            "total_questions": 21
        }

#### DELETE /questions/\<int:id\>

* Description:
  * Deletes a question by id 
  * Returns id of deleted question upon success.
* Sample: Delete Method `http://localhost:5000/questions/6`<br>

        {
            "deleted": 6, 
            "success": true
        }

#### POST /questions

* Description:
  * Creates a new question
  * Returns JSON object with newly created question
* Sample: POST Method`http://localhost:5000/questions'{
            "question": "What is the color of ocean if u look from space?",
            "answer": "blue",
            "difficulty": 3,
            "category": "3"
        }'`<br>

        
#### Search Question : POST /questions

* Description:
  * Searches for questions using search_question parameter .
  * Returns JSON object with paginated matching questions.
* Sample: POST Method `http://localhost:5000/search_question`<br>

This is the body of request

    `{
        "searchTerm":"What"
    }`

        
#### GET /categories/\<int:id\>/questions

* Description:
  * Gets questions by category id.
  * Returns JSON object with paginated matching questions.
* Sample: `http://localhost:5000/categories/1/questions`<br>

        {
            "current_category": "Science",
            "questions": [
                {
                    "answer": "The Liver",
                    "category": 1,
                    "difficulty": 4,
                    "id": 20,
                    "question": "What is the heaviest organ in the human body?"
                },
                {
                    "answer": "Blood",
                    "category": 1,
                    "difficulty": 4,
                    "id": 22,
                    "question": "Hematology is a branch of medicine involving the study of what?"
                },
                {
                    "answer": "",
                    "category": 1,
                    "difficulty": 1,
                    "id": 27,
                    "question": "What is the day after Sunday?"
                }
            ],
            "success": true,
            "total_questions": 20
        }

#### POST /quizzes

* Description:
  * Get a random question given by category 
  * Returns JSON object with random question not among previous questions.
* Sample: POST Method `http://localhost:5000/quizzes`
<br>

Request Body

'{"previous_questions": [9, 12],
  "quiz_category": {"type": "History", "id": "4"}}'`<br>

        {
            "question": {
                "answer": "Scarab",
                "category": 4,
                "difficulty": 4,
                "id": 23,
                "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            },
            "success": true
        }
