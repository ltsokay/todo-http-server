from flask import Flask, request, jsonify
from tasks import Task
from storage import Storage
from logger import log

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
storage = Storage()

tasks = storage.load()
next_id = max([t.id for t in tasks], default=0) + 1


def save_state():
    storage.save(tasks)
    log.info("Tasks saved to file")


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json()
    title = data.get("title")
    priority = data.get("priority")

    if not title or not priority:
        return jsonify({"error": "title and priority required"}), 400

    new_task = Task(id=next_id, title=title, priority=priority)
    next_id += 1
    tasks.append(new_task)

    save_state()
    return jsonify(new_task.to_dict()), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify([t.to_dict() for t in tasks])


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for t in tasks:
        if t.id == task_id:
            return jsonify(t.to_dict())
    return jsonify({"error": "Not found"}), 404


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    for t in tasks:
        if t.id == task_id:
            t.isDone = True
            save_state()
            return "", 200
    return "", 404


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    for t in tasks:
        if t.id == task_id:

            t.title = data.get("title", t.title)
            t.priority = data.get("priority", t.priority)
            t.isDone = data.get("isDone", t.isDone)

            save_state()
            return jsonify(t.to_dict()), 200

    return "", 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks

    before = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]

    if len(tasks) == before:
        return "", 404

    save_state()
    return "", 200


@app.errorhandler(Exception)
def handle_error(e):
    log.error(str(e))
    return jsonify({"error": "internal server error"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    log.info("Server started")
    app.run(debug=True, port=5000)
