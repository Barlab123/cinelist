from db.init import get_db

def insert_tasks(tasks):
    db = get_db()
    cur = db.executemany("INSERT INTO tasks(title,done,genre) VALUES (?, ?, ?)", tasks)
    db.commit()
    return cur.fetchall()

def get_task(task_id):
    db = get_db()
    row = db.execute("SELECT id, title, done, genre, created_at FROM tasks WHERE id = ?", [task_id]).fetchone()
    return row

def get_task_by_title(title):
    db = get_db()
    existingTask = db.execute("SELECT id FROM tasks WHERE title LIKE ?", [title]).fetchone()
    return existingTask
