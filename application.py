import logging
from dotenv import load_dotenv
import gradio as gr
from agents.doctor_agent import DoctorAgent
from agents.radiologist_agent import RadiologistsAgent

class MedicalAssistantFramework:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')
        self.log("Medical Assistant Framework initialized")
        load_dotenv()
        self.doctor_agent = DoctorAgent()
        self.radiologist_agent = RadiologistsAgent()

    def log(self, message: str):
        logging.info(message)

    def chatInitialization(self):
        self.log("Chat initialization started")
        gr.ChatInterface(fn=self.doctor_agent.chat, type="messages").launch()
        self.log("Chat initialization completed")

    def run(self) -> None:
        self.log("Initializing Medical Assistant Framework")
        self.log("Medical Assistant Framework is ready")
        self.log("You can now interact with the medical assistant agents.")
        self.chatInitialization()

if __name__=="__main__":
    MedicalAssistantFramework().run()
