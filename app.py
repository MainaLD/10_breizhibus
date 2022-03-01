from flask import Flask, render_template, request
from connexion_breizibus import Connexion


app = Flask(__name__)


@app.route("/")
def afficher_lignes():
    lignes = Connexion.get_lines()
    return render_template("index.html", list_lignes=lignes)


# /<int:id_ligne>
@app.route("/arrets", methods=["POST"])
def afficher_arrets():
    ligne_nom = request.values.get("ligne_saisi")
    print(ligne_nom)
    list_arrets = Connexion.get_stops(ligne_nom)
    print(list_arrets)
    return render_template("arrets.html", afficher_arrets=list_arrets)


@app.route("/identification")
def identifier():
    return render_template("form_identifier.html")


@app.route("/autorisation", methods=["POST"])
def autoriser():
    identifiant = request.values.get("user_identifiant")
    mdp = request.values.get("user_mdp")
    oui = Connexion.identifier(identifiant, mdp)
    return render_template("identifier.html", reponse=oui, qui=identifiant)


@app.route("/autorisation/ajouter")
def ajouter_bus():
    return render_template("form_bus.html")


@app.route("/autorisation/ajout", methods=["POST"])
def ajout():
    numero = request.values.get("bus_num")
    immatriculation = request.values.get("bus_immatriculation")
    nb_place = request.values.get("bus_nb_place")
    id_ligne = request.values.get("id_ligne")
    Connexion.add_bus(numero, immatriculation, nb_place, id_ligne)
    return render_template("ajout.html", num=numero)


@app.route("/autorisation/modifier")
def modifier_bus():
    return render_template("form_bus.html")


# @app.route("/autorisation/modification", methods=["GET"])
# def modification():
#     numero = request.values.get("bus_num")
#     immatriculation = request.values.get("bus_immatriculation")
#     nb_place = request.values.get("bus_nb_place")
#     id_ligne = request.values.get("id_ligne")
#     return render_template("ajout.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
