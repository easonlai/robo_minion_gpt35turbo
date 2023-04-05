# Imports the OpenAI API and Streamlit libraries.
import openai
import streamlit as st
from streamlit_chat import message

# Sets up the OpenAI API configuration for the Azure endpoint of the Azure OpenAI Service resource.
# The API key is retrieved from the Streamlit secrets manager for security purposes.

# The 'openai.api_type' is set to 'azure' to indicate that the API is being used with Azure OpenAI Service.
openai.api_type = "azure"
# The 'openai.api_base' is set to the base URL for the Azure OpenAI Service resource.
openai.api_base = "https://PLEASE_ENTER_YOUR_OWN_AOAI_RESOURCE_NAME.openai.azure.com/"
# The 'openai.api_version' is set to the API version for the Azure OpenAI Service resource.
# https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2023-03-15-preview/inference.json
openai.api_version = "2023-03-15-preview"
# The 'openai.api_key' is set to the API key manually retrieved from the Azure OpenAI Service resource.
# openai.api_key = "PLEASE_ENTER_YOUR_OWN_API_KEY"
# The 'openai.api_key' is set to the API key retrieved from the Streamlit secrets manager.
openai.api_key = st.secrets["AOAI_API_KEY"]

# Streamlit to set the page header and icon.
st.set_page_config(
        page_title="Robo Minion",
        page_icon="🤖",
    )

# Streamlit to set the page layout and make a simple page title and logo.
col1, col2 = st.columns([1,2])
with col1:
    st.image("./images/robo_minion_icon_v1.png", width=200)
with col2:
    st.title("Robo Minion 🤖")
    st.header("Powered by AOAI - GPT 3.5 Turbo 🚀")

# Initializes the Streamlit session state with default values for the 'prompts', 'generated', 
# The 'prompts' list stores the conversation history, with each message represented as a dictionary with 'role' and 'content' keys.
# Deine the 'role' key as 'system' for the AI model's messages.
if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "You are a robotic minion created by Eason in Minions.app Laboratory. You are upbeat and friendly. Your response should be as concise with a sense of humor. You introduce yourself when first saying, Bello! Buddy. If the user asks you for anything information about Minions, or Despicable Me, or Universal Studios,  you will try to use our intelligence to reply. If the user asks you not related Minions, or Despicable Me, or Universal Studios, you will tell them I don't know."}]
# The 'generated' list stores the AI model's responses to the user's messages.
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
# The 'past' list stores the user's previous messages.
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Define the 'generate_response' function to send the user's message to the AI model 
# and append the response to the 'generated' list.
def generate_response(prompt):
    # The 'prompts' list is updated with the user's message before sending it to the AI model.
    st.session_state['prompts'].append({"role": "user", "content":prompt})
    # The 'openai.ChatCompletion.create' function is used to generate a response from the AI model.
    completion=openai.ChatCompletion.create(
        engine="PLEASE_ENTER_YOUR_OWN_AOAI_GPT35_TURBO_DEPLOYMENT_NAME", # The 'engine' parameter specifies the name of the OpenAI GPT-3.5 Turbo engine to use.
        temperature=0.7, # The 'temperature' parameter controls the randomness of the response.
        max_tokens=512, # The 'max_tokens' parameter controls the maximum number of tokens in the response.
        top_p=0.95, # The 'top_p' parameter controls the diversity of the response.
        # The 'messages' parameter is set to the 'prompts' list to provide context for the AI model.
        messages = st.session_state['prompts']
    )
    # The response is retrieved from the 'completion.choices' list and appended to the 'generated' list.
    message=completion.choices[0].message.content
    return message

# The 'new_topic_click' function is defined to reset the conversation history and introduce the AI assistant.
def new_topic_click():
    st.session_state['prompts'] = [{"role": "system", "content": "You are a robotic minion created by Eason in Minions.app Laboratory. You are upbeat and friendly. Your response should be as concise with a sense of humor. You introduce yourself when first saying, Bello! Buddy. If the user asks you for anything information about Minions, or Despicable Me, or Universal Studios,  you will try to use our intelligence to reply. If the user asks you not related Minions, or Despicable Me, or Universal Studios, you will tell them I don't know."}]
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""

# The 'chat_click' function is defined to send the user's message to the AI model 
# and append the response to the conversation history.
def chat_click():
    if st.session_state['user']!= '':
        user_chat_input = st.session_state['user']
        output=generate_response(user_chat_input)
        st.session_state['past'].append(user_chat_input)
        st.session_state['generated'].append(output)
        st.session_state['prompts'].append({"role": "assistant", "content": output})
        st.session_state['user'] = ""

# The user's input is retrieved from the 'user' session state.
user_input=st.text_input("You:", key="user")

# Streamlit to set the page layout and make the chat & new topic button.
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    chat_button=st.button("Send", on_click=chat_click)
with col2:
    new_topic_button=st.button("New Topic", on_click=new_topic_click)

# The 'message' function is defined to display the messages in the conversation history.
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], avatar_style='bottts', key=str(i))
        message(st.session_state['past'][i], is_user=True, avatar_style='thumbs', key=str(i) + '_user')