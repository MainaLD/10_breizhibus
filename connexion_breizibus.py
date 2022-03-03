from types import ClassMethodDescriptorType
import mysql.connector as msql
from ligne import Ligne
from bus import Bus
from arret_ligne import Arret_ligne

class Connexion:
    # Variables de classe
    # --------------------
    __USER = "breizhibus"
    __PWD = "breizhibus"
    __HOST = "localhost"
    __PORT = "8081"
    __DB = "breizhibus"
    __cursor = None

    # Méthodes de classe
    # -------------------------------------
    # OUVERTURE ET FERMETURE
    # -------------------------------------
    @classmethod
    def open_connexion(cls):
        if cls.__cursor == None:
            cls.__bdd = msql.connect(
                user=cls.__USER,
                password=cls.__PWD,
                host=cls.__HOST,
                port=cls.__PORT,
                database=cls.__DB,
            )
            cls.__cursor = cls.__bdd.cursor()

    @classmethod
    def close_connexion(cls):
        cls.__cursor.close()
        cls.__bdd.close()
        cls.__cursor = None

    # ----------------------------------------------------------------------
    # METHODES
    # ----------------------------------------------------------------------
    @classmethod
    def get_lines(cls):
        """Méthode pour récupérer toutes les lignes"""

        cls.open_connexion()
        query = "SELECT * FROM lignes"
        cls.__cursor.execute(query)
        # lignes = cls.__cursor.fetchall()

        liste_lignes = []
        for enregistrement in cls.__cursor:
            liste_lignes.append(Ligne(enregistrement[0],enregistrement[1]))

        cls.close_connexion()

        return liste_lignes

    @classmethod
    def get_stops(cls, ligne_nom):
        """Méthode pour trouver tous les arrêts d'une ligne ==> retourne une liste de tuple"""
        cls.open_connexion()
        # Vérifier la requête
        query = f"SELECT lignes.nom, arrets.nom, arrets.adresse FROM lignes JOIN arrets_lignes ON lignes.id_ligne = arrets_lignes.id_ligne JOIN arrets ON arrets_lignes.id_arret = arrets.id_arret WHERE lignes.nom = '{ligne_nom}'"
        cls.__cursor.execute(query)
        arret = []
        for arret_lu in cls.__cursor:
            arret.append(Arret_ligne(arret_lu[0], arret_lu[1], arret_lu[2]))
        
        cls.close_connexion()
        return arret

    @classmethod
    def identifier(cls, identifiant_saisi, mdp_saisi):
        """Méthode pour s'identifier"""
        ok = False

        cls.open_connexion()
        query = f"SELECT identifiant, mdp FROM administrateurs WHERE identifiant = '{identifiant_saisi}' AND mdp = '{mdp_saisi}'"
        cls.__cursor.execute(query)
        cls.__cursor.fetchall()
        if cls.__cursor.rowcount > 0:
            ok = True

        cls.close_connexion()

        return ok

    @classmethod
    def lister_bus(cls):
        cls.open_connexion()
        # Vérifier la requête
        query = "SELECT id_bus, numero, immatriculation, nombre_place, bus.id_ligne, lignes.nom FROM bus JOIN lignes ON lignes.id_ligne = bus.id_ligne;"
        cls.__cursor.execute(query)

        list_bus = []
        for bus in cls.__cursor:
            list_bus.append(Bus(bus[0], bus[1], bus[2], bus[3], bus[4], bus[5]))
        
        cls.close_connexion()
        return list_bus    



    @classmethod
    def add_bus(cls, num_saisi, immatriculation_saisi, nb_place_saisi, ligne_saisi):
        """Méthode pour ajouter un bus dans la table bus à partir du numéro, de l'immatriculation, du nombre de place et de la ligne saisi par l'utilisateur"""
        cls.open_connexion()
        query = f"INSERT INTO bus (numero, immatriculation, nombre_place, id_ligne) VALUES ('{num_saisi}', '{immatriculation_saisi}', {nb_place_saisi}, {ligne_saisi})"
        cls.__cursor.execute(query)
        cls.__bdd.commit()
        cls.close_connexion()
        pass

    @classmethod
    def get_bus(cls):
        """Méthode pour récupérer toutes les lignes"""

        cls.open_connexion()
        query = "SELECT id_bus FROM bus ORDER BY id_bus ASC"
        cls.__cursor.execute(query)
        # bus = cls.__cursor.fetchall()

        liste_bus = []
        for enregistrement in cls.__cursor:
            liste_bus.append(enregistrement[0])

        cls.close_connexion()

        return liste_bus
    
    @classmethod
    def update_bus(
        cls,
        id_bus_a_modifier,
        num_saisi,
        immatriculation_saisi,
        nb_place_saisi,
        ligne_saisi,
    ):
        """Méthode pour modifier un bus dans la table bus à partir du numéro, de l'immatriculation, du nombre de place et de la ligne saisi par l'utilisateur"""
        # FAUT-IL DES CONDITIONS EN FONCTION DES CHAMPS SAISIS ?????
        cls.open_connexion()
        query = f"UPDATE bus SET numero = '{num_saisi}', immatriculation = '{immatriculation_saisi}', nombre_place = {nb_place_saisi}, id_ligne = {ligne_saisi} WHERE id_bus = {id_bus_a_modifier}"
        cls.__cursor.execute(query)
        cls.__bdd.commit()
        cls.close_connexion()
        pass

    @classmethod
    def delete_bus(cls, id_bus: int):
        """Méthode pour supprimer un bus dans la table bus à partir de son id"""
        cls.open_connexion()
        query = f"DELETE FROM bus WHERE id_bus = {id_bus}"
        cls.__cursor.execute(query)
        cls.__bdd.commit()
        cls.close_connexion()
        pass
