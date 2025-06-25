import requests

# Ils ont changé cette année

r_1 = requests.post("https://resultats.gouv.tg/api/examens/generate-url/bac1",
                    json={"num_table": 10, "type_enseignement": "GENERAL"})
print(r_1.text)
# Maintenant, ce n'est plus direct
# Ils vont donner un nouveau lien pour récuperer
# les résultats
lien_1 = r_1.json()


# Récupération des résultats
r_2 = requests.get(
    f"https://resultats.gouv.tg/api/examens/bac1/{lien_1["url"]}")
print(r_2.text)
# Si ce n'est pas vide
if r_2.json():
    print(r_2.json())
# Sinon
else:
    print("Vide")


# Maintenant, on peut faire une boucle de 10000 à 20000
# Même logique
for numero in range(10000, 20000):
    r_1 = requests.post("https://resultats.gouv.tg/api/examens/generate-url/bac1",
                        json={"num_table": numero, "type_enseignement": "GENERAL"})
    print(r_1.text)
    lien_1 = r_1.json()
    r_2 = requests.get(
        f"https://resultats.gouv.tg/api/examens/bac1/{lien_1["url"]}")
    print(r_2.text)
    # Si ce n'est pas vide
    if r_2.json():
        print(r_2.json())
    # Sinon
    else:
        print("Vide")
