from openai import OpenAI
import os
import argparse

MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
ASSISTANT_NAME = "Job Classification Assistant"

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Job Classification Assistant")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", choices=MODEL_OPTIONS, help="Model to use for the assistant (default: gpt-4o-mini)")
    parser.add_argument("--name", type=str, default=ASSISTANT_NAME, help="Assistant Name")
    parser.add_argument("vector_store_id", type=str, default=None, help="Vector Store ID (e.g. 'vs_UBHS....AlBE')")
    return parser.parse_args()

def main(args) -> None:

  client = OpenAI()

  INSTRUCTIONS = """You are an expert in job classification.  Use your knowledge base to answer questions about classifying job postings into ONET-SOC occupations.
Consider the occupation descriptions, sample job titles and alternate job titles, task statements, and technology skills to make your classification decisions.  
Consider the occupation's career pathway and career cluster when making the occupation classification decision.

If you can't find a good match based on the provided job description and the O*NET 28 taxonomy in provided knowledge base, you can search the web for additional information to help you make a decision.
Only return classifications that match an occupation in the O*NET 28 taxonomy.
Put people manager titles into management occupations."""

  assistant = client.beta.assistants.create(
    name=args.name,
    instructions=INSTRUCTIONS,
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [args.vector_store_id]}},
    model=args.model,
  )

  # print out assistant_id and set as os envrionment variable ASSISTANT_ID
  print("Assistant ID: ", assistant.id)
  # Set the environment variable ASSISTANT_ID
  os.environ["ASSISTANT_ID"] = assistant.id

if __name__ == "__main__":
    args = get_args()
    main(args)