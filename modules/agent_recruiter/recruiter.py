import openai, streamlit as st
from re import sub
from ast import literal_eval
from time import sleep

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 1

OPEN_AI_KEY = st.secrets.OPENAI_API_KEY

def clean_prompt(prompt:str) -> str:
    return sub(r'[^a-zA-Z0-9]', '', prompt)

def string_to_list(list_str: str) -> list[dict[str, str]]:
    return literal_eval(list_str)

def api_call(prompt:str) -> str:

    system_prompt = [
        "Role: You are a profession recruitment specialist who is able to identify the minimum required roles to complete a specific requirement.",
        "Task: The user will provide you will a specific task, you will identify multiple job titles and outline in granular detail the job title, job specifications and skills for each job title required to complete the task.",
        "Format: You will respond only with data formatted as a list of dictionaries, for example {'job_title':'str', 'job_specification':'str', 'skills':['str', etc...]}",
        "Important: You will only reply as outline within the Format information, provide no pre or post summary analysis or any other comments."
        ]
    
    attempts = 0
    openai.api_key = OPEN_AI_KEY

    while attempts < MAX_RETRIES:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [{"role":"user", "content":prompt}, {"role":"system", "content":"".join(system_prompt)}],
                temperature = 1,
                max_tokens = 2000
            )

            return f"{completion['choices'][0].message['content']}"
        
        except Exception:
            attempts += 1
            sleep(3)

    else:
        return "Sorry maximum attempts exceeded :("

def display_agent_recruiter():

    st.write(
        """
        This function is primarily designed to create AI agent roles for use with other AI agent based functions.

        When using large language models, being specific to the role required in order to complete a task typically generates higher quality outputs.
        The challenge is that for an organisation, its sometime challenging to identify granular detail for roles needed to complete the task.

        For example, if we have a task to redesign a master data model without a domain expert, it is challenging to identify all of the specific roles the project will require.

        """)

    user_input = st.text_area(
        "Enter your required task you wish to complete:", 
        max_chars=100, 
        placeholder="I need to redesign a master data model for products within a eCommerce business which specialises in toys for cats.",
        height=20
        )
    
    if user_input:

        with st.spinner("Recruiting..."):

            reply = api_call(prompt=user_input)

        st.success("Recruitment complete!")
        st.divider()

        reply_list = string_to_list(list_str=reply)

        st.json(body=reply_list, expanded=True)
        st.divider()