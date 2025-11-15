"""Redis helper functions for job status storage"""
import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

job_results_fallback = {}
redis_client = None


def init_redis():
    """
    Initialize Redis client with connection pooling
    
    Returns:
        redis.Redis or None: Redis client instance or None if connection fails
    """
    global redis_client
    
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_username = os.getenv("REDIS_USERNAME", None)
    redis_password = os.getenv("REDIS_PASSWORD", None)
    redis_db = int(os.getenv("REDIS_DB", 0))
    
    try:
        client = redis.Redis(
            host=redis_host,
            port=redis_port,
            username=redis_username,
            password=redis_password,
            db=redis_db,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        client.ping()
        print(f"Redis connected successfully to {redis_host}:{redis_port}")
        redis_client = client
        return client
    except Exception as e:
        print(f"Redis connection error: {e}")
        print("Falling back to in-memory storage (not recommended for production)")
        redis_client = None
        return None


def get_redis_client():
    """Get the initialized Redis client"""
    global redis_client
    if redis_client is None:
        redis_client = init_redis()
    return redis_client


def get_job_status(job_id):
    """
    Get job status from Redis or fallback storage
    
    Args:
        job_id (str): The job ID to retrieve
        
    Returns:
        dict or None: Job status data or None if not found
    """
    client = get_redis_client()
    
    if client:
        try:
            data = client.get(f"job:{job_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return job_results_fallback.get(job_id)
    else:
        return job_results_fallback.get(job_id)


def set_job_status(job_id, status, result=None, error=None, prompt=None):
    """
    Set job status in Redis or fallback storage
    
    Args:
        job_id (str): The job ID
        status (str): Job status (e.g., "processing", "completed", "failed")
        result: Optional result data
        error: Optional error message
        prompt: Optional prompt text for the job
        
    Returns:
        bool: True if stored in Redis, False if using fallback
    """
    client = get_redis_client()
    
    job_data = {
        "status": status,
        "result": result,
        "error": error
    }
    
    if prompt is not None:
        job_data["prompt"] = prompt
    
    if client:
        try:
            client.setex(
                f"job:{job_id}",
                86400,
                json.dumps(job_data)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            job_results_fallback[job_id] = job_data
            return False
    else:
        job_results_fallback[job_id] = job_data
        return False


def get_job_count():
    """
    Get total number of jobs (approximate for Redis)
    
    Returns:
        int: Number of jobs stored
    """
    client = get_redis_client()
    
    if client:
        try:
            keys = client.keys("job:*")
            return len(keys)
        except Exception as e:
            print(f"Redis count error: {e}")
            return len(job_results_fallback)
    else:
        return len(job_results_fallback)


def get_all_jobs(limit=100):
    """
    Get all jobs from Redis or fallback storage
    
    Args:
        limit (int): Maximum number of jobs to return
        
    Returns:
        dict: Dictionary mapping job_id to job data
    """
    client = get_redis_client()
    all_jobs = {}
    
    if client:
        try:
            keys = client.keys("job:*")
            for key in keys[:limit]:
                try:
                    job_id = key.replace("job:", "")
                    data = client.get(key)
                    if data:
                        job_data = json.loads(data)
                        job_data["job_id"] = job_id
                        all_jobs[job_id] = job_data
                except Exception as e:
                    print(f"Error parsing job {key}: {e}")
                    continue
        except Exception as e:
            print(f"Redis get_all_jobs error: {e}")
            all_jobs = job_results_fallback.copy()
    else:
        all_jobs = job_results_fallback.copy()
    
    return all_jobs


def is_redis_connected():
    """
    Check if Redis is connected
    
    Returns:
        bool: True if Redis is connected, False otherwise
    """
    client = get_redis_client()
    return client is not None

