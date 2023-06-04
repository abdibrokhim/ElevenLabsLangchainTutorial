import openai
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os


os.environ['OPENAI_API_KEY'] = 'api-key'


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])


llm = ChatOpenAI(temperature=0, openai_api_key=os.environ.get("OPENAI_API_KEY"))
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)


def get_response(prompt, podcaster, guest,):
    _prompt = f"""

    Generate a podcast with {podcaster} and {guest}. They are discussing about {prompt}.
    
    """

    response = conversation.predict(input=_prompt)
    
    return response
