
# Project Name: Civo LLM Boilerplate

## Introduction

This project provides a boilerplate for deploying a K8s GPU Cluster on Civo Cloud using Terraform. It automates the setup of various applications and tools, including:

- [Ollama LLM Inference Server](https://github.com/ollama/ollama)
- [Ollama Web UI](https://github.com/open-webui/open-webui)
- [Nvidia Device Plugin](https://github.com/NVIDIA/k8s-device-plugin)
- An example Python LLM application

## Project Goal

The goal of this project is to enable customers to easily use Open Source Large Language Models (LLMs), providing 1:1 compatibility with OpenAI's ChatGPT.

- Access to the latest Open Source LLMs made avaliable from Ollama
- Provide a user interface to allow non-technical users access to models
- Provide a path to produce insights with LLMs whilst maintaining soverignty over the data
- enable LLMs in regulatory usecases where ChatGPT can't be used.


## ASSIGNMENT OBJECTIVES

This section outlines the key tasks and deliverables required to complete this assignment. Your objective is to extend the existing Flask application with asynchronous AI agent capabilities using Inngest AgentKit, and deploy the solution to Civo Cloud.

### 1. Create LLM API Endpoint

**Objective:** Extend the Flask application (`app/main.py`) to include a new API endpoint that serves as the entry point for LLM interactions from the frontend.

**Requirements:**
- Create a RESTful API endpoint (e.g., `/api/chat` or `/api/agent`) that accepts user queries/prompts
- The endpoint should accept POST requests with JSON payloads containing user input
- Implement proper request validation and error handling
- This endpoint will serve as the bridge between the frontend interface and the Inngest AgentKit background processing

**What is an AI Agent?**

An AI agent is an autonomous system that goes beyond simple LLM question-answering. It combines:
- **Tool Usage:** Can call external functions, APIs, or services to accomplish tasks (e.g., searching databases, making calculations, fetching data via api or mcp)
- **State & Memory:** Maintains context across interactions and remembers previous steps in a workflow
- **Autonomy:** Operates independently in the background, making decisions without requiring human intervention for each step

Unlike a simple chatbot that only responds to prompts (as defined in the @main.py file), an AI agent actively plans, executes, and adapts its approach to achieve a goal. With Inngest AgentKit, these agents run asynchronously as background workflows.

### 2. Integrate Inngest AgentKit

**Objective:** Implement Inngest AgentKit to handle LLM agent operations asynchronously in the background.

**Requirements:**
- Review the [Inngest AgentKit documentation](https://docs.inngest.com/agentkit/ and https://agentkit.inngest.com/overview) to understand the framework
- Configure Inngest in your Flask application to enable background agent execution
- Create an Inngest function that is triggered by your API endpoint
- The Inngest function should orchestrate the AI agent workflow and handle the LLM processing
- Ensure the agent runs completely in the background without blocking the API response

**Key Concepts:**
- **Asynchronous Processing:** The API should immediately return a job/request ID to the frontend
- **Background Execution:** Inngest agents run separately from the API request-response cycle
- **Response Handling:** Implement a mechanism (webhooks, polling endpoint, or WebSocket) to deliver agent responses back to the frontend GUI when available

### 3. Build a Custom AI Agent

**Objective:** Design and implement an AI agent that demonstrates meaningful functionality beyond simple Q&A.

**Requirements:**
- Choose an agent type that showcases practical use cases (examples: research agent, code analysis agent, multi-step reasoning agent, etc.)
- The agent should leverage the Ollama LLM infrastructure already deployed in the cluster
- Implement proper agent state management and conversation context handling
- Ensure the agent can handle multi-turn interactions if applicable
- Add appropriate logging and monitoring for agent execution

**Deliverables:**
- A working agent that executes in the background via Inngest
- Clear documentation of what the agent does and how it works
- Response delivery mechanism that updates the frontend GUI when results are ready

### 4. Deploy to Civo Cloud

**Objective:** Deploy your enhanced application to the Civo Kubernetes cluster using the existing deployment pipeline.

**Requirements:**
- Build a Docker image containing your updated Flask application with Inngest integration
- Push the image to a container registry (Docker Hub, Civo Container Registry, etc.)
- Update the Helm chart configuration in `infra/helm/app` to reference your new image
- Configure necessary environment variables for Inngest (API keys, endpoints, etc.)
- Deploy the application to the Civo GPU cluster using Terraform
- Verify that the application can communicate with the Ollama inference server in the cluster
- Test the end-to-end flow: Frontend → API → Inngest Agent → LLM → Response to Frontend

**Configuration Notes:**
- Follow the deployment instructions in the "Building and deploying the Example Application" section
- Ensure all secrets and API keys are properly managed (use Kubernetes secrets, not hardcoded values)
- Update the `deploy_app` variable in `tf/variables.tf` to `true` to enable application deployment

### 5. Update Documentation

**Objective:** Create comprehensive documentation in `__README.MD` for running and testing the application.

**Requirements:**
- Document the complete setup process in simple, clear terms
- Include instructions for local development and testing
- Explain how to configure Inngest (API keys, environment variables)
- Provide step-by-step deployment instructions
- Include example API requests and expected responses
- Add troubleshooting tips for common issues
- Document the agent's capabilities and usage examples

**Target Audience:** The documentation should be accessible to developers with basic Python and Docker knowledge.

### Success Criteria

Your assignment will be considered complete when:
- The Flask API successfully triggers Inngest agent execution
- Agents run asynchronously in the background without blocking the API
- Agent responses are delivered back to the frontend GUI
- The application is successfully deployed and running on Civo Cloud
- The `__README.MD` contains clear, tested instructions for setup and usage
- All components (Frontend, API, Inngest, Ollama LLM) work together end-to-end

### Additional Resources

- [Inngest AgentKit Documentation](https://docs.inngest.com/agentkit/ and https://agentkit.inngest.com/overview)
- [Inngest Python SDK](https://www.inngest.com/docs/reference/python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Civo Kubernetes Documentation](https://www.civo.com/docs/kubernetes)


## Project Deployment Prerequisites

Before beginning, ensure you have the following:

- A [Civo Cloud account](https://dashboard.civo.com/signup).
- A [Civo Cloud API Key](https://dashboard.civo.com/security).
- [Terraform](https://developer.hashicorp.com/terraform/install) installed on your local machine.

## Project Setup

1. Obtain your Civo API key from the Civo Cloud dashboard.
2. Create a file named `terraform.tfvars` in the project's root directory.
3. Insert your Civo API key into this file as follows:

    ```hcl
    civo_token = "YOUR_API_KEY"
    ```

## Project Configuration

Project configurations are managed within the `tf/variables.tf` file. This file contains definitions and default values for the Terraform variables used in the project.

| Variable             | Description                                       | Type   | Default Value      |
|----------------------|---------------------------------------------------|--------|--------------------|
| `cluster_name`       | The name of the cluster.                          | string | "llm_cluster"     |
| `cluster_node_size`  | The GPU node instance to use for the cluster.     | string | "g4s.kube.small" |
| `cluster_node_count` | The number of nodes to provision in the cluster.  | number | 1                  |
| `civo_token`         | The Civo API token, set in terraform.tfvars.      | string | N/A                |
| `region`             | The Civo Region to deploy the cluster in.         | string | "LON1"             |

## Deployment Configuration

Deployment of components is controlled through boolean variables within the `tf/variables.tf` file. Set these variables to `true` to enable the deployment of the corresponding component.

| Variable                      | Description                                             | Type  | Default Value |
|-------------------------------|---------------------------------------------------------|-------|---------------|
| `deploy_ollama`               | Deploy the Ollama inference server.                     | bool  | true         |
| `deploy_ollama_ui`            | Deploy the Ollama Web UI.                               | bool  | true         |
| `deploy_app`                  | Deploy the example application.                         | bool  | false         |
| `deploy_nv_device_plugin_ds`  | Deploy the Nvidia GPU Device Plugin for enabling GPU support. | bool  | true         |

## Deploy LLM Boiler Plate

To deploy, simply run the following commands:

1. **Initialize Terraform:**

    ```
    terraform init
    ```

    This command initializes Terraform, installs the required providers, and prepares the environment for deployment.

2. **Plan Deployment:**

    ```
    terraform plan
    ```

    This command displays the deployment plan, showing what resources will be created or modified.

3. **Apply Deployment:**

    ```
    terraform apply
    ```

    This command applies the deployment plan. Terraform will prompt for confirmation before proceeding with the creation of resources.


## Building and deploying the Example Application
1. **Build the custom application container**
    Enter the application folder:
    ```
    cd app
    ```
    Build the docker image:
    ```
    docker build -t {repo}/{image} .
    ```
    Push the docker image to a registry:
    ```
    docker push -t {repo}/{image}
    ```
    Navigate to the helm chart:
    ```
    cd ../infra/helm/app
    ```
    Modify the Helm Values to point to your docker registry, e.g
    ```yaml
    replicaCount: 1
    image:
        repository: {repo}/{image}
        pullPolicy: Always
        tag: "latest"

    service:
        type: ClusterIP
        port: 80
    ```
2. **Initialize Terraform:**

    Navigate to the terraform directory
    ```
    cd ../tf
    ```

    ```
    terraform init
    ```

    This command initializes Terraform, installs the required providers, and prepares the environment for deployment.

3. **Plan Deployment:**

    ```
    terraform plan
    ```

    This command displays the deployment plan, showing what resources will be created or modified.

4. **Apply Deployment:**

    ```
    terraform apply
    ```

    This command applies the deployment plan. Terraform will prompt for confirmation before proceeding with the creation of resources.