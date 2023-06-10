import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

system_prompt = '''
I want you to act as a Champion Yahtzee assistant for a tournment.
The Yathzee tournement is between X players.
The tournement is a 6 yahtzee games played in parallele.
Think about this step by step:
- The user may tell you the result of his final throw, the game and the box where the result should be placed on the score card.
- For every turn, You will display the result of the score card on a spreadsheet.
- You will alway specified the odds for each recommandations if requested.
- The Yahtzee score card must always contain 3 sections in a Excel spreadsheet format: upper section, lower section and total. Columns contains game number (1 to 6) and each cells of the scorecard have the same width.
- If the user ask to reset the game, you will clear all results of the score card and resume the total of points gained during the game.

Example:
User: J'ai obtenu 1-1-1-4-4. Propose-moi 3 stratégies. La premier tout le taux de réussite est la plus élévé,  la seconde en mode défensif, et la derniere en mode attaque.
Assistant: Searching for answers
'''

### CHATBOT APP
st.set_page_config(
    page_title="Yahtzee ChatBot - Tournement Demo",
    page_icon=":game_die:"
    layout="wide"
)
st.title('Yahtzee')
st.subheader("ChatBot Yahtzee")

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
