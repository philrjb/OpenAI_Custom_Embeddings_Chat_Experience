import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

system_prompt = '''
I want you to act as a Highly knowledge french teacher assistant. You will looking for typo writing, grammar and conjugation error and you will make recommendation on how to improve.
Think about this step by step:
- Search for writting errors.
- Alway correct error.

Example:
User: Does this sentance contain errors : J'aime la vie.
Assistant: Searching for answers
'''

### CHATBOT APP

st.set_page_config(
    page_title="Grammaire et conjugaison ChatBot - Langue Francaise",
    page_icon=":fr:"
    layout="wide"
)

st.title('Grammaire et conjugaison')
st.subheader("ChatBot Grammaire et conjugaison FR")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input("Les bonnes questions font les bonnes réponses !!!","", key="input")

if st.button('Submit', key='generationSubmit'):

    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant()
        messages = []
        system_message = Message('system',system_prompt)
        messages.append(system_message.message())
    else:
        messages = []


    user_message = Message('user',prompt)
    messages.append(user_message.message())

    response = query(messages)

    # Debugging step to print the whole response
    #st.write(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['content'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
