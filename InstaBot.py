import instaloader
import json
import lzma
import os
from pprint import pprint 

##################################### Creer un compte Bot et entrer l'identifiant et mdp  #####################################
USERNAME = "identifiant"
MDP = "Mdp******"

setProfile = set()

bot = instaloader.Instaloader()
bot.login(USERNAME, MDP)

##################################### Choisir le ou les comptes à recuperer  #####################################
ACCOUNTS = ['compte1', 'compte2']

##################################### Pour chaques compte ajouter dans le tableau récupérer les donnee du profile et le met dans le set  #####################################

for profileAccount in ACCOUNTS:
    profile = instaloader.Profile.from_username(bot.context, profileAccount)
    setProfile.add(profile)



############### Télécharger tout des comptes mis dans le set ############### 
bot.download_profiles(setProfile, profile_pic=False, posts=True, tagged=False, igtv=False, highlights=False, stories=True, fast_update=False, post_filter=None, storyitem_filter=None, raise_errors=False, latest_stamps=None)


##################################### Extraction en JSON des .XZ #####################################
# with lzma.open('./nomducompte/2023-01-20_10-22-47_UTC.json.xz', 'rb') as f:
#     file_content = f.read()
#     data = json.loads(file_content)
#     w = open(f'./nomducompte/2023-01-20_10-22-47_UTC.json', mode="w")
#     w.write(json.dumps(data))




# Boucler sur tt les fichiers existants des document downloads pour chaques comptes / les extraire en json / les ajouter dans un objet au nom du compte / L'ajouter lui meme a un object a envoyer dans un fichier json pour l'utiliser en js par la suite 
path = './'
allEntries = os.scandir(path)
name_files = {}
for entry in allEntries:

    if entry.is_dir():
        name_files[entry.name] = {}
        name_files[entry.name]['all'] = []
        name_files[entry.name]['dataPost'] = []
        name_files[entry.name]['dataAccount'] = []

        entriesIn = os.scandir(entry.name)

        for entryIn in entriesIn:
            name_files[entry.name]['all'].append(entryIn.name)

            if entryIn.is_file() and entryIn.name.endswith('.xz'):
                
                with lzma.open(f'./{entry.name}/{entryIn.name}', 'rb') as f:
                    file_content = f.read()
                    data = json.loads(file_content)
                    parts = entryIn.name.split(".")

                    nameFileWithoutJSONXZ =  parts[0]
                    if nameFileWithoutJSONXZ.find('UTC') == -1:
                        name_files[entry.name]['dataAccount'].append(nameFileWithoutJSONXZ)
                    else:
                        name_files[entry.name]['dataPost'].append(nameFileWithoutJSONXZ)

                    nameFileWithoutXZ = ".".join([parts[0], parts[1]])

                    w = open(f'./{entry.name}/{nameFileWithoutXZ}', mode="w")
                    w.write(json.dumps(data))
               
# pprint(name_files)