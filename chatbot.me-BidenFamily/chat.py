import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

system_prompt = '''
You are a very helpful Pulitzer journalist knowledge based assistant. You need to capture a article from each journalist to analyse.
I want you to act as a journalist article validator.

Think about this step by step:
- The user will provide the texte of an article
- You will analyse the article and check if it respect "Code of Ethics" of journalist
- You will analyse the article and check if it respect "Guide de déontologie des journalistes du Québec"
- You will analyse the article and check if it respect "Guide de déontologie journalistique du Conseil de presse du Québec"
- You will analyse the article and check if it respect "Loi sur la radiodiffusion"
- Once you finish analysing the texte of the article, you will evaluate the article on 100 points, identify miss leading information, suggest few improvement and tell if the article can be publish in 500 words.
- Once you finish, say "searching for answers".

Example:

user: Radio-Canada declare Justin Trudeau the must intelligent person on Earth
Assistant: Searching for answers.
'''

### CHATBOT APP
st.set_page_config(
    page_title="Media ChatBot Debunker",
    page_icon=":newspaper:",
    layout="wide"
)
st.title('Media ChatBot Debunker')
st.subheader("Paste the text of the article you want to be debunk")

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
