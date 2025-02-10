from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import os
from datetime import datetime

app = Flask(__name__)

# Connect to Redis service defined in docker-compose
redis_conn = Redis(host='redis', port=6379)
q = Queue('pdf_tasks', connection=redis_conn)

@app.route('/submit', methods=['POST'])
def submit_task():
    try:
        data = request.json
        if not data or 'pdf_url' not in data:
            return jsonify({'error': 'Missing pdf_url'}), 400
        
        # Create a unique task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare task data
        task_data = {
            'pdf_url': data['pdf_url'],
            'options': data.get('options', {}),
            'submitted_by': data.get('submitted_by', 'anonymous'),
            'task_id': task_id
        }
        
        # Enqueue the task
        job = q.enqueue(
            'consumer.process_job',
            task_data,
            job_id=task_id
        )
        
        return jsonify({
            'status': 'success',
            'job_id': job.id,
            'task_id': task_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
