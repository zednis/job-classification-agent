import streamlit as st
import pandas as pd
import os
import json
import time

from typing import List, Optional

from dotenv import load_dotenv

from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError

from langchain.agents.openai_assistant.base import OpenAIAssistantFinish
from langchain_community.agents.openai_assistant import OpenAIAssistantV2Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

st.set_page_config(layout="wide", page_title="Job Classification Assistant")

if "init" not in st.session_state:
   'Initialize the session state with environment variables'

   load_dotenv()

   assert(os.environ.get("ASSISTANT_ID") is not None), "ASSISTANT_ID environment variable is not set.  Please run create_assistant.py to create an assistant."
   assert(os.environ.get("OPENAI_API_KEY") is not None), "OPENAI_API_KEY environment variable is not set.  Please set the OPEN_API_KEY environment variable."

   st.session_state['ASSISTANT_ID'] = os.environ.get("ASSISTANT_ID")
   st.session_state['DEFAULT_PROMPT_TEMPLATE'] = os.environ.get("DEFAULT_PROMPT_TEMPLATE")
   
   st.session_state['init'] = True

st.sidebar.title("Assistant Configuration")
st.sidebar.write(f"Assistant ID: `{st.session_state.ASSISTANT_ID}`")
st.sidebar.checkbox("Include Explanation?", True, key="include_explanation")
  
if "career_clusters" not in st.session_state: 
   # Load the career clusters from data/occupation_career_clusters.json into a DataFrame
  career_clusters = pd.read_json("data/processed/occupation_career_clusters.json", orient="records", lines=True)
  st.session_state["career_clusters"] = career_clusters

with st.expander("Prompt Config"):

   help_text = """Use the following variables in your prompt template:
   - {job_post_title}: the title of the job post
   - {job_post_description}: the description of the job post
   - {format_instructions}: instructions for formatting the job post (managed by the PydanticOutputParser)
   - {include_explanation}: whether to include an explanation for the classification (controlled by the Include Explanation? checkbox in the sidebar)
   - {hints}: additional hints for the assistant
"""

   st.text_area("Prompt Template", key="prompt_template", value=st.session_state.DEFAULT_PROMPT_TEMPLATE, height=320, help=help_text)

   st.text_area("Hints", key="hints", placeholder="Did the assistant get something wrong?  Add additional hints here and try again!")

class JobClassification (BaseModel):
   occupation_code: str = Field(description="O*NET 28 occupation code", pattern=r'(\d{2}-\d{4}\.\d{2})', examples=["15-2051.00"])
   occupation_title: str = Field(description="O*NET 28 occupation title", max_length=80, examples=["Data Scientists"])
   explanation: Optional[str] = Field(description="explanation from Agent for occupation classification", max_length=1000, default=None)

   @property
   def occupation_link(self) -> str:
      return f'https://www.onetonline.org/link/summary/{self.occupation_code}'


class JobClassifications(BaseModel):
   job_classifications: List[JobClassification] = Field(description="List of Job Classifications", min_items=0, max_items=3)
   overall_explanation: Optional[str] = Field(description="Overall explanation from Agent for all occupation classifications", max_length=1000, default=None)

parser = PydanticOutputParser(pydantic_object=JobClassifications)

prompt_template = st.session_state.get("prompt_template", st.session_state.DEFAULT_PROMPT_TEMPLATE)

prompt = ChatPromptTemplate.from_template(
   prompt_template, 
   partial_variables={
      "format_instructions": parser.get_format_instructions(),
      "include_explanation": st.session_state["include_explanation"],
      "hints": st.session_state["hints"]
   })

def parse_output(output: OpenAIAssistantFinish) -> JobClassifications:
   '''Parse the output from the assistant into a JobClassifications object'''   
   output_text = output.return_values.get('output')
   output_text = output_text.lstrip('```json').rstrip('```')
   output_obj = json.loads(output_text)
   return JobClassifications(**output_obj)

if "agent" not in st.session_state:
   agent = OpenAIAssistantV2Runnable(assistant_id=st.session_state.ASSISTANT_ID, as_agent=True)
   st.session_state['agent'] = agent
   st.session_state['chain'] = (agent | parse_output)

def get_career_clusters(occupation_code: str) -> List[str]:
   '''Get Career Clusters for a given occupation code'''
   
   if "career_clusters" not in st.session_state:
      return []
   
   df = st.session_state["career_clusters"]
   values = df[df['occupation_code'] == occupation_code]['career_cluster'].to_list()
   return values[0] if len(values) > 0 else []

def get_career_pathways(occupation_code: str) -> List[str]:
   '''Get Career Pathways for a given occupation code'''
   
   if "career_clusters" not in st.session_state:
      return []
   
   df = st.session_state["career_clusters"]

   values = df[df['occupation_code'] == occupation_code]['career_pathway'].to_list()
   return values[0] if len(values) > 0 else []

def display_job_classifications(job_classifications: JobClassifications):
   
   if not job_classifications.job_classifications:
      st.write("No classifications found for the job post.")
      return

   for job_classification in job_classifications.job_classifications:

      career_clusters = get_career_clusters(job_classification.occupation_code)
      career_pathways = get_career_pathways(job_classification.occupation_code)

      st.write(f"#### [{job_classification.occupation_title}]({job_classification.occupation_link })")
      st.write(f"**O*NET-SOC Code**: {job_classification.occupation_code}")
    
      # show career cluster and career pathway
      st.write(f"**Career Clusters**: {', '.join(career_clusters) if len(career_clusters) else 'N/A'}")
      st.write(f"**Career Pathways**: {', '.join(career_pathways) if len(career_clusters) else 'N/A'}")

      if job_classification.explanation:
         st.write(f"**Explanation**:\n\n{job_classification.explanation}")

with st.form("job_post"):
   job_post_title = st.text_input("Job Post Title", key="job_post_title")
   job_post_description = st.text_area("Job Post Description", key="job_post_description")

   submitted = st.form_submit_button("Classify Job Post")

   if submitted:
      chain = st.session_state["chain"]

      job_post_title = st.session_state["job_post_title"]
      job_post_description = st.session_state["job_post_description"]

      include_explanation = st.session_state["include_explanation"]
      hints = st.session_state["hints"]

      template_args = { 
         "job_post_title": job_post_title, 
         "job_post_description": job_post_description, 
         "include_explanation": include_explanation, 
         "hints": hints if hints else "N/A"
      }

      input = {"content": prompt.format(**template_args)}

      try:
         start_time = time.time()
         with st.spinner('Classifying...'):
            results = chain.invoke(input)
            
            if results:
               display_job_classifications(results)
            else:
               st.info("No results returned from the assistant")
      
      except ValidationError as e:
         st.error(f"Validation Error: {e}\n\n{e.errors()}")

      except ValueError as e:
         st.error(f"Error: {str(e)}")

      finally: 
         end_time = time.time()
         execution_time = end_time - start_time
         st.info(f"Execution time: {execution_time} seconds")