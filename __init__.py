from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from .models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(req, selection):
    page = req.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return [q.format() for q in selection][start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, database_path=database_path)

    # --- CORS: allow all origins ---
    CORS(app, resources={r"*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    # --- Set Access-Control headers on every response ---
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS"
        )
        return response

    # ---------- Helpers ----------
    def categories_dict():
        cats = Category.query.order_by(Category.id).all()
        return {c.id: c.type for c in cats}

    # ---------- Routes ----------

    # GET: all categories
    @app.route("/categories", methods=["GET"])
    def get_categories():
        cats = categories_dict()
        if not cats:
            abort(404)
        return jsonify({"success": True, "categories": cats})

    # GET: questions (paginated, 10 per page)
    @app.route("/questions", methods=["GET"])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current = paginate_questions(request, selection)
        if len(current) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": current,
                "total_questions": len(selection),
                "current_category": None,
                "categories": categories_dict(),
            }
        )

    # DELETE: question by id
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        q = Question.query.get(question_id)
        if not q:
            abort(404)
        try:
            db.session.delete(q)
            db.session.commit()
            return jsonify({"success": True, "deleted": question_id})
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # POST: create question OR search (if body contains searchTerm)
    @app.route("/questions", methods=["POST"])
    def create_or_search_question():
        body = request.get_json() or {}

        # If searchTerm is provided, treat as search endpoint
        if "searchTerm" in body:
            term = (body.get("searchTerm") or "").strip()
            if term == "":
                abort(400)
            selection = (
                Question.query.filter(Question.question.ilike(f"%{term}%"))
                .order_by(Question.id)
                .all()
            )
            return jsonify(
                {
                    "success": True,
                    "questions": [q.format() for q in selection],
                    "total_questions": len(selection),
                    "current_category": None,
                }
            )

        # Otherwise: create a question
        question = (body.get("question") or "").strip()
        answer = (body.get("answer") or "").strip()
        category = body.get("category")
        difficulty = body.get("difficulty")

        if not question or not answer or category is None or difficulty is None:
            abort(400)

        try:
            q = Question(
                question=question,
                answer=answer,
                category=int(category),
                difficulty=int(difficulty),
            )
            db.session.add(q)
            db.session.commit()
            return jsonify({"success": True, "created": q.id}), 201
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # POST: (explicit) search endpoint
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        term = (request.get_json() or {}).get("searchTerm", "").strip()
        if term == "":
            abort(400)
        selection = (
            Question.query.filter(Question.question.ilike(f"%{term}%"))
            .order_by(Question.id)
            .all()
        )
        return jsonify(
            {
                "success": True,
                "questions": [q.format() for q in selection],
                "total_questions": len(selection),
                "current_category": None,
            }
        )

    # GET: questions by category (also accepts POST like einige Starterprojekte)
    @app.route("/categories/<int:category_id>/questions", methods=["GET", "POST"])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            abort(404)
        selection = (
            Question.query.filter(Question.category == category_id)
            .order_by(Question.id)
            .all()
        )
        # optional pagination via ?page=
        page = request.args.get("page", type=int)
        current = (
            paginate_questions(request, selection)
            if page
            else [q.format() for q in selection]
        )
        return jsonify(
            {
                "success": True,
                "questions": current,
                "total_questions": len(selection),
                "current_category": category.type,
            }
        )

    # POST: quizzes (random next question by category, excluding previous)
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json() or {}
        previous_questions = body.get("previous_questions", []) or []
        quiz_category = body.get("quiz_category", {}) or {}
        category_id = quiz_category.get("id")

        query = Question.query
        if category_id and int(category_id) != 0:
            query = query.filter(Question.category == int(category_id))
        if previous_questions:
            query = query.filter(~Question.id.in_(previous_questions))

        candidates = query.all()
        if not candidates:
            return jsonify({"success": True, "question": None})

        question = random.choice(candidates)
        return jsonify({"success": True, "question": question.format()})

    # ---------- Error Handlers ----------
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            500,
        )

    return app
