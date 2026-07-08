import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key= os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found, get it from groq")

client = Groq(api_key = my_api_key)

model= "llama-3.3-70b-versatile"
role= "user"
prompt = "do you know virat kohli" 


#message mai role and content hi hoga
#message ek dictionary typr hai
message = {
    "role": role,
    "content":prompt
}

#messages are array of message
messages= [message]

#response is our output
response= client.chat.completions.create(model= model, messages= messages)
print(response)

answer= response.choices[0].message.content
print(answer)