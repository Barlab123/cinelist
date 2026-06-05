from flask import Blueprint, request, g, render_template, flash, url_for, redirect
from db.init import get_db
from db.repository import get_task, insert_tasks
from helpers import validate_title

web = Blueprint("web", __name__)

GENRES = ["Akcja", "Dramat", "Komedia", "Horror", "Sci-Fi", "Thriller", "Romans", "Animacja", "Dokumentalny", "Inne"]

@web.route("/")
def index():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    watched = db.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    recent = db.execute("SELECT id, title, done, genre, created_at FROM tasks ORDER BY created_at DESC LIMIT 5").fetchall()
    return render_template('home.html', total=total, watched=watched, recent=recent)

@web.route("/ping-db")
def ping_db():
    db = get_db()
    db.execute("SELECT 1").fetchone()
    return render_template('ping.html')

@web.route("/list")
def list():
    db = get_db()
    filter_genre = request.args.get("genre", "")
    filter_status = request.args.get("status", "")

    query = "SELECT id, title, done, genre, created_at FROM tasks"
    conditions = []
    params = []

    if filter_genre:
        conditions.append("genre = ?")
        params.append(filter_genre)
    if filter_status == "watched":
        conditions.append("done = 1")
    elif filter_status == "unwatched":
        conditions.append("done = 0")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY created_at DESC"

    tasks = db.execute(query, params).fetchall()
    return render_template('list.html', tasks=tasks, genres=GENRES, filter_genre=filter_genre, filter_status=filter_status)

@web.route("/tasks/<int:task_id>")
def task(task_id):
    task = get_task(task_id)
    return render_template('task.html', task=task)

@web.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title").strip()
        genre = request.form.get("genre", "Inne")
        validation = validate_title(title)
        if validation is not None:
            flash(validation, "error")
            return render_template('add_task.html', genres=GENRES, title=title, selected_genre=genre)
        insert_tasks([[title, 0, genre]])
        flash("Film dodany do watchlisty!", "success")
        return redirect(url_for('web.list'))
    return render_template('add_task.html', genres=GENRES, title="", selected_genre="Inne")

@web.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", [task_id])
    db.commit()
    flash("Film usunięty z listy.", "success")
    return redirect(url_for('web.list'))

@web.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET done = NOT done WHERE id = ?", [task_id])
    db.commit()
    is_task_view = request.form.get("is_task_view")
    flash("Status filmu zaktualizowany.", "success")
    if is_task_view == "1":
        return redirect(url_for('web.task', task_id=task_id))
    return redirect(url_for('web.list'))

@web.route("/tasks/<int:task_id>/change_title", methods=["POST"])
def change_task_title(task_id):
    title = request.form.get("title")
    validation = validate_title(title)
    if validation is not None:
        flash(validation, "error")
        return redirect(url_for('web.task', task_id=task_id))
    db = get_db()
    db.execute("UPDATE tasks SET title = ? WHERE id = ?", [title, task_id])
    db.commit()
    flash("Tytuł zmieniony.", "success")
    return redirect(url_for('web.task', task_id=task_id))