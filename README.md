API Documentation

Base URL (development): http://127.0.0.1:5000
All responses are JSON (application/json).

Error Format

On errors, the API responds with a consistent structure:

{
  "success": false,
  "error": 404,
  "message": "resource not found"
}


Error codes handled: 400, 404, 422, 500

GET /categories

Description
Fetches all available categories as a dictionary.

Request Parameters
None.

Success Response (200)

{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}


Error Response

404 if no categories exist.

GET /questions

Description
Fetches a paginated list of questions (10 per page), total number of questions, and all categories.

Query Parameters

page (optional, integer, default = 1)

Success Response (200)

{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the heaviest organ in the human body?",
      "answer": "Liver",
      "category": 1,
      "difficulty": 4
    }
  ],
  "total_questions": 42,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null
}


Error Response

404 if page is out of range.

DELETE /questions/<int:question_id>

Description
Deletes a question by ID.

Path Parameters

question_id (required)

Success Response (200)

{ "success": true, "deleted": 7 }


Error Response

404 if the question doesn’t exist

422 on database errors

POST /questions

Description
Either creates a new question or performs a search, depending on the request body.

A) Create Question

Request Body

{
  "question": "What is 5+5?",
  "answer": "10",
  "category": 1,
  "difficulty": 1
}


Success Response (201)

{ "success": true, "created": 43 }


Error Response

400 if required fields are missing

422 if category ID is invalid

B) Search (Alternative to /questions/search)

Request Body

{ "searchTerm": "title" }


Success Response (200)

{
  "success": true,
  "questions": [ /* matched questions */ ],
  "total_questions": 3,
  "current_category": null
}


Error Response

400 if searchTerm is empty

POST /questions/search

Description
Searches for questions where the text contains the search term (case-insensitive).

Request Body

{ "searchTerm": "heaviest" }


Success Response (200)

{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the heaviest organ in the human body?",
      "answer": "Liver",
      "category": 1,
      "difficulty": 4
    }
  ],
  "total_questions": 1,
  "current_category": null
}


Error Response

400 if searchTerm is empty

GET /categories/<int:category_id>/questions

(POST also supported)

Description
Fetches all questions in a given category. Supports optional pagination.

Path Parameters

category_id (required)

Query Parameters

page (optional, int)

Success Response (200)

{
  "success": true,
  "questions": [ /* questions in category */ ],
  "total_questions": 7,
  "current_category": "Science"
}


Error Response

404 if category does not exist

POST /quizzes

Description
Returns a random question to play the quiz. Excludes previously asked questions, optionally limited to a category.

Request Body

{
  "previous_questions": [1, 2, 3],
  "quiz_category": { "id": 1 }
}


id: 0 or omitted = all categories

Success Response (200) – question available

{
  "success": true,
  "question": {
    "id": 10,
    "question": "Who painted the Mona Lisa?",
    "answer": "Leonardo da Vinci",
    "category": 2,
    "difficulty": 2
  }
}


Success Response (200) – no questions left

{ "success": true, "question": null }

Example Requests (PowerShell)
# Categories
curl.exe http://127.0.0.1:5000/categories

# Questions (page=1)
curl.exe "http://127.0.0.1:5000/questions?page=1"

# Create question
$body = @{question="What is 5+5?"; answer="10"; category=1; difficulty=1} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions" -Method Post -ContentType "application/json" -Body $body

# Search
$search = @{searchTerm="heaviest"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions/search" -Method Post -ContentType "application/json" -Body $search

# Questions by category
curl.exe http://127.0.0.1:5000/categories/1/questions

# Delete question
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions/7" -Method Delete

# Quiz
$quiz = @{previous_questions=@(); quiz_category=@{id=1}} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/quizzes" -Method Post -ContentType "application/json" -Body $quiz