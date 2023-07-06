import os
import glob
import shutil

input_directory = "/Users/philipperaymondjb/Documents/GitHub/_public/OpenAI_Custom_Embeddings_Chat_Experience/OpenAI_Custom_Embeddings_Chat_Experience/chatbot.me-BidenFamily/_tmp"
output_directory = "/Users/philipperaymondjb/Documents/GitHub/_public/OpenAI_Custom_Embeddings_Chat_Experience/OpenAI_Custom_Embeddings_Chat_Experience/chatbot.me-BidenFamily/_tmp"

# Trouver tous les fichiers .emlx dans le répertoire d'entrée
emlx_files = glob.glob(os.path.join(input_directory, "*.emlx"))

for emlx_file in emlx_files:
    # Créer un nouveau nom de fichier avec l'extension .txt
    txt_file = os.path.splitext(emlx_file)[0] + ".txt"
    txt_file = os.path.join(output_directory, os.path.basename(txt_file))

    # Copier le contenu du fichier .emlx au fichier .txt
    shutil.copy2(emlx_file, txt_file)

    # Supprimer le fichier d'origine .emlx
    os.remove(emlx_file)

    print(f"{emlx_file} converti en {txt_file}")


#Assurez-vous de remplacer /chemin/du/dossier/source/ et /chemin/du/dossier/destination/ par les chemins de votre choix. Le code ci-dessus trouvera tous les fichiers .emlx dans le répertoire d'entrée, créera des fichiers .txt correspondants dans le répertoire de sortie en copiant leur contenu, puis supprimera les fichiers .emlx d'origine.