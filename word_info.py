from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

# OpenAI model instellen
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Conversatieketen met geheugen
conversation = ConversationChain(llm=chat_model, verbose=True)

# Voorbeeldgesprek
response = conversation.run("Hallo, kun je me iets vertellen over Ai-migo?")
print(response)



