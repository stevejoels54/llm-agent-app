from flask import Flask, request, jsonify
import os
import uuid
import inngest
import inngest.flask
from dotenv import load_dotenv
from utils.redis_helper import (
    get_job_status,
    set_job_status,
    get_all_jobs,
)
from utils.ollama_helper import get_ollama_client
from utils.container_utils import is_running_in_container
from utils.agent_workflows import (
    analyze_user_prompt,
    research_agent_workflow,
    reasoning_agent_workflow,
    simple_qa_workflow
)

load_dotenv()

app = Flask(__name__)

INNGEST_ENV = os.getenv("INNGEST_ENV", "dev").lower()
IS_PRODUCTION = INNGEST_ENV in {"prod", "production"}

inngest_kwargs = {
    "app_id": os.getenv("INNGEST_APP_ID", "llm-agent-app"),
    "is_production": IS_PRODUCTION,
}

signing_key = os.getenv("INNGEST_SIGNING_KEY")
event_key = os.getenv("INNGEST_EVENT_KEY")
if signing_key:
    inngest_kwargs["signing_key"] = signing_key
if event_key:
    inngest_kwargs["event_key"] = event_key

inngest_client = inngest.Inngest(**inngest_kwargs)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """API endpoint to trigger AI agent processing"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400
        
        job_id = str(uuid.uuid4())
        
        prompt_text = data["prompt"]
        set_job_status(job_id, "processing", None, None, prompt=prompt_text)
        
        inngest_client.send_sync(
            inngest.Event(
                name="agent/process",
                data={
                    "job_id": job_id,
                    "prompt": data["prompt"],
                    "session_id": data.get("session_id", "default")
                }
            )
        )
        
        return jsonify({
            "job_id": job_id,
            "status": "processing",
            "message": "Agent processing started"
        }), 202
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status/<job_id>', methods=['GET'])
def get_job_status_endpoint(job_id):
    """Get the status and result of a job"""
    job_status = get_job_status(job_id)
    if job_status is None:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify(job_status)

@app.route('/api/jobs', methods=['GET'])
def get_all_jobs_endpoint():
    """Get all jobs from Redis"""
    try:
        limit = request.args.get('limit', 100, type=int)
        all_jobs = get_all_jobs(limit=limit)
        jobs_list = []
        for job_id, job_data in all_jobs.items():
            job_entry = {
                "job_id": job_id,
                **job_data
            }
            jobs_list.append(job_entry)
        return jsonify({"jobs": jobs_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Serve the web GUI"""
    return app.send_static_file('index.html')

@app.route('/demo')
def return_results():
    """Demo endpoint for testing Ollama connection"""
    client = get_ollama_client()
    
    # generate a response
    response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a motivational quote."},
        ]
    )
    
    return response.choices[0].message.content

@inngest_client.create_function(
    fn_id="agent-processor",
    trigger=inngest.TriggerEvent(event="agent/process")
)
def process_agent_request(ctx: inngest.Context) -> str:
    """
    Inngest function that processes AI agent requests asynchronously
    This is where the main agent logic lives
    """
    try:
        job_id = ctx.event.data["job_id"]
        prompt = ctx.event.data["prompt"]
        
        ctx.logger.info(f"Processing agent request for job {job_id}")
        
        analysis = analyze_user_prompt(prompt)
        
        if analysis["type"] == "research":
            result = research_agent_workflow(prompt)
        elif analysis["type"] == "reasoning":
            result = reasoning_agent_workflow(prompt)
        else:
            result = simple_qa_workflow(prompt)
        
        current_job = get_job_status(job_id)
        prompt_text = current_job.get("prompt") if current_job else None
        set_job_status(job_id, "completed", result, None, prompt=prompt_text)
        
        return f"Job {job_id} completed successfully"
        
    except Exception as e:
        ctx.logger.error(f"Error processing job {job_id}: {str(e)}")
        current_job = get_job_status(job_id)
        prompt_text = current_job.get("prompt") if current_job else None
        set_job_status(job_id, "failed", None, str(e), prompt=prompt_text)
        raise e

try:
    inngest.flask.serve(app, inngest_client, [process_agent_request])
    print("Inngest integration set up successfully")
except Exception as e:
    print(f"Error setting up Inngest integration: {e}")
    @app.route('/api/inngest', methods=['GET', 'POST', 'PUT'])
    def inngest_endpoint():
        return jsonify({"error": "Inngest integration failed", "details": str(e)}), 500

if __name__ == '__main__':
    if is_running_in_container():
        app.run(debug=True, host='0.0.0.0', port=8080)  # Use 8080 for non-root container
    else:
        app.run(debug=True, host='0.0.0.0', port=5050)
    print(f"App running on port {5050 if not is_running_in_container() else 8080}")
