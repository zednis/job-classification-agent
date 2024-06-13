import streamlit as st
import pandas as pd
import os
import json

from typing import List, Optional

from dataclasses import dataclass, field, asdict

from langchain.agents.openai_assistant.base import OpenAIAssistantFinish
from langchain_community.agents.openai_assistant import OpenAIAssistantV2Runnable
from langchain_core.prompts import ChatPromptTemplate
import time

st.set_page_config(layout="wide", page_title="Job Classification Assistant")

# check that environemnt variables are set
if "env_var_init" not in st.session_state:

   assistant_id = os.environ.get("ASSISTANT_ID")

   if not assistant_id:
          raise ValueError("ASSISTANT_ID environment variable is not set.  Please run create_assistant.py to create an assistant and set env var ASSISTANT_ID")

   st.session_state['assistant_id'] = assistant_id

   if not os.environ.get("OPENAI_API_KEY"):
      raise ValueError("OPENAI_API_KEY environment variable is not set.  Please set the OPEN_API_KEY environment variable.")

   st.session_state['env_var_init'] = True

  
if "career_clusters" not in st.session_state: 
   # Load the career clusters from data/occupation_career_clusters.json into a DataFrame
  career_clusters = pd.read_json("data/processed/occupation_career_clusters.json", orient="records", lines=True)
  st.session_state["career_clusters"] = career_clusters

with st.expander("Classification Hints"):
   st.text_area("Hints", placeholder="Did the assistant get something wrong?  Add additional hints here and try again!", key="hints")

prompt_template = """Classify the following job post into an ONET classification. Include the occupation code, title, and a short one paragraph explanation for the classification.  Do not include source references.  Consider the career pathway and cluster for the occupation.  Put people manager titles into management occupations.

Return the results as JSON with the following fields: occupation_code, occupation_title, explanation (optional).

agent should include explanation: {include_explanation}

additional hints: {hints}

job post title: {job_post_title}
job post description: {job_post_description}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

@dataclass
class JobClassification:
   occupation_link: str = field(init=False)
   occupation_code: str
   occupation_title: str
   explanation: Optional[str] = None

   def __post_init__(self):
      self.occupation_link = f'https://www.onetonline.org/link/summary/{self.occupation_code}'

def parse_output_to_job_classification(output: OpenAIAssistantFinish) -> JobClassification:
   '''Parse the output from the assistant into a JobClassification object'''   
   output_text = output.return_values.get('output')
   output_text = output_text.lstrip('```json').rstrip('```')
   output_obj = json.loads(output_text)
   return JobClassification(**output_obj)

if "agent" not in st.session_state:
   assistant_id = st.session_state["assistant_id"]
   agent = OpenAIAssistantV2Runnable(assistant_id=assistant_id, as_agent=True)
   st.session_state['agent'] = agent
   st.session_state['chain'] = (agent | parse_output_to_job_classification)

st.sidebar.title("Assistant Configuration")
st.sidebar.write(f"Assistant ID: `{st.session_state['agent'].assistant_id}`")
st.sidebar.checkbox("Include Explanation?", True, key="include_explanation")

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

def display_job_classification(job_classification: JobClassification):
   
   career_clusters = get_career_clusters(job_classification.occupation_code)
   career_pathways = get_career_pathways(job_classification.occupation_code)

   st.write(f"#### [{job_classification.occupation_title}]({job_classification.occupation_link})")
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

        template_args = { 
           "job_post_title": job_post_title, 
           "job_post_description": job_post_description, 
           "include_explanation": st.session_state["include_explanation"], 
           "hints": st.session_state["hints"]
        }

        input = {"content": prompt.format(**template_args)}

        try:
          start_time = time.time()
          with st.spinner('Classifying...'):
            classification_result = chain.invoke(input)
          if classification_result:
            display_job_classification(classification_result)

        except ValueError as e:
          st.error(f"Error: {e}")

        finally: 
          end_time = time.time()
          execution_time = end_time - start_time
          st.info(f"Execution time: {execution_time} seconds")