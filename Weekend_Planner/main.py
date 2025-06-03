import streamlit as st
import requests
import os

# Constants
HF_TOKEN = "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"  # Replace with your token
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300},
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        # Some models return list of dictionaries with 'generated_text'
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        # Some models return a dictionary with 'generated_text'
        elif isinstance(result, dict) and 'generated_text' in result:
            return result['generated_text']
        else:
            return "Unexpected response format from Hugging Face API."
    elif response.status_code == 404:
        return "❌ Error 404: Model not found. Check model name."
    elif response.status_code == 401:
        return "❌ Error 401: Invalid API token."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

def run_task(task, agents, context):
    agent_key = task["agent"]
    agent_info = agents.get(agent_key, {})
    role = agent_info.get("role", "")
    goal = agent_info.get("goal", "")
    backstory = agent_info.get("backstory", "")

    prompt = f"""
You are {role}
Goal: {goal}
Backstory: {backstory}

Context:
City: {context['city']}
People: {context['people']}
Budget: {context['budget']}
Interests: {', '.join(context['interests'])}

Task: {task['description']}

Please provide the output expected:
"""
    return query_huggingface(prompt)

def main():
    st.title("🗓️ Weekend Planner - Hugging Face Edition")

    st.sidebar.header("User Preferences")
    city = st.sidebar.text_input("City", "Hyderabad")
    people = st.sidebar.slider("Number of People", 1, 10, 2)
    budget = st.sidebar.text_input("Budget", "2000 INR")
    interests = st.sidebar.multiselect(
        "Interests",
        ["Food", "Museums", "Parks", "Shopping", "Adventure", "Relaxation", "Nightlife"],
        default=["Food", "Parks"]
    )

    if st.button("Generate Weekend Plan"):
        context = {
            "city": city,
            "people": people,
            "budget": budget,
            "interests": interests
        }

        agents = {
            "weekend_itinerary_agent": {
                "role": "Weekend Itinerary Planner",
                "goal": "Create an engaging and relaxing 2-day weekend plan.",
                "backstory": "An AI that specializes in optimizing weekend experiences."
            }
        }

        task = {
            "agent": "weekend_itinerary_agent",
            "description": "Generate a weekend itinerary based on user preferences."
        }

        with st.spinner("Generating plan..."):
            output = run_task(task, agents, context)
            st.markdown("### 🧠 Generated Plan:")
            st.markdown(output)

if __name__ == "__main__":
    main()
