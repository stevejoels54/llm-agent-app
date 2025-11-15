"""AI agent workflow functions"""
import json
from .ollama_helper import get_ollama_client


def analyze_user_prompt(prompt):
    """
    Analyze the user prompt to determine the best agent strategy
    
    Args:
        prompt (str): User's input prompt
        
    Returns:
        dict: Analysis result with type and complexity
    """
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["research", "analyze", "investigate", "study", "compare"]):
        return {"type": "research", "complexity": "high"}
    elif any(word in prompt_lower for word in ["explain", "how", "why", "steps", "process"]):
        return {"type": "reasoning", "complexity": "medium"}
    else:
        return {"type": "simple", "complexity": "low"}


def research_agent_workflow(prompt):
    """
    Multi-step research agent that breaks down complex queries
    
    Args:
        prompt (str): Research question or prompt
        
    Returns:
        dict: Research report with sub-questions and synthesis
    """
    client = get_ollama_client()
    
    breakdown_prompt = f"""
    Break down this research question into 3-5 specific sub-questions that need to be answered:
    
    Question: {prompt}
    
    Return a numbered list of sub-questions:
    """
    
    breakdown_response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are a research assistant that breaks down complex questions."},
            {"role": "user", "content": breakdown_prompt}
        ]
    )
    
    sub_questions = breakdown_response.choices[0].message.content
    
    research_results = []
    for i, line in enumerate(sub_questions.split('\n')):
        if line.strip() and any(char.isdigit() for char in line[:3]):
            sub_question = line.strip()
            
            research_response = client.chat.completions.create(
                model="llama3.2:latest",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable research assistant. Provide detailed, accurate information."},
                    {"role": "user", "content": sub_question}
                ]
            )
            
            research_results.append({
                "question": sub_question,
                "answer": research_response.choices[0].message.content
            })
    
    synthesis_prompt = f"""
    Based on the following research, provide a comprehensive answer to the original question: "{prompt}"
    
    Research findings:
    {json.dumps(research_results, indent=2)}
    
    Provide a well-structured, comprehensive response that synthesizes all the research:
    """
    
    final_response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are an expert analyst who synthesizes research into clear, comprehensive reports."},
            {"role": "user", "content": synthesis_prompt}
        ]
    )
    
    return {
        "type": "research_report",
        "original_question": prompt,
        "sub_questions": research_results,
        "synthesis": final_response.choices[0].message.content,
        "agent_steps": ["question_breakdown", "sub_question_research", "synthesis"]
    }


def reasoning_agent_workflow(prompt):
    """
    Multi-step reasoning agent for complex explanations
    
    Args:
        prompt (str): Question or prompt requiring reasoning
        
    Returns:
        dict: Reasoning explanation with steps and final answer
    """
    client = get_ollama_client()
    
    planning_prompt = f"""
    Create a step-by-step plan to thoroughly explain or solve: "{prompt}"
    
    Return a numbered plan with 3-5 logical steps:
    """
    
    plan_response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are a logical reasoning assistant that creates clear step-by-step plans."},
            {"role": "user", "content": planning_prompt}
        ]
    )
    
    plan = plan_response.choices[0].message.content
    
    reasoning_steps = []
    for i, line in enumerate(plan.split('\n')):
        if line.strip() and any(char.isdigit() for char in line[:3]):
            step_description = line.strip()
            
            step_prompt = f"""
            Execute this reasoning step: {step_description}
            
            Context: We are working on "{prompt}"
            
            Provide a detailed explanation for this step:
            """
            
            step_response = client.chat.completions.create(
                model="llama3.2:latest",
                messages=[
                    {"role": "system", "content": "You are a detailed reasoning assistant. Explain each step thoroughly."},
                    {"role": "user", "content": step_prompt}
                ]
            )
            
            reasoning_steps.append({
                "step": step_description,
                "explanation": step_response.choices[0].message.content
            })
    
    final_prompt = f"""
    Provide a final comprehensive explanation for: "{prompt}"
    
    Based on this step-by-step reasoning:
    {json.dumps(reasoning_steps, indent=2)}
    
    Create a clear, complete explanation:
    """
    
    final_response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are an expert teacher who creates clear, comprehensive explanations."},
            {"role": "user", "content": final_prompt}
        ]
    )
    
    return {
        "type": "reasoning_explanation",
        "original_question": prompt,
        "reasoning_plan": plan,
        "reasoning_steps": reasoning_steps,
        "final_explanation": final_response.choices[0].message.content,
        "agent_steps": ["planning", "step_execution", "synthesis"]
    }


def simple_qa_workflow(prompt):
    """
    Simple Q&A workflow for straightforward questions
    
    Args:
        prompt (str): Simple question or prompt
        
    Returns:
        dict: Simple answer with question and response
    """
    client = get_ollama_client()
    
    response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide clear, accurate answers."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return {
        "type": "simple_answer",
        "question": prompt,
        "answer": response.choices[0].message.content,
        "agent_steps": ["direct_response"]
    }

