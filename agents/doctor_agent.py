# imports
import os
from agents.radiologist_agent import RadiologistsAgent
from agents.agent import Agent
from google import genai
from google.genai import types
from agents.llm_gemini import LargeLanguageModelGemini


class DoctorAgent(Agent):
    """Doctor Agent that uses a remote LLM to answer medical questions and provide diagnoses"""
    name = "Doctor Agent"
    color = Agent.BLUE
    system_prompt = (
            "You are a medical doctor with expertise in diagnosing and treating various conditions. "
            "You will be provided with patient symptoms and medical history, and your task is to provide a diagnosis and treatment plan."
            "If the user's question is a general or non-medical question, answer it directly as a knowledgeable assistant. "
            "If the user's question is medical in nature (e.g., about symptoms, diagnosis, or treatment), first consult the Radiologist Agent to obtain any relevant radiological information. "
            "After receiving the radiological information, use it to provide a comprehensive and accurate medical answer to the user's question."
    )
    def chat(self, message,history) -> str:
        """Method to handle chat messages and return a response from the LLM"""
        history.append({
            "role": "user",
            "content": message
        })
        history_text = "\n".join([f"{item['role']}: {item['content']}" for item in history])
        return self.llm.call_model(history_text)
    def radio_diagnose(self, message: str) -> str:
        """Method to handle medical diagnosis requests"""
        self.log(f"Diagnosing message: {message}")
        return self.radiologist_agent.diagnose(message)
        # Placeholder for actual diagnosis logic

    def __init__(self):
        self.log("Initializing Doctor Agent")
        self.llm = LargeLanguageModelGemini(self.system_prompt)
        self.radiologist_agent = RadiologistsAgent()
        self.log("Doctor Agent initialized successfully")


