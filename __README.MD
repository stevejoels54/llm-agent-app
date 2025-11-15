# AI Agent Application - Complete Setup and Usage Guide

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Configuration](#configuration)
5. [Running Locally](#running-locally)
6. [API Documentation](#api-documentation)
7. [Agent Capabilities](#agent-capabilities)
8. [Deployment to Civo Cloud](#deployment-to-civo-cloud)
9. [Testing the Deployment](#testing-the-deployment)
10. [Troubleshooting](#troubleshooting)
11. [Architecture Overview](#architecture-overview)

---

## Overview

This application is an AI Agent platform that provides asynchronous LLM processing capabilities using Inngest AgentKit and Ollama. It features a web-based GUI for interacting with AI agents that can perform research, reasoning, and simple Q&A tasks.

### Key Features

- **Asynchronous Processing**: AI agents run in the background without blocking API responses
- **Multiple Agent Types**: 
  - Research Agent: Breaks down complex questions into sub-questions and synthesizes findings
  - Reasoning Agent: Provides step-by-step explanations for complex topics
  - Simple Q&A: Direct question-answering for straightforward queries
- **Web GUI**: Modern, responsive interface for interacting with agents
- **Job Status Tracking**: Real-time status updates via Redis-backed storage
- **Auto-Detection**: Automatically selects the best agent type based on your prompt

### Technology Stack

- **Backend**: Flask (Python)
- **Workflow Engine**: Inngest AgentKit
- **LLM**: Ollama (via OpenAI-compatible API)
- **Storage**: Redis (for job status)
- **Frontend**: Vanilla JavaScript + HTML/CSS
- **Deployment**: Kubernetes (Civo Cloud), Helm, Terraform

---

## Prerequisites

Before you begin, ensure you have the following installed and configured:

### Required Software

- **Python 3.8+** - [Installation Guide](https://www.python.org/downloads/)
- **Docker** - [Installation Guide](https://www.docker.com/get-started)
- **Ollama** - [Installation Guide](https://ollama.ai/download)
- **Node.js & npm** (for Inngest CLI) - [Installation Guide](https://nodejs.org/)
- **Redis** (optional for local dev, required for production)

### Required Accounts & Keys

- **Inngest Account**: Sign up at [https://www.inngest.com](https://www.inngest.com)
  - You'll need: Signing Key and Event Key from Inngest Dashboard
- **Civo Cloud Account** (for deployment): Sign up at [https://dashboard.civo.com/signup](https://dashboard.civo.com/signup)
  - You'll need: Civo API Key from [Security Settings](https://dashboard.civo.com/security)
- **Container Registry Account** (for deployment): Docker Hub, GitHub Container Registry, or Civo Container Registry

### Optional (for deployment)

- **Terraform** - [Installation Guide](https://developer.hashicorp.com/terraform/install)
- **kubectl** - [Installation Guide](https://kubernetes.io/docs/tasks/tools/)
- **Helm** - [Installation Guide](https://helm.sh/docs/intro/install/)

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd _llmBoilerGrow2025
```

### Step 2: Install Ollama and Pull Model

```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai/download for installation instructions

# Start Ollama service
ollama serve

# In another terminal, pull the required model
ollama pull llama3.2
```

### Step 3: Set Up Python Environment

```bash
cd app/

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Minimum `.env` configuration for local development:**

```env
# Inngest Configuration (Development Mode)
INNGEST_ENV=dev
INNGEST_APP_ID=llm-agent-app

# For production, you'll also need:
# INNGEST_SIGNING_KEY=your_signing_key_here
# INNGEST_EVENT_KEY=your_event_key_here

# Redis Configuration (Optional for local dev - will use in-memory fallback if not set)
# REDIS_HOST=localhost
# REDIS_PORT=6379
# REDIS_USERNAME=default
# REDIS_PASSWORD=
# REDIS_DB=0
```

**Note**: For local development, Inngest keys can be empty. The app will work in development mode without them, but background processing will only work when connected to Inngest.

---

## Configuration

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `INNGEST_ENV` | Environment mode (`dev` or `prod`) | Yes | `dev` |
| `INNGEST_APP_ID` | Inngest application ID | Yes | `llm-agent-app` |
| `INNGEST_SIGNING_KEY` | Inngest signing key (for production) | No* | - |
| `INNGEST_EVENT_KEY` | Inngest event key (for production) | No* | - |
| `REDIS_HOST` | Redis hostname | No | `localhost` |
| `REDIS_PORT` | Redis port | No | `6379` |
| `REDIS_USERNAME` | Redis username | No | `default` |
| `REDIS_PASSWORD` | Redis password | No | - |
| `REDIS_DB` | Redis database number | No | `0` |

\* Required for production deployment. Optional for local development.

### Getting Inngest Credentials

1. **Sign up** at [https://www.inngest.com](https://www.inngest.com)
2. **Create an app** in the Inngest Dashboard
3. **Navigate to**: Settings → API Keys
4. **Copy** the following:
   - **Signing Key**: Used to verify requests from Inngest
   - **Event Key**: Used to send events to Inngest
5. **Add to `.env`** file for production use

---

## Running Locally

### Option 1: Using the Setup Script (Recommended)

```bash
cd app/
chmod +x setup_and_run.sh
./setup_and_run.sh
```

This script will:
- Check for required dependencies
- Start the Flask application on port 5050

### Option 2: Manual Start

#### Terminal 1: Start Inngest Dev Server

```bash
# Install Inngest CLI globally (if not already installed)
npm install -g inngest-cli@latest

# Start Inngest dev server
npx inngest-cli@latest dev -u http://127.0.0.1:5050/api/inngest --no-discovery
```

#### Terminal 2: Start Flask Application

```bash
cd app/
source venv/bin/activate  # If using virtual environment
python main.py
```

The application will start on **http://localhost:5050**

### Accessing the Application

- **Web GUI**: Open [http://localhost:5050](http://localhost:5050) in your browser
- **API Endpoint**: [http://localhost:5050/api/chat](http://localhost:5050/api/chat)

---

## API Documentation

### Endpoints

#### 1. POST `/api/chat`

Submit a prompt to an AI agent for processing.

**Request:**
```json
{
  "prompt": "Research the benefits of microservices architecture",
  "session_id": "optional-session-id"
}
```

**Response (202 Accepted):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Agent processing started"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5050/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is Kubernetes?",
    "session_id": "my-session-123"
  }'
```

#### 2. GET `/api/status/<job_id>`

Get the status and result of a specific job.

**Request:**
```bash
GET /api/status/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "status": "completed",
  "result": {
    "type": "simple_answer",
    "question": "What is Kubernetes?",
    "answer": "Kubernetes is an open-source container orchestration platform...",
    "agent_steps": ["direct_response"]
  },
  "prompt": "What is Kubernetes?",
  "error": null
}
```

**Status Values:**
- `processing`: Agent is currently processing the request
- `completed`: Agent has finished and returned results
- `failed`: An error occurred during processing

**cURL Example:**
```bash
curl http://localhost:5050/api/status/550e8400-e29b-41d4-a716-446655440000
```

#### 3. GET `/api/jobs`

Get all jobs from Redis storage.

**Query Parameters:**
- `limit` (optional): Maximum number of jobs to return (default: 100)

**Request:**
```bash
GET /api/jobs?limit=50
```

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "result": {...},
      "prompt": "What is Kubernetes?",
      "error": null
    },
    ...
  ]
}
```

**cURL Example:**
```bash
curl http://localhost:5050/api/jobs?limit=10
```

---

## Agent Capabilities

### Research Agent

The Research Agent automatically activates when your prompt contains keywords like "research", "analyze", "investigate", "study", or "compare".

**How it works:**
1. Breaks down the complex question into 3-5 sub-questions
2. Researches each sub-question independently
3. Synthesizes all findings into a comprehensive answer

**Example Prompts:**
- "Research the benefits and drawbacks of microservices architecture"
- "Analyze the impact of AI on modern software development"
- "Compare Docker and Kubernetes containerization strategies"

**Example Response Structure:**
```json
{
  "type": "research_report",
  "original_question": "Research the benefits of microservices",
  "sub_questions": [
    {
      "question": "1. What are the key benefits of microservices?",
      "answer": "Microservices provide several benefits..."
    },
    ...
  ],
  "synthesis": "Based on the research findings, microservices architecture...",
  "agent_steps": ["question_breakdown", "sub_question_research", "synthesis"]
}
```

### Reasoning Agent

The Reasoning Agent activates for prompts requiring step-by-step explanations, indicated by words like "explain", "how", "why", "steps", or "process".

**How it works:**
1. Creates a step-by-step plan to address the question
2. Executes each step with detailed explanations
3. Provides a final comprehensive explanation

**Example Prompts:**
- "Explain how transformers work in machine learning"
- "How does Kubernetes schedule pods?"
- "Why is Redis fast? Explain the steps involved"

**Example Response Structure:**
```json
{
  "type": "reasoning_explanation",
  "original_question": "Explain how transformers work",
  "reasoning_plan": "1. Understand the problem...\n2. Break it down...",
  "reasoning_steps": [
    {
      "step": "1. Understand the transformer architecture",
      "explanation": "Transformers use attention mechanisms..."
    },
    ...
  ],
  "final_explanation": "In summary, transformers work by...",
  "agent_steps": ["planning", "step_execution", "synthesis"]
}
```

### Simple Q&A Agent

For straightforward questions that don't require multi-step reasoning or research.

**Example Prompts:**
- "What is Python?"
- "How do I install Docker?"
- "Tell me a joke"

**Example Response Structure:**
```json
{
  "type": "simple_answer",
  "question": "What is Python?",
  "answer": "Python is a high-level programming language...",
  "agent_steps": ["direct_response"]
}
```

### Auto-Detect Mode (Default)

The application automatically analyzes your prompt and selects the most appropriate agent type. You can also manually select an agent type using the badges in the web GUI.

---

## Deployment to Civo Cloud

This section covers deploying the application to Civo Cloud using Kubernetes, Helm, and Terraform.

### Prerequisites for Deployment

- Civo Cloud account with API key
- Terraform installed
- kubectl installed
- Container registry account (Docker Hub, GitHub Container Registry, or Civo Container Registry)
- Inngest production credentials (Signing Key and Event Key)

### Step 1: Build and Push Docker Image

#### Option A: Docker Hub

```bash
cd app/

# Login to Docker Hub
docker login

# Build the image
docker build -t YOUR_DOCKERHUB_USERNAME/llm-agent-app:latest .

# Push to registry
docker push YOUR_DOCKERHUB_USERNAME/llm-agent-app:latest
```

#### Option B: GitHub Container Registry

```bash
cd app/

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Build and tag
docker build -t ghcr.io/YOUR_GITHUB_USERNAME/llm-agent-app:latest .

# Push
docker push ghcr.io/YOUR_GITHUB_USERNAME/llm-agent-app:latest
```

#### Option C: Civo Container Registry

```bash
# Login to Civo registry
civo kubernetes registry-login

# Build and tag
docker build -t civo/YOUR_REGISTRY_NAME/llm-agent-app:latest .

# Push
docker push civo/YOUR_REGISTRY_NAME/llm-agent-app:latest
```

### Step 2: Configure Terraform

```bash
cd infra/tf/

# Create terraform.tfvars if it doesn't exist
cat > terraform.tfvars << EOF
civo_token = "YOUR_CIVO_API_KEY"
cluster_name = "llm-cluster"
region = "LON1"
deploy_app = true
deploy_ollama = true
deploy_ollama_ui = true
deploy_nv_device_plugin_ds = true
EOF
```

**Replace `YOUR_CIVO_API_KEY`** with your actual Civo API key from [Security Settings](https://dashboard.civo.com/security).

### Step 3: Update Helm Chart Values

Edit `infra/helm/app/values.yaml`:

```yaml
replicaCount: 1

image:
  repository: YOUR_REGISTRY/llm-agent-app  # Update with your image path
  pullPolicy: Always
  tag: "latest"

service:
  type: LoadBalancer
  port: 80

env:
  inngestEnv: "prod"
  
secrets:
  inngestSecretName: "inngest-secrets"
  redisSecretName: "redis-secrets"
```

**Important:** Replace `YOUR_REGISTRY/llm-agent-app` with your actual Docker image path.

### Step 4: Deploy Infrastructure

```bash
cd infra/tf/

# Initialize Terraform
terraform init

# Review deployment plan
terraform plan

# Apply deployment
terraform apply
```

This will create:
- Civo Kubernetes cluster with GPU nodes
- Ollama LLM server deployment
- Ollama Web UI
- Nvidia GPU Device Plugin
- Your application (if `deploy_app = true`)

**Wait 5-10 minutes** for the deployment to complete.

### Step 5: Configure Kubernetes Access

```bash
# Get kubeconfig from Terraform output
cd infra/tf/
terraform output -raw kubeconfig > kubeconfig.yaml

# Set KUBECONFIG environment variable
export KUBECONFIG=$(pwd)/kubeconfig.yaml

# Or use Civo CLI
civo kubernetes config llm-cluster --save

# Verify access
kubectl get nodes
```

### Step 6: Create Kubernetes Secrets

#### Create Inngest Secret

```bash
kubectl create secret generic inngest-secrets \
  --from-literal=signing-key='YOUR_INNGEST_SIGNING_KEY' \
  --from-literal=event-key='YOUR_INNGEST_EVENT_KEY' \
  --namespace=default
```

**Replace:**
- `YOUR_INNGEST_SIGNING_KEY` with your actual Inngest signing key
- `YOUR_INNGEST_EVENT_KEY` with your actual Inngest event key

#### Create Redis Secret

```bash
kubectl create secret generic redis-secrets \
  --from-literal=redis-host='YOUR_REDIS_HOST' \
  --from-literal=redis-port='6379' \
  --from-literal=redis-username='default' \
  --from-literal=redis-password='YOUR_REDIS_PASSWORD' \
  --from-literal=redis-db='0' \
  --namespace=default
```

**Redis Options:**

1. **Deploy Redis in the cluster:**
   ```bash
   helm install redis bitnami/redis --set auth.enabled=false
   # Then use: redis-host=redis-master.redis.svc.cluster.local
   ```

2. **Use external Redis service:** Provide your Redis hostname/IP and password

3. **Managed Redis service:** Use your provider's Redis connection details

### Step 7: Verify Deployment

```bash
# Check if pods are running
kubectl get pods

# Check deployment status
kubectl get deployment

# View application logs
kubectl logs -f deployment/llm-agent-app

# Get service URL
kubectl get svc llm-agent-app
```

### Step 8: Get Application URL

```bash
# Get LoadBalancer external IP
kubectl get svc llm-agent-app

# Look for EXTERNAL-IP column
# Or use port-forward for testing
kubectl port-forward svc/llm-agent-app 8080:80
```

Access your application at:
- **LoadBalancer URL**: `http://EXTERNAL-IP`
- **Port-forward**: `http://localhost:8080`

---

## Testing the Deployment

### 1. Test Web GUI

1. Open the LoadBalancer URL in your browser
2. You should see the AI Agent Interface
3. Try sending a prompt: "What is Kubernetes?"

### 2. Test API Endpoint

```bash
# Replace EXTERNAL_IP with your LoadBalancer IP
curl -X POST http://EXTERNAL_IP/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain how Docker containers work"}'

# You should receive a job_id and status: "processing"
# Poll for results:
curl http://EXTERNAL_IP/api/status/JOB_ID_HERE
```

### 3. Verify Inngest Integration

```bash
# Check application logs
kubectl logs deployment/llm-agent-app | grep -i inngest

# Check Inngest dashboard for function executions
# Visit: https://app.inngest.com
```

### 4. Verify Ollama Connection

```bash
# Test connectivity from app pod to Ollama
kubectl exec -it deployment/llm-agent-app -- \
  curl http://ollama.ollama.svc.cluster.local:11434/api/tags

# Should return list of available models
```

### 5. Test Different Agent Types

**Research Agent:**
```bash
curl -X POST http://EXTERNAL_IP/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Research the benefits of microservices"}'
```

**Reasoning Agent:**
```bash
curl -X POST http://EXTERNAL_IP/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain step by step how Kubernetes schedules pods"}'
```

**Simple Q&A:**
```bash
curl -X POST http://EXTERNAL_IP/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?"}'
```

---

## Troubleshooting

### Application Issues

#### Issue: Application Won't Start Locally

**Symptoms:** Flask app fails to start or crashes immediately

**Solutions:**
1. Check if Ollama is running:
   ```bash
   ollama serve
   ```

2. Verify Ollama model is installed:
   ```bash
   ollama list
   # If llama3.2 is not listed:
   ollama pull llama3.2
   ```

3. Check Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify port 5050 is available:
   ```bash
   lsof -i :5050  # macOS/Linux
   # Kill process if needed
   ```

#### Issue: Inngest Not Connecting

**Symptoms:** Jobs stay in "processing" status indefinitely, or errors about Inngest connection

**Solutions:**
1. **For local development:**
   - Ensure Inngest dev server is running:
     ```bash
     npx inngest-cli@latest dev -u http://127.0.0.1:5050/api/inngest --no-discovery
     ```
   - Check that Inngest dev server shows your function registered

2. **For production:**
   - Verify Inngest secrets are created:
     ```bash
     kubectl get secret inngest-secrets
     ```
   - Check environment variables in pod:
     ```bash
     kubectl exec deployment/llm-agent-app -- env | grep INNGEST
     ```
   - Verify Inngest credentials in Inngest Dashboard

3. Check application logs for Inngest errors:
   ```bash
   kubectl logs deployment/llm-agent-app | grep -i inngest
   ```

#### Issue: Redis Connection Failed

**Symptoms:** Jobs work but disappear on restart, or "Redis connection error" in logs

**Solutions:**
1. **Local development:**
   - Start Redis:
     ```bash
     docker run -d --name redis-dev -p 6379:6379 redis:latest
     ```
   - Or verify local Redis is running:
     ```bash
     redis-cli ping  # Should return "PONG"
     ```

2. **Production:**
   - Verify Redis secret exists:
     ```bash
     kubectl get secret redis-secrets
     ```
   - Test connectivity from pod:
     ```bash
     kubectl exec deployment/llm-agent-app -- \
       nc -zv YOUR_REDIS_HOST 6379
     ```
   - Check Redis pod/service (if in cluster):
     ```bash
     kubectl get pods -n redis
     kubectl get svc -n redis
     ```

**Note:** The application will fall back to in-memory storage if Redis is unavailable, but jobs will be lost on pod restart.

### Deployment Issues

#### Issue: Pods Not Starting

**Symptoms:** Pods in `Pending` or `CrashLoopBackOff` state

**Solutions:**
```bash
# Check pod status and events
kubectl describe pod <pod-name>

# Common issues:
# 1. Image pull errors
kubectl describe pod <pod-name> | grep -i image
# Solution: Verify image path in values.yaml and ensure registry is accessible

# 2. Secret not found
kubectl describe pod <pod-name> | grep -i secret
# Solution: Create required secrets (inngest-secrets, redis-secrets)

# 3. Resource limits
kubectl describe pod <pod-name> | grep -i resources
# Solution: Check node capacity or adjust resource requests
```

#### Issue: Cannot Connect to Ollama

**Symptoms:** Jobs fail with "connection refused" to Ollama

**Solutions:**
```bash
# Verify Ollama is deployed
kubectl get pods -n ollama

# Check Ollama service
kubectl get svc -n ollama

# Test connectivity from app pod
kubectl exec -it deployment/llm-agent-app -- \
  curl http://ollama.ollama.svc.cluster.local:11434/api/tags

# If Ollama is not deployed, deploy it:
cd infra/tf/
# Ensure deploy_ollama = true in terraform.tfvars
terraform apply
```

#### Issue: LoadBalancer Not Getting External IP

**Symptoms:** `EXTERNAL-IP` shows as `<pending>`

**Solutions:**
1. Wait a few minutes (LoadBalancer provisioning can take 2-5 minutes)
2. Check service events:
   ```bash
   kubectl describe svc llm-agent-app
   ```
3. Verify cluster has LoadBalancer support (Civo clusters support this by default)

#### Issue: Image Pull Errors

**Symptoms:** `ErrImagePull` or `ImagePullBackOff` errors

**Solutions:**
```bash
# Verify image exists in registry
docker pull YOUR_REGISTRY/llm-agent-app:latest

# Check image pull secrets if using private registry
kubectl get secrets

# Create image pull secret if needed
kubectl create secret docker-registry regcred \
  --docker-server=YOUR_REGISTRY \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_PASSWORD \
  --namespace=default

# Update deployment to use the secret (edit deployment.yaml or use Helm)
```

### Performance Issues

#### Issue: Jobs Taking Too Long

**Possible causes:**
1. **Ollama model not loaded:** First request may take longer
2. **GPU resources:** Verify GPU nodes are available and Ollama is using them
3. **Complex prompts:** Research/Reasoning agents make multiple LLM calls

**Solutions:**
```bash
# Check Ollama GPU usage
kubectl exec -it deployment/ollama -- nvidia-smi

# Verify model is loaded in Ollama
kubectl exec -it deployment/ollama -- \
  curl http://localhost:11434/api/tags
```

#### Issue: High Memory Usage

**Possible causes:**
1. Multiple concurrent jobs
2. Large LLM responses
3. Redis storing too many jobs

**Solutions:**
1. Adjust job retention in Redis (currently 86400 seconds = 24 hours)
2. Limit concurrent requests
3. Scale resources:
   ```bash
   kubectl scale deployment llm-agent-app --replicas=2
   ```

---

## Architecture Overview

### System Components

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────────────────┐
│      Flask Application              │
│  ┌───────────────────────────────┐  │
│  │  /api/chat (POST)             │  │
│  │  /api/status/<id> (GET)       │  │
│  │  /api/jobs (GET)              │  │
│  └───────────────────────────────┘  │
│            │                         │
│            │ Inngest Event           │
│            ▼                         │
│  ┌───────────────────────────────┐  │
│  │  Inngest AgentKit             │  │
│  │  - process_agent_request()    │  │
│  └───────────────────────────────┘  │
└────┬──────────────┬──────────────────┘
     │              │
     │ Redis        │ Ollama API
     ▼              ▼
┌─────────┐   ┌──────────────┐
│  Redis  │   │    Ollama    │
│ (Jobs)  │   │  (LLM Server)│
└─────────┘   └──────────────┘
```

### Request Flow

1. **User submits prompt** via Web GUI or API
2. **Flask API** receives POST to `/api/chat`
3. **Job created** in Redis with status "processing"
4. **Inngest event sent** to trigger background processing
5. **API returns immediately** with job_id and status
6. **Frontend polls** `/api/status/<job_id>` for updates
7. **Inngest function** executes asynchronously:
   - Analyzes prompt to select agent type
   - Executes agent workflow (Research/Reasoning/Simple)
   - Makes LLM calls to Ollama
   - Stores result in Redis
8. **Frontend receives** updated status and displays result

### Agent Workflows

**Research Agent Flow:**
```
Prompt → Analyze → Break into sub-questions → 
Research each → Synthesize → Store result
```

**Reasoning Agent Flow:**
```
Prompt → Analyze → Create plan → 
Execute each step → Final explanation → Store result
```

**Simple Q&A Flow:**
```
Prompt → Analyze → Direct LLM call → Store result
```

### Data Flow

- **Redis**: Stores job status, results, and prompts (key: `job:<job_id>`, TTL: 24 hours)
- **Inngest**: Manages background workflow execution and retries
- **Ollama**: Provides LLM inference capabilities via OpenAI-compatible API

---

## Additional Resources

- [Inngest AgentKit Documentation](https://docs.inngest.com/agentkit/)
- [Inngest AgentKit Overview](https://agentkit.inngest.com/overview)
- [Inngest Python SDK](https://www.inngest.com/docs/reference/python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Civo Kubernetes Documentation](https://www.civo.com/docs/kubernetes)
- [Terraform Civo Provider](https://registry.terraform.io/providers/civo/civo/latest/docs)

---

## Support and Contributing

For issues, questions, or contributions:
1. Check the Troubleshooting section above
2. Review application logs: `kubectl logs deployment/llm-agent-app`
3. Check Inngest dashboard for function execution status
4. Verify all prerequisites and configuration are correct

---

## Summary Checklist

Use this checklist when setting up the application:

**Local Development:**
- [ ] Python 3.8+ installed
- [ ] Ollama installed and running
- [ ] llama3.2 model pulled
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured
- [ ] Redis started (optional)
- [ ] Inngest dev server running (for local testing)
- [ ] Flask app starts successfully
- [ ] Web GUI accessible at http://localhost:5050

**Production Deployment:**
- [ ] Docker image built and pushed to registry
- [ ] Helm values.yaml updated with image path
- [ ] Terraform configured with Civo API key
- [ ] `deploy_app = true` in terraform.tfvars
- [ ] Infrastructure deployed with Terraform
- [ ] Kubernetes access configured
- [ ] Inngest secrets created in Kubernetes
- [ ] Redis secrets created in Kubernetes (or Redis deployed)
- [ ] Application pods running
- [ ] Application accessible via LoadBalancer
- [ ] End-to-end testing successful

---

**Version:** 1.0.0