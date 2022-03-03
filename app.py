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
    list_bus = Connexion.nommer_bus(ligne_nom)
    print(list_arrets)
    return render_template("arrets.html", afficher_arrets=list_arrets, afficher_bus=list_bus)


@app.route("/identification")
def identifier():
    return render_template("form_identifier.html")

# ["POST", "GET"] => pour revenir sur la page sans repasser par le mdp
@app.route("/autorisation", methods=["POST"])
def autoriser():
    identifiant = request.values.get("user_identifiant")
    mdp = request.values.get("user_mdp")
    oui = Connexion.identifier(identifiant, mdp)
    return render_template("identifier.html", reponse=oui, qui=identifiant)


@app.route("/autorisation/ajouter")
def ajouter_bus():
    return render_template("form_bus_add.html")


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
    liste_bus = Connexion.get_bus()
    return render_template("form_bus_update.html", list_id_bus=liste_bus)


@app.route("/autorisation/modification", methods=["POST"])
def modification():
    id_bus = request.values.get("id_bus_saisi")
    numero = request.values.get("bus_num")
    immatriculation = request.values.get("bus_immatriculation")
    nb_place = request.values.get("bus_nb_place")
    id_ligne = request.values.get("id_ligne")
    Connexion.update_bus(id_bus, numero, immatriculation, nb_place, id_ligne)
    return render_template("modification.html", num=numero)


@app.route("/autorisation/supprimer")
def supprimer_bus():
    liste_bus = Connexion.get_bus()
    return render_template("form_bus_delete.html", list_id_bus=liste_bus)


@app.route("/autorisation/suppression", methods=["POST"])
def suppression():
    id_bus = request.values.get("id_bus_saisi")
    Connexion.delete_bus(id_bus)
    return render_template("suppression.html", id_bus=id_bus)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
