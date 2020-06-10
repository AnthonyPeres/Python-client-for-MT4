from Client import Client
from time import sleep

client = Client()

"""
Déroulement d'une boucle : 
    1. On reçoit une valeur sur la pullSocket
    2. On affiche cette valeur (la valeur d'une devise avec son nom etc)
    3. On appelle la fonction de traitement avec cette valeur
    4. On envoie un ordre si besoin
"""

while True:

    # message = client.send_on_req("Salut")
    # print(message)
    # Quand on reçoit une valeur sur la pullSocket
    
    message = client.receive_on_pull()
    print(message)

    # Afficher cette valeur

    # Appeler la fonction de traitement avec cette valeur

    # Envoyer un ordre si besoin