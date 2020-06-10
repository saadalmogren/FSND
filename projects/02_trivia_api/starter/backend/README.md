# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Api documentation

```
• Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration. 
• Authentication: This version of the application does not require any authentaction or Keys
 
Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return three error types when requests fail:
	• 400: Bad Request
	• 404: Not Found
	• 422: Unprocessable
    • 405: method not allowed
    • 500: server error



Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/results'
GET '/categories/<int:cate_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of question objects formated in (
        'id': self.id,
        'question': self.question,
        'answer': self.answer,
        'category': self.category,
        'difficulty': self.difficulty
      )
- Request Arguments: None
- Returns: list of question objects paginated in groups of 10, list of categories, total number of questions and the current catgory
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ....
  ]
  "total_questions": 18
}

DELETE '/questions/<int:question_id>'
- Deletes the question with the provided id 
- Request Arguments: None
- Returns: Boolean 'success' true if the question is deleted or false if there is an error

{
    "success": True
}

POST '/questions'
- Creates a new question. 
- Request Arguments: question, answer, category, difficulty
- Returns: Boolean 'success' true if the question is deleted or false if there is an error
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"question?", "answer":"answer", "category": 2, "difficulty": 3}'

{
    "success": True
}

POST '/questions/result'
- Searches for questions containing the search term. 
- Request Arguments: searchTerm, 
  category, and difficulty score.
- Returns: list of questions, total number of questions and the curretn category.
curl http://127.0.0.1:5000/questions/result -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'

GET '/categories/<int:cate_id>/questions'
- Fetches a list of questions based on the category id. 
- Request Arguments: None.
- Returns: list of questions, total number of questions and the curretn category.
curl -X GET http://127.0.0.1:5000/categories/4/questions 

{
  "current_category": 4,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "total_questions": 3
}

POST '/quizzes'
- Fetches a list of questions to play a quiz. 
- Request Arguments: a list of previous questions in the quiz and the quiz category.
- Returns: question.
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 4], "quiz_category": {"id": 4}}'
{
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```