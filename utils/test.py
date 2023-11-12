from .connexion_breizhibus import Connexion


lignes = Connexion.get_lines()
arret = Connexion.get_stops("Rouge")
id_bus = Connexion.get_bus()
# Connexion.add_bus("BB07", "PB123TD", 20, 3)
# Connexion.update_bus(7, "PB123TY")
# connexion = Connexion.identifier("simplon_22", "CA_Quai_59")
# Connexion.delete_bus(21)


# print(lignes)
# print(arret)
print(id_bus)
# print(connexion)
# if connexion != None
#    url gestion des bus
# else
#    url error

# if not (connexion):
#     print("La liste est vide")
# else:
#     print("La liste est pleine")
# for i in lignes:
#     print(i["id"])
#     print(i["nom"])
