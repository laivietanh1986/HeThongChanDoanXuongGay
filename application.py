import logging
from dotenv import load_dotenv
import gradio as gr
from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    LiteLLMModel,

    GradioUI

)
from smolagents import ManagedAgent
import os

class MedicalAssistantFramework:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')
        self.log("Medical Assistant Framework initialized")
        load_dotenv()
        # init the model
        self.model = LiteLLMModel(model_id="gemini/gemma-3-27b-it",
                     api_key=os.getenv("GEMINI_API_KEY"))
        self.radiology_agent = ToolCallingAgent(
            model=self.model,
            tools=["radiology_tool"]
        )
        self.radiology_managed_agent = ManagedAgent(
            name="Radiology Managed Agent",
            agent=self.radiology_agent,
            description="I am a radiology expert. I can assist with interpreting medical images and providing insights on radiological findings.",
        )
        self.document_agent = ToolCallingAgent(
            model=self.model,
            tools=["document_tool"]
        )
        self.document_managed_agent = ManagedAgent(
            name="Document Managed Agent",
            agent=self.document_agent,
            description="query and retrieve medical documents, articles, and research papers.",
        )
        self.docter_agent = CodeAgent(
            tools = [],
            model=self.model,
            managed_agent = [self.radiology_managed_agent, self.document_managed_agent],
            name="Doctor Agent",
             additional_authorized_imports=["re"],

        # system_prompt="""You are a blog post creation manager. Coordinate between research, writing, and editing teams.
        # Follow these steps:
        # 1. Use research_agent to gather information
        # 2. Pass research to research_checker_agent to check for relevance
        # 3. Pass research to writer_agent to create the initial draft
        # 4. Send draft to editor for final polish
        # 4. Save the final markdown file
        # """
        )
    def doctor_agent_chat(self,message: str,history:str)-> str:
        """
        Function to handle chat messages with the doctor agent.
        """
        self.log(f"Received message: {message}")
        conversation = []
        if history:
            conversation.append(history)
        conversation.append({"role": "user", "content": message})
        self.log("Conversation history: {}".format(conversation))
        return self.docter_agent.run(f"""
            You are a medical doctor with expertise in diagnosing and treating various conditions.
            You will be provided with patient symptoms and medical history, and your task is to provide a diagnosis and treatment plan.

            If the user's question is medical in nature (e.g., about symptoms, diagnosis, or treatment)
            1. First ask Radiology Agent: For interpreting medical images and providing insights on radiological findings.
            2. Then querying and retrieving medical documents, articles.
            3. Finally, provide a comprehensive response based on the information gathered.
            If the user's question is not related to medical topics, answer it directly as a knowledgeable assistant.
            {message}
        """)

    def log(self, message: str):
        logging.info(message)

    def chatInitialization(self):
        self.log("Chat initialization started")
        # gr.ChatInterface(fn=self.doctor_agent_chat, type="messages").launch()
        GradioUI(self.docter_agent).launch()
        self.log("Chat initialization completed")

    def run(self) -> None:
        self.log("Initializing Medical Assistant Framework")
        self.log("Medical Assistant Framework is ready")
        self.log("You can now interact with the medical assistant agents.")
        self.chatInitialization()

if __name__=="__main__":
    MedicalAssistantFramework().run()
