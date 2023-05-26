from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

def User_login(user):
    with open('df_commentaire.csv', 'r', newline='') as fichier_csv:
        reader = csv.reader(fichier_csv)
        premiere_ligne = next(reader)  
        if user in premiere_ligne:
            return True
        else:
            return False

def obtenir_hotels_commentes(utilisateur):
    numero_colonne = None
    hotels_commentes = []

    with open('df_commentaire.csv', 'r', newline='') as fichier_csv:
        reader = csv.reader(fichier_csv)
        premiere_ligne = next(reader)  # Lire la première ligne du fichier CSV

        if utilisateur in premiere_ligne:
            numero_colonne = premiere_ligne.index(utilisateur)  # Trouver le numéro de colonne pour l'utilisateur

        if numero_colonne is not None:
            for ligne in reader:
                if len(ligne) > numero_colonne:
                    commentaire = ligne[numero_colonne].strip()
                    if commentaire:  # Vérifier si le commentaire n'est pas vide
                        hotel = ligne[0]  # Récupérer le nom de l'hôtel dans la première colonne
                        hotels_commentes.append(hotel)

    return hotels_commentes

def obtenir_commentaires(utilisateur):
    numero_colonne = None
    commentaires = {}

    with open('df_commentaire.csv', 'r', newline='') as fichier_csv:
        reader = csv.reader(fichier_csv)
        premiere_ligne = next(reader)  # Lire la première ligne du fichier CSV

        if utilisateur in premiere_ligne:
            numero_colonne = premiere_ligne.index(utilisateur)  # Trouver le numéro de colonne pour l'utilisateur

        if numero_colonne is not None:
            for ligne in reader:
                if len(ligne) > numero_colonne:
                    commentaire = ligne[numero_colonne].strip()
                    if commentaire:  # Vérifier si le commentaire n'est pas vide
                        hotel = ligne[0]  # Récupérer le nom de l'hôtel dans la première colonne
                        commentaires[hotel] = commentaire

    return commentaires


def obtenir_hotels_non_commentes(utilisateur):
    hotels_commentes = obtenir_hotels_commentes(utilisateur)  # Obtient les hôtels commentés par l'utilisateur
    hotels_tous = obtenir_tous_les_hotels()  # Obtient tous les hôtels disponibles
    
    hotels_non_commentes = [hotel for hotel in hotels_tous if hotel not in hotels_commentes]
    
    return hotels_non_commentes

def obtenir_tous_les_hotels():
    hotels = []

    with open('df_commentaire.csv', 'r', newline='') as fichier_csv:
        reader = csv.reader(fichier_csv)
        next(reader)  
        for ligne in reader:
            hotel = ligne[0] 
            hotels.append(hotel)

    return hotels



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if User_login(username):
        return redirect('/recommandation?username={}'.format(username))
    else:
        return redirect('/log_echec')

@app.route('/recommandation')
def page_log():
    username = request.args.get('username')
    hotels_commentes = obtenir_hotels_commentes(username)

    hotel_selectionne = request.args.get('hotel')
    commentaires = obtenir_commentaires(username)
    commentaire = commentaires.get(hotel_selectionne, "") if hotel_selectionne else ""

    return render_template('recommandation.html', username=username, hotels_commentes=hotels_commentes, commentaire=commentaire, commentaires=commentaires, hotel_selectionne=hotel_selectionne)


@app.route('/log_echec')
def page_echec():
    return render_template('log_echec.html')

@app.route('/ajouter-commentaire')
def page_new_comment():
    username = request.args.get('username')
    hotels_non_commentes = obtenir_hotels_non_commentes(username)
    return render_template('new_comment.html', hotels_non_commentes=hotels_non_commentes)

if __name__ == '__main__':
    app.run(debug=True)