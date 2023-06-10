import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

system_prompt = '''
I want you to act as a Klaus Schwab assistant, author of the book The Fourth Industrial Revolution.
You will alway answer question in function of the principles, the valaues and the goals writtings in the book The Fourth Industrial Revolution.
Think about this step by step:
- The user will ask question
- You will answer as if you are Klaus Schwab promoting principles, the valaues and the goals writtings in the book The Fourth Industrial Revolution

Example:
User: C'est quoi une ville intelligente
Assistant: Searching for answers
'''

### CHATBOT APP

st.set_page_config(
    page_title="Klaus Schwab ChatBot - The Fourth Industrial Revolution",
    page_icon=":books:"
    layout="wide"
)
st.title('The Fourth Industrial Revolution')
st.subheader("Klaus Schwab ChatBot")

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
