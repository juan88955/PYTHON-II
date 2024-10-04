from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = Flask(__name__)

class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    done: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

tasks_db = []

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(**data, id=len(tasks_db) + 1)
    tasks_db.append(task)
    return jsonify(task.dict()), 201

@app.route('/tasks', methods=['GET'])
def read_tasks():
    return jsonify([task.dict() for task in tasks_db])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def read_task(task_id):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task:
        return jsonify(task.dict())
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task:
        data = request.json
        updated_task = Task(**data, id=task_id)
        tasks_db[tasks_db.index(task)] = updated_task
        return jsonify(updated_task.dict())
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task:
        tasks_db.remove(task)
        return '', 204
    return jsonify({"error": "Task not found"}), 404

@app.route('/', methods=['GET', 'POST'])
def task_form():
    if request.method == 'POST':
        data = request.form
        task = Task(**data, id=len(tasks_db) + 1)
        tasks_db.append(task)
        return render_template('tasks.html', tasks=tasks_db, message="Tarea creada exitosamente")
    return render_template('tasks.html', tasks=tasks_db)

if __name__ == '__main__':
    app.run(debug=True)
