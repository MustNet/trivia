# test_flaskr.py
import os, unittest, json
from flaskr import create_app
from flaskr.models import db, Question, Category

TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://postgres:PASSWORT@localhost:5432/trivia_test"
)

class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        # App mit Test-DB erzeugen (create_app bindet die DB bereits!)
        self.app = create_app({"SQLALCHEMY_DATABASE_URI": TEST_DB_URL})
        self.client = self.app.test_client

        # Frische Tabellen + Seed-Daten
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            c1 = Category(type="Science")
            c2 = Category(type="Art")
            db.session.add_all([c1, c2])
            db.session.flush()

            q1 = Question(question="What is H2O?", answer="Water", category=c1.id, difficulty=1)
            q2 = Question(question="Who painted Mona Lisa?", answer="Leonardo da Vinci", category=c2.id, difficulty=2)
            db.session.add_all([q1, q2])
            db.session.commit()

        self.new_question = {
            "question": "What is 2+2?",
            "answer": "4",
            "category": 1,
            "difficulty": 1,
        }

    def tearDown(self):
        pass

    # -------- Categories --------
    def test_get_categories_success(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["categories"]), 2)

    # -------- Questions (GET + pagination) --------
    def test_get_questions_paginated_success(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)
        self.assertIn("categories", data)

    def test_get_questions_beyond_valid_page_404(self):
        res = self.client().get("/questions?page=9999")
        self.assertEqual(res.status_code, 404)

    # -------- Create Question --------
    def test_create_question_success(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

    def test_create_question_400_missing_fields(self):
        res = self.client().post("/questions", json={"question": "Incomplete"})
        self.assertEqual(res.status_code, 400)

    # -------- Delete Question --------
    def test_delete_question_success(self):
        # create first
        res_create = self.client().post("/questions", json=self.new_question)
        created_id = json.loads(res_create.data)["created"]

        res = self.client().delete(f"/questions/{created_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], created_id)

    def test_delete_question_404_not_found(self):
        res = self.client().delete("/questions/999999")
        self.assertEqual(res.status_code, 404)

    # -------- Search --------
    def test_search_questions_success(self):
        res = self.client().post("/questions/search", json={"searchTerm": "what"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["total_questions"], 1)

    def test_search_questions_400_empty_term(self):
        res = self.client().post("/questions/search", json={"searchTerm": ""})
        self.assertEqual(res.status_code, 400)

    # -------- By Category --------
    def test_get_questions_by_category_success(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertEqual(data["current_category"], "Science")

    def test_get_questions_by_category_404(self):
        res = self.client().get("/categories/999/questions")
        self.assertEqual(res.status_code, 404)

    # -------- Quizzes --------
    def test_play_quiz_success(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {"id": 1}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("question", data)

    def test_play_quiz_none_left(self):
        with self.app.app_context():
            ids = [q.id for q in Question.query.filter(Question.category == 1).all()]

        res = self.client().post("/quizzes", json={
            "previous_questions": ids,
            "quiz_category": {"id": 1}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(data["question"])


if __name__ == "__main__":
    unittest.main()
