
import pandas as pd

RAW_DATA_DIR = "../data/raw"
PROCESSED_DATA_DIR = "../data/processed"

# generate JSONL files for ONET 28 data

def process_desciptions():
    '''Create a JSONL file of occupation descriptions and reported titles for occupations'''

    # load data/Occupation Data.xslx in a DataFrame
    df = pd.read_excel(f"{RAW_DATA_DIR}/Occupation Data.xlsx")

    # rename column 'O*NET-SOC Code' to 'code'
    column_map = {
        "O*NET-SOC Code": "occupation_code",
        "Title": "occupation_title",
        "Description": "occupation_description"
    }

    df.rename(columns=column_map, inplace=True)

    # create a JSONL file of 'occupation_descriptions.jsonl' of df
    df.to_json(f"{PROCESSED_DATA_DIR}/occupation_descriptions.json", orient="records", lines=True)

def process_sample_titles():

    # load data/Sample of Reported Titles.xlsx in a DataFrame
    df = pd.read_excel(f"{RAW_DATA_DIR}/Sample of Reported Titles.xlsx")

    # drop column 'Shown in My Next Move'
    df.drop(columns=["Shown in My Next Move"], inplace=True)

    # rename column 'O*NET-SOC Code' to 'occupation_code' and 'Title' to 'occupation_title'
    column_map = {
        "O*NET-SOC Code": "occupation_code", 
        "Title": "occupation_title", 
        "Reported Job Title": "sample_job_title"
    }
    df.rename(columns=column_map, inplace=True)

    # create a JSONL file 'occupation_sample_titles.jsonl' of df
    df.to_json(f"{PROCESSED_DATA_DIR}/occupation_sample_titles.json", orient="records", lines=True)

def process_alternate_titles():
    '''Create a JSONL file of alternate job titles for occupations'''

    # load data/Alternate Titles.xlsx in a DataFrame
    df = pd.read_excel(f"{RAW_DATA_DIR}/Alternate Titles.xlsx")

    # drop columns 'Alternate Title' and 'Short Title' from df_alternate_titles
    df.drop(columns=["Short Title", "Source(s)"], inplace=True)

    # rename column 'O*NET-SOC Code' to 'occupation_code' and 'Title' to 'occupation_title'
    columnn_map = {
        "O*NET-SOC Code": "occupation_code",
        "Title": "occupation_title",
        "Alternate Title": "alternate_job_title"
    }
    df.rename(columns=columnn_map, inplace=True)

    # create a JSONL file of df
    df.to_json(f"{PROCESSED_DATA_DIR}/occupation_alternate_titles.json", orient="records", lines=True)

def process_task_statements():
    '''Create a JSONL file of Task Statements for occupations'''

    df = pd.read_excel(f"{RAW_DATA_DIR}/Task Statements.xlsx")

    # drop unnecessary columns
    df.drop(columns=["Task ID", "Incumbents Responding", "Date", "Domain Source"], inplace=True)

    column_map = {
        "O*NET-SOC Code": "occupation_code",
        "Title": "occupation_title",
        "Task": "task_statement",
        "Task Type": "task_type",
    }
    df.rename(columns=column_map, inplace=True)

    df.to_json(f"{PROCESSED_DATA_DIR}/occupation_task_statements.json", orient="records", lines=True)

def process_technology_skills():
    '''Create a JSONL file of Technology Skills for occupations'''

    df = pd.read_excel(f"{RAW_DATA_DIR}/Technology Skills.xlsx")

     # drop unnecessary columns
    df.drop(columns=["Commodity Code"], inplace=True)

    column_map = {
        "O*NET-SOC Code": "occupation_code",
        "Title": "occupation_title",
        "Example": "technology",
        "Commodity Title": "technology_category",
        "Hot Technology": "hot_technology",
        "In Demand": "in_demand",
    }
    df.rename(columns=column_map, inplace=True)

    df.to_json(f"{PROCESSED_DATA_DIR}/occupation_technology_skills.json", orient="records", lines=True)

def process_career_clusters():
    '''Create a JSONL file of Career Clusters for occupations'''

    df = pd.read_excel(f"{RAW_DATA_DIR}/All Career Clusters.xlsx", skiprows=3)

    column_map = {
        "Code": "occupation_code",
        "Occupation": "occupation_title",
        "Career Cluster": "career_cluster",
        "Career Pathway": "career_pathway",
    }
    df.rename(columns=column_map, inplace=True)
    df = df[["occupation_code", "occupation_title", "career_pathway", "career_cluster"]]

    df.sort_values(by=['occupation_code'], inplace=True)

    # split career_cluster and career_pathway by ';'
    df['career_cluster'] = df['career_cluster'].apply(lambda x: [y.strip() for y in x.split(';')] if isinstance(x, str) else x)
    df['career_pathway'] = df['career_pathway'].apply(lambda x: [y.strip() for y in x.split(';')] if isinstance(x, str) else x)

    df.to_json(f"{PROCESSED_DATA_DIR}/occupation_career_clusters.json", orient="records", lines=True)

process_desciptions()
process_sample_titles()
process_alternate_titles()
process_task_statements()
process_technology_skills()
process_career_clusters()

