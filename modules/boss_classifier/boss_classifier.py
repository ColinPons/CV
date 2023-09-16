# !pip install pyarrow
import openai, streamlit as st
from time import sleep
from numpy import dot
from numpy.linalg import norm
from pandas import read_parquet, DataFrame
from os import path
from typing import List

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 1
OPEN_AI_KEY = st.secrets.OPENAI_API_KEY

def create_vector(prompt:str, model="text-embedding-ada-002", api_key=OPEN_AI_KEY) -> List[float] and int:
    """ prompt:str, mode:str|default=text-embedding-ada-002, api_key:str|.env API_KEY """
    openai.api_key = api_key

    for retry_count in range(MAX_RETRIES):
        try:
            # API call to Embedding, prompt encoded and decoded to prevent intermittant issues
            response = openai.Embedding.create(input=prompt.encode(encoding="ASCII", errors="ignore").decode(), model=model)

            # return embedding vector and total tokens used
            return response["data"][0]["embedding"], int(response["usage"]["total_tokens"])
        
        except Exception as e:

            if retry_count < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
                sleep(RETRY_DELAY_SECONDS)

            else:
                raise Exception(f"API request failed after {MAX_RETRIES} retries: {e}")

def classify_product(prompt:str) -> List[tuple]:
    """ 
    Input : str  Return : list[tuple]

    Creates vector for prompt and returns list of tuples
    (similarity:float, boss_code:str, boss_decription:str)
    """

    nexus_data = read_parquet(path.join(path.dirname(path.realpath(__file__)),"BOSS classification vectorised.parquet"))

    # Get vector from the prompt
    prompt_vector, total_tokens = create_vector(prompt)

    data_list = []

    # Iterate over nexus data
    for index, boss_vector in enumerate(nexus_data["boss_vector"]):

        # Get similarity
        similarity = dot(prompt_vector, boss_vector)/(norm(prompt_vector)*norm(boss_vector))
        
        # Create tuple and add to list
        data_list.append((similarity, nexus_data["boss_code"][index], nexus_data["boss_description"][index]))

    # Sort list of tuples
    data_list.sort(key=lambda x: x[0], reverse=True)

    return data_list

def create_dataframe(user_input:str) -> DataFrame:

    results = classify_product(user_input)
    
    # Convert the list of tuples into a DataFrame for better visualization
    df = DataFrame(results, columns=["Similarity %", "BOSS Code", "BOSS Description"])

    # Reorder dataframe
    df = df[["BOSS Code", "BOSS Description", "Similarity %"]]

    # Convert values
    df["Similarity %"] = round((df["Similarity %"] * 100),2)  

    return df.head(5)

def display_boss_classifier_module():

    st.write(
        """
        This classifier uses one-shot classification using semantic embeddings.

        I decided to use the BOSS Federation's IPSC classification structure as it is
        freely available, when a new version is released the previous is replaced and
        the classification has a low number of classifications making it a good candidate for this
        proof of concept.

        The tool compares the semantic embedding of a product description against the embeddings of
        the BOSS classification, the result is a percentage match in order to support better identification
        for users unfarmiliar with the classification.

        """)

    st.markdown("https://www.bossfederation.com/", unsafe_allow_html=False)
    
    user_input = st.text_area("Enter a product description:", max_chars=100)

    # Initialize or retrieve counter using Streamlit's state feature
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    if st.session_state.counter < 100:

        if user_input:

            df = create_dataframe(user_input=user_input)

            st.session_state.counter += 10

            st.progress(st.session_state.counter, text="Free Play")

            # Display the top 5
            st.table(df.head(5))

    else:
        st.write("Thank you for trying this module :)")