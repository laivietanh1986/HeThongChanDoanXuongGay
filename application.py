import logging
from dotenv import load_dotenv
import gradio as gr
from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    LiteLLMModel,
    HfApiModel,
    GradioUI

)
from agents.smoltool.radiology_tool import diagnose
from agents.smoltool.document_tool import get_medical_document
from smolagents import ManagedAgent
import os

class MedicalAssistantFramework:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')
        self.log("Medical Assistant Framework initialized")
        load_dotenv()
        # Get API key from environment variables
        self.api_key = os.getenv("HF_TOKEN")
        # init the model

        self.model = HfApiModel(model_id="meta-llama/Llama-3.3-70B-Instruct")
        # self.model = LiteLLMModel(model_id="gemini/gemini-2.0-flash-lite",
        #              api_key=os.getenv("GEMINI_API_KEY"))
        self.radiology_agent = ToolCallingAgent(
            model=self.model,
            tools=[diagnose],
            max_steps=3
        )
        self.radiology_managed_agent = ManagedAgent(
            name="super_radiology",
            agent=self.radiology_agent,
            description="got medical question and check and analyze radiology medical symbol.",
        )
        self.document_agent = ToolCallingAgent(
            model=self.model,
            tools=[get_medical_document]
        )
        self.document_managed_agent = ManagedAgent(
            name="super_medical_document_retriever",
            agent=self.document_agent,
            description="got infomation from radiology and using it to query and retrieve medical documents, articles, and research papers.",
        )
        self.docter_agent = CodeAgent(
            tools = [],
            model=self.model,
            managed_agents = [self.radiology_managed_agent,self.document_managed_agent],
            additional_authorized_imports=["re"],



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
        result =  self.docter_agent.run(f"""{message}""")
        return result


    def log(self, message: str):
        logging.info(message)

    def chatInitialization(self):
        self.log("Chat initialization started")
        # gr.ChatInterface(fn=self.doctor_agent_chat, type="messages").launch()
        # GradioUI(self.docter_agent).launch()
        self.docter_agent.run("you got question :the boy fell when running, this hand could not use, please check the status  ?" \
        "1. first you should check the radiology symbol of the hand, and analyze it." \
        "2. then you should query and retrieve medical documents, articles, and research papers about the hand fracture." \
        "3. finally you should give the answer to the user, and must use the information from the medical document you are query .")

         # Initialize the Gradio UI
        self.log("Chat initialization completed")

    def run(self) -> None:
        self.log("Initializing Medical Assistant Framework")
        self.log("Medical Assistant Framework is ready")
        self.log("You can now interact with the medical assistant agents.")
        self.chatInitialization()

if __name__=="__main__":
    MedicalAssistantFramework().run()
