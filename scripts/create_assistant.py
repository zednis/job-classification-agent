from openai import OpenAI
import os

client = OpenAI()

## TODO add the following to the agent instructions?
# When you evaluate a job post, consider the following:
# - Does the job post title match a sample or alternate job title in the ONET taxonomy?  If so, return this occupation.
# - Does the job post description contain responsibility or qualification statements that match the task statements for an occupation in the ONET taxonomy?  If so, return this occupation.
# - Does the job post description contain mention of required skills or technologies that are associated with an occupation in the ONET taxonomy?  If so, return this occupation.
# - Does the job post description borrow language from the ONET taxonomy?  If so, return this occupation


INSTRUCTIONS = """You are an expert in job classification.  Use your knowledge base to answer questions about classifying job postings into ONET-SOC occupations.
Consider the occupation descriptions, sample and alternate job titles, task statements, and technology skills to make your classification decisions.  
Consider the career pathway and cluster when making the occupation classification decision.  

If you can't find a good match based on the provided job description and ONET taxonomy in provided knowledge base, you can search the web for additional information to help you make a decision.

Put people manager titles into management occupations."""

ASSISTANT_NAME = "Job Classification Assistant"
MODEL = "gpt-4o"

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

if not VECTOR_STORE_ID:
    raise ValueError("""VECTOR_STORE_ID environment variable is not set.  
                     Please run create_vector_store.py to create a vector store and set env var VECTOR_STORE_ID.""")

assistant = client.beta.assistants.create(
  name=ASSISTANT_NAME,
  instructions=INSTRUCTIONS,
  tools=[{"type": "file_search"}],
  tool_resources={"file_search": {"vector_store_ids": [VECTOR_STORE_ID]}},
  model=MODEL,
)

# print out assistant_id and set as os envrionment variable ASSISTANT_ID
print("Assistant ID: ", assistant.id)
# Set the environment variable ASSISTANT_ID
os.environ["ASSISTANT_ID"] = assistant.id