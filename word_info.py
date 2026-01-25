from langchain import OpenAI

llm = OpenAI(temperature=0)
response = llm("Hallo wereld")
print(response)




