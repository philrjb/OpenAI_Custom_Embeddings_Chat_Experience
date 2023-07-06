import os
import re
import io
import chardet
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

repertoire = os.path.normpath('/Users/philipperaymondjb/Documents/GitHub/fine-tune/Biden Laptop emails/biden-laptop-emlxs')

def optimiser_fichier_texte(fichier_entrant, fichier_sortant):
    with open(fichier_entrant, 'rb') as f:
        raw_data = f.read()
    detected_encoding = chardet.detect(raw_data)['encoding']

    try:
        with io.open(fichier_entrant, 'r', encoding=detected_encoding) as f_entree:
            contenu = f_entree.read()
    except UnicodeDecodeError:
        with io.open(fichier_entrant, 'r', encoding='ISO-8859-1') as f_entree:
            contenu = f_entree.read()

    contenu_optimise = optimiser_contenu(contenu)

    with io.open(fichier_sortant, 'w', encoding='utf-8') as f_sortie:
        f_sortie.write(contenu_optimise)

    os.remove(fichier_entrant)

def optimiser_contenu(contenu):
    contenu = remove_html_tags(contenu)
    contenu = remove_stop_words(contenu)

    contenu = re.sub(r'\\n{2,}', '\\\\n', contenu)
    contenu = re.sub(r'\t+', ' ', contenu)
    contenu = re.sub(r' +', ' ', contenu)
    contenu = re.sub(r'\\r+', '', contenu)
    
    return contenu

def remove_html_tags(text):
    clean_text = re.sub('<[^>]*>', '', text)
    return clean_text

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    words = re.findall(r'\b\w+\b', text, re.MULTILINE)
    filtered_text = ' '.join([word for word in words if word.lower() not in stop_words])
    return filtered_text

for fichier in os.listdir(repertoire):
    fichier_entrant = os.path.join(repertoire, fichier)
    if os.path.isfile(fichier_entrant):
        fichier_sortant = os.path.join(repertoire, 'clean_' + fichier)
        optimiser_fichier_texte(fichier_entrant, fichier_sortant)
