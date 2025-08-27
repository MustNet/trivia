ToDos

Use Flask-CORS to enable cross-domain requests and set response headers.
curl.exe -I -X OPTIONS http://127.0.0.1:5000/questions `
  -H "Origin: http://localhost:3000" `
  -H "Access-Control-Request-Method: GET"

Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
curl.exe "http://127.0.0.1:5000/questions?page=1"
curl.exe "http://127.0.0.1:5000/questions?page=9999"

Create an endpoint to handle GET requests for all available categories.
curl.exe http://127.0.0.1:5000/categories

Create an endpoint to DELETE a question using a question ID.
$new = J(@{question="Temp delete"; answer="bye"; category=1; difficulty=1})
$r   = Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions" -Method Post -ContentType "application/json" -Body $new
$id  = $r.created
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions/$id" -Method Delete

Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
$body = J(@{question="What is 5+5?"; answer="10"; category=1; difficulty=1})
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions" -Method Post -ContentType "application/json" -Body $body


Create a POST endpoint to get questions based on category.
curl.exe http://127.0.0.1:5000/categories/1/questions

Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
$search = J(@{searchTerm="heaviest"})  
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions/search" -Method Post -ContentType "application/json" -Body $search

Create a POST endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
$quiz = J(@{previous_questions=@(); quiz_category=@{id=1}})
Invoke-RestMethod -Uri "http://127.0.0.1:5000/quizzes" -Method Post -ContentType "application/json" -Body $quiz

Create error handlers for all expected errors including 400, 404, 422, and 500.

400
$empty = J(@{searchTerm=""})
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions/search" -Method Post -ContentType "application/json" -Body $empty

404
curl.exe http://127.0.0.1:5000/categories/999/questions

422
$fk = J(@{question="Bad cat"; answer="x"; category=9999; difficulty=1})
Invoke-RestMethod -Uri "http://127.0.0.1:5000/questions" -Method Post -ContentType "application/json" -Body $fk
