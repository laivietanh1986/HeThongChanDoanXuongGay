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
from agents.smoltool.radiology_tool import identify_bone_location, has_fracture,fracture_type
from agents.smoltool.document_tool import retriever_tool
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
            tools=[identify_bone_location, has_fracture, fracture_type],
            max_steps=3
        )
        self.radiology_managed_agent = ManagedAgent(
            name="super_radiology",
            agent=self.radiology_agent,
            description="got medical question and check and analyze radiology medical symbol.",
        )
        self.document_agent = ToolCallingAgent(
            model=self.model,
            tools=[retriever_tool],
            max_steps=4,  # Limit the number of reasoning steps

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
    def doctor_agent_chat(self,file_path: str,message:str,another_param)-> str:
        """
        Function to handle chat messages with the doctor agent.
        """

        self.log("another_param: {}".format(another_param))
        self.log("file_path: {}".format(file_path))

        self.log(f"Received message: {message}")
        conversation = []

        conversation.append({"role": "user", "content": message})
        self.log("Conversation history: {}".format(conversation))
        # result =  self.docter_agent.run(f"""
        # "you using the image from this you got question:{message} ?" \
        # # "1. first you should check the radiology symbol of the hand, if this is hand we continue to check the fracture , type of fracture , and analyze it." \
        # # "2. if this is not hand, please answer user that you are not responsibility for this case, you are only take care of hand bone ." \
        # # "3. then you should query and retrieve medical documents, articles, and research papers about the hand fracture." \
        # # "4. finally you should give the answer to the user, and must use the information from the medical document you are query ."
        # """)
        result = "okie"
        return result


    def log(self, message: str):
        logging.info(message)

    def chatInitialization(self):
        self.log("Chat initialization started")
        # gr.ChatInterface(fn=self.doctor_agent_chat, type="messages").launch()
        # GradioUI(self.docter_agent).launch()
        image_input = gr.Image(type="filepath",sources =["upload"], label="Upload X-ray Image")
        message_input = gr.Textbox(label="Enter your question about the X-ray image")
        history_input = gr.Textbox(label="Conversation History", visible=False)
        output = gr.Textbox(label="Response from Medical Assistant")
        gr.Interface(
            fn=self.doctor_agent_chat,
            inputs=[image_input,message_input, history_input],
            outputs=output,
            title="Medical Assistant Framework",
            description="A framework to assist with medical questions and radiology analysis.",
            theme="default",
            allow_flagging="never",
        ).launch(share=False)
        # self.docter_agent.run("you using the image from this you got question:the boy fell when running, this hand is fracture , look like greenstick,  and could not use, please check the status  ?" \
        # "1. first you should check the radiology symbol of the hand, if this is hand we continue to check the fracture , type of fracture , and analyze it." \
        # "2. if this is not hand, please answer user that you are not responsibility for this case, you are only take care of hand bone ." \
        # "3. then you should query and retrieve medical documents, articles, and research papers about the hand fracture." \
        # "4. finally you should give the answer to the user, and must use the information from the medical document you are query .")

         # Initialize the Gradio UI
        self.log("Chat initialization completed")

    def run(self) -> None:
        self.log("Initializing Medical Assistant Framework")
        self.log("Medical Assistant Framework is ready")
        self.log("You can now interact with the medical assistant agents.")
        self.chatInitialization()

if __name__=="__main__":
    MedicalAssistantFramework().run()
