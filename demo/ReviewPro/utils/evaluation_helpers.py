###documentation

import itertools
import json
import os
import re

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# set up model info
model = "gpt-4o"
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=1.0,
    max_tokens=2048,
)

# prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant to the manager of a small coffee shop.",
        ),
        (
            "human",
            """
Complete an employee evaluation using this template format for a response:

Employee: {employee_name}
Date and history:
Overall Rating: Outstanding (5) / Exceeds Expectations (4) / Fully Successful (3) / Unacceptable (0) 
- With text justification
Critical Element: (Same scale as overall rating)
- Makes drinks (Coffee, Latte, etc)
- Timeliness (how quick you got your order done)
- Customer Satisfaction 
- Store Operations
- Shows up to work on time
Comments and Suggestions:

Based on the inputs:

Goals/objectives
{goals_and_objectives}

Employee self evaluation

{self_eval}

Manager comments

{manager_comments}
        
""",
        ),
    ]
)


def query_llm(data_folder: str, input_filename: str) -> pd.DataFrame:
    """
    queries llm model above with the prompt detailed above with the information from the input data folder
    """

    sample_input_data_df = pd.read_csv(
        os.path.join(data_folder, input_filename)
    )

    # responses = []
    # prompts = []

    chain = prompt_template | llm

    response_df = []

    if "EmployeeName" in sample_input_data_df.columns:
        sample_input_data_df.rename(columns={"EmployeeName": "Employee"},inplace=True,)

    for row_num, row in sample_input_data_df.iterrows():
        pii_data = {
            "employee_name": row.Employee,  # Name,
            "goals_and_objectives": row.goalsAndObjectives,
            "self_eval": row.employeeSelfEval,
            "manager_comments": row.managerComments,
        }

        prompt = prompt_template.format(**pii_data)
        response = chain.invoke(pii_data)

        pii_data["response"] = response.content
        pii_data["prompt"] = prompt
        pii_data["model"] = llm

        response_df.append(pii_data)

    response_df = pd.DataFrame(response_df)

    return response_df


def get_overall_rating(response):
    pattern = r"Overall Rating(.+\d.+)\n"
    # pattern = r'\(?(\d+(?:\.\d+)?)\)?'
    overall_score = 0
    match = re.findall(pattern, response, flags=re.I)
    if len(match) > 0:
        res = re.findall(r"\d", match[0])

        if len(res) > 0:
            overall_score = float(res[0].strip())
    return overall_score  # if overall_score >= 3 else 0.0


def get_critical_ratings(response):
    # Regex for critical scores
    drinks_regex = r"Makes drinks(.+\d.+)\n"
    time_regex = r"Timeliness(.+\d.+)\n"
    cust_regex = r"Customer Satisfaction(.+\d.+)\n"
    store_regex = r"Store Operations(.+\d.+)\n"
    shows_regex = r"Shows up to work on time(.+\d.+)\n"

    critical_regex = [
        drinks_regex,
        time_regex,
        cust_regex,
        store_regex,
        shows_regex,
    ]
    critical_match = []

    for cr in critical_regex:
        cm = "0"
        res = re.findall(cr, response, flags=re.I)

        if len(res) > 0:
            cm = res[0].strip()
            if len(cm) == 0:
                cm = "0"
        critical_match.append(cm)

    critical_scores = []
    for cm in critical_match:
        cs = 0
        res = re.findall(r"\d", cm)
        if len(res) > 0:
            cs = res[0]
        critical_scores.append(cs)

    return critical_scores


def get_name(response):
    """Template: Should extract employee name from the response"""
    name_regex = r"Employee:(.+)\n"
    ename = re.findall(name_regex, response, flags=re.I)
    for n in ename:
        n = n.strip()
        dont = re.findall("evaluation", n, flags=re.I)
        if len(dont) == 0:
            return n
    return


def process_queries(response_df: pd.DataFrame) -> pd.DataFrame:
    output_df = pd.DataFrame(
        {
            "evaluationOutput": response_df.response,
            "prompt": response_df.prompt,
            "extractedOverallRating": [
                get_overall_rating(response)
                for response in response_df.response
            ],
            "extractedDrinks": [
                float(get_critical_ratings(response)[0])
                for response in response_df.response
            ],
            "extractedTimeliness": [
                float(get_critical_ratings(response)[1])
                for response in response_df.response
            ],
            "extractedCustomerSatisfaction": [
                float(get_critical_ratings(response)[2])
                for response in response_df.response
            ],
            "extractedStoreOperations": [
                float(get_critical_ratings(response)[3])
                for response in response_df.response
            ],
            "extractedOnTime": [
                float(get_critical_ratings(response)[4])
                for response in response_df.response
            ],
            "extractedName": [
                get_name(response) for response in response_df.response
            ],
            "modelCalled": response_df.model,
        }
    )
    output_df["averageScore"] = (
        output_df[
            [
                "extractedDrinks",
                "extractedTimeliness",
                "extractedCustomerSatisfaction",
                "extractedStoreOperations",
                "extractedOnTime",
            ]
        ]
        .mean(axis=1)
        .round()
    )
    return output_df
