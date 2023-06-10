import streamlit as st
import openai
import os

from config import INDEX_NAME, MAX_TOKENS, COMPLETIONS_MODEL, EMBEDDINGS_MODEL, CHAT_MODEL, TEXT_EMBEDDING_CHUNK_SIZE, PREFIX, TEMPERATURE, TOP_K

from streamlit_chat import message
from database import get_redis_connection, get_redis_results
from chatbot import RetrievalAssistant, Message


def init_app():
    st.set_page_config(page_title="Grammaire et conjugaison ChatBot - Langue Francaise", page_icon=":fr:", layout="wide")
    st.title('Grammaire et conjugaison')
    st.subheader("ChatBot Grammaire et conjugaison FR")


def query_chatbot(chat, question):
    assistant_response = chat.ask_assistant(question)
    return assistant_response['choices'][0]['content']


def search_documents(client, prompt):
    return get_redis_results(client, prompt, INDEX_NAME)


def get_summary(prompt, search_result):
    summary_prompt = '''Summarise this result in a bulleted list to answer the search query a user has sent.
    Search query: SEARCH_QUERY_HERE
    Search result: SEARCH_RESULT_HERE
    Summary:
    '''
    summary_prepped = summary_prompt.replace('SEARCH_QUERY_HERE', prompt).replace('SEARCH_RESULT_HERE', search_result)
    summary = openai.Completion.create(engine=COMPLETIONS_MODEL, prompt=summary_prepped, max_tokens=MAX_TOKENS)
    return summary['choices'][0]['text']

init_app()

app_mode = st.sidebar.selectbox("Veuillez choisir votre mode d'interaction", ["Chatbot", "Searchbot", "NotePad", "Upload file", "Voice", "Configuration", "Mode d'emploi"])

if app_mode == "Chatbot":
    system_prompt = '''
I want you to act as a Highly knowledge french teacher assistant. You will looking for typo writing, grammar and conjugation error and you will make recommendation on how to improve.
Think about this step by step:
- Search for writting errors.
- Alway correct error.

Example:
User: Does this sentance contain errors : J'aime la vie.
Assistant: Searching for answers
'''
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    st.write("IMPORTANT: La présence de la chaîne de caractères 'searching for answers' sous cette forme exacte indique que le Bot est en mode personnalisé.\
                        Vérifier la valeur du paramètre certainty en mode SearchBot pour améliorer votre question")


    prompt = st.text_input("Les bonnes questions font les bonnes réponses !!!", "", key="inputChatbot")

    if st.button('Submit to Chatbot', key='generationSubmitChatBot'):
        if 'chat' not in st.session_state:
            st.session_state['chat'] = RetrievalAssistant()
            messages = [Message('system', system_prompt).message()]
        else:
            messages = []
        messages.append(Message('user', prompt).message())
        response = st.session_state['chat'].ask_assistant(messages)
        st.session_state.past.append(prompt)
        st.session_state.generated.append(response['content'])

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

elif app_mode == "Searchbot":
    st.write("IMPORTANT: Le résultat de la recherche doit avoir une valeur de certainty > 0.135595798492 pour fonctionner avec GPT-4")
    prompt = st.text_input("Les bonnes questions font les bonnes réponses !!!", "", key="inputSearchbot")

    
    if st.button('Submit to Searchbot', key='generationSubmitSearchBot'):
        redis_client = get_redis_connection()
        result_df = search_documents(redis_client, prompt)
        summary_text = get_summary(prompt, result_df['result'][0])
        st.write(summary_text)
        st.table(result_df)

elif app_mode == "NotePad":
    def save_file(content, filename):
        data_directory = 'data'
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        with open(os.path.join(data_directory, filename), "w") as f:
           f.write(content)

    user_input = st.text_area("Entrez vos notes", "Notes personnelles. En date du DD MM 2023. < contexte >, < texte >.")
    file_name = st.text_input("Entrez le nom du fichier pour enregistrer la note (avec l'extension .txt)", "contexte.txt")

    if st.button("Enregistrer"):
        save_file(user_input, file_name)
        st.success(f"Fichier '{file_name}' enregistré dans le dossier 'data' du répertoire du projet")

elif app_mode == "Upload file":
    
    st.write( """La fonction transformer.py n'est pas encore intégrer au code de cette page""" )
    def save_uploaded_file(uploaded_file, destination):
        with open(os.path.join("data", destination), "wb") as f:
            f.write(uploaded_file.getbuffer())
    uploaded_file = st.file_uploader("Choisir un fichier", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file, uploaded_file.name)
        st.success(f"Fichier {uploaded_file.name} enregistré dans 'data/' avec succès")

elif app_mode == "Voice":
    
    st.write( """ Comming soon. Conversion voix vers fichier texte """ )

elif app_mode == "Configuration":
    
    st.write( """ Configuration actuelle """ )

    st.write(f"INDEX_NAME: {INDEX_NAME}")
    st.write(f"MAX_TOKENS: {MAX_TOKENS}")
    st.write(f"COMPLETIONS_MODEL: {COMPLETIONS_MODEL}")
    st.write(f"EMBEDDINGS_MODEL: {EMBEDDINGS_MODEL}")
    st.write(f"CHAT_MODEL: {CHAT_MODEL}")
    st.write(f"TEXT_EMBEDDING_CHUNK_SIZE: {TEXT_EMBEDDING_CHUNK_SIZE}")
    st.write(f"TEMPERATURE: {TEMPERATURE}")
    st.write(f"MAX_TOKENS: {MAX_TOKENS}")
    st.write(f"TOP_K: {TOP_K}")

elif app_mode == "Mode d'emploi":
    
    st.write( """ 
    \n1. Utilisez la liste déroulante à gauche pour choisir un mode d'interaction. 
    \n2. Le mode Chatbot permet d'interagir avec un chatbot intelligent pour obtenir des réponses basées sur la thématique. 
    \n3. Le mode Searchbot recherche des documents / notes pour répondre à votre question. 
    \n4. Le mode OpenAI traite les questions et utilise OpenAI pour générer des réponses. 
    \n5. Posez vos questions dans le champ de saisie prévu à cet effet et cliquez sur soumettre pour obtenir une réponse. 
    \n
    * How to work with large language models: https://github.com/openai/openai-cookbook/blob/970d8261fbf6206718fe205e88e37f4745f9cf76/how_to_work_with_large_language_models.md
    * Techniques to improve reliability : https://github.com/openai/openai-cookbook/blob/970d8261fbf6206718fe205e88e37f4745f9cf76/techniques_to_improve_reliability.md
    * Pour utiliser #ChatGPT Public: https://chat.openai.com/
    * Pour utiliser DALL-E: https://labs.openai.com/
    * Pour utiliser le playground OpenAI : https://platform.openai.com/playground?mode=chat&model=gpt-4
    * ChatGPT — Release Notes : https://help.openai.com/en/articles/6825453-chatgpt-release-notes
    * Billings : https://platform.openai.com/account/usage
    + Current version : ChatGPT May 24 Version
    
    
    """ )
