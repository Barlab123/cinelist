from flask import Blueprint, jsonify, request, abort
from db.init import get_db
from db.repository import insert_tasks

api = Blueprint("api", __name__)

@api.route("/tasks", methods=["GET"])
def api_tasks_list():
    db = get_db()
    rows = db.execute("SELECT id, title, done, genre, created_at FROM tasks ORDER BY created_at DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@api.route("/tasks/<int:task_id>", methods=["GET"])
def api_tasks_get(task_id):
    db = get_db()
    row = db.execute("SELECT id, title, done, genre, created_at FROM tasks WHERE id = ?", [task_id]).fetchone()
    if row is None:
        abort(404, description="Movie not found")
    return jsonify(dict(row))

@api.route("/tasks", methods=["POST"])
def api_tasks_add():
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, description="Missing JSON or title")
    title = data["title"].strip()
    if len(title) < 4:
        abort(400, description="Title has to have more than 3 chars")
    db = get_db()
    existingTask = db.execute("SELECT id FROM tasks WHERE title LIKE ?", [title]).fetchone()
    if existingTask:
        abort(400, description=f"Movie already exists: {title}")
    done = 1 if data.get("done") else 0
    genre = data.get("genre", "Inne")
    task = [[title, done, genre]]
    inserted_row = insert_tasks(task)[0]
    db.commit()
    return jsonify(dict(inserted_row)), 201


@api.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def api_tasks_update(task_id):
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Missing JSON")
    title = data.get("title")
    done = data.get("done")
    genre = data.get("genre")
    db = get_db()
    row = db.execute("SELECT id FROM tasks WHERE id = ?", [task_id]).fetchone()
    if row is None:
        abort(404, description="Movie not found")
    if title is not None:
        title = title.strip()
        if len(title) < 4:
            abort(400, description="Title has to have more than 3 chars")
        existingTask = db.execute("SELECT id FROM tasks WHERE title LIKE ?", [title]).fetchone()
        if existingTask:
            abort(400, description=f"Movie already exists: {title}")
        db.execute("UPDATE tasks SET title = ? WHERE id = ?", [title, task_id])
    if done is not None:
        db.execute("UPDATE tasks SET done = ? WHERE id = ?", [1 if done else 0, task_id])
    if genre is not None:
        db.execute("UPDATE tasks SET genre = ? WHERE id = ?", [genre, task_id])
    db.commit()
    updated_row = db.execute("SELECT id, title, done, genre, created_at FROM tasks WHERE id = ?", [task_id]).fetchone()
    return jsonify(dict(updated_row))

@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def api_tasks_delete(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", [task_id])
    db.commit()
    if cur.rowcount == 0:
        abort(404, description="Movie not found")
    return "", 204