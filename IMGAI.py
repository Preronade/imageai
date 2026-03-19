import os
from dotenv import load_dotenv
import groq  # <--- ADD THIS LINE to fix the NameError

# 1. Load the hidden .env file
load_dotenv()

# 2. Get the key from the environment
api_key = os.getenv("GROQ_API_KEY")

# 3. Initialize the Groq client
# This is where your code was likely failing
client = groq.Groq(
    api_key=api_key,
)