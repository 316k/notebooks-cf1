#!/usr/bin/env python

import json
import os
from glob import glob
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

"""
Convention:

A) La première ligne commence par:
    #@title Exercice.+

B) Toutes les lignes sont conservées jusqu'à la première ligne qui contient seulement des ######:

    #####

C) Les commentaires qui commencent par des ### sont conservés et
suivis d'une ligne vide

D) On peut garder un footer à la fin pour fournir des tests avec

    ### tests

    3x # ou plus

"""


def cleanup(code: list):
    # La première ligne reste
    header = code[0]
    
    output = [
        header,
    ]

    code = code[1:]

    # On garde tout le début jusqu'à un séparateur "####..."
    begin = [
        i
        for i, ligne in enumerate(code)
        if re.match(r'^#{2,}$', ligne)
    ]

    if begin:
        idx = begin[0] + 1
        output.extend(code[:idx])
        output.append('')
        code = code[idx:]

    # On extrait tout de suite les cas de tests à la fin
    end = [
        i
        for i, ligne in enumerate(code)
        if re.match(r'^#{3,} tests?$', ligne, flags=re.IGNORECASE)
    ]

    footer = ['']
    if end:
        idx = end[-1]
        footer = [''] + code[idx:]
        code = code[:idx]

    # Garde les blocs de commentaires où chaque ligne commence par ###
    # en mettant un espace à la fin du bloc
    keep_only = [
        (i, line)
        for i, line in enumerate(code)
        if line.startswith('###')
    ]

    keep_only_with_space = []
    for i, (idx, line) in enumerate(keep_only):

        if i > 0:
            prev_num = keep_only[i-1][0]
            diff = idx - prev_num
            if diff > 1:
                keep_only_with_space.append("")
        
        keep_only_with_space.append(line)


    output.extend(keep_only_with_space)

    output.extend(footer)
    
    if output[-1] != '':
        output.append('')

    # Vérifie que toutes les lignes terminent déjà par "\n"
    for i in range(len(output)):
        
        if len(output[i]) == 0 or output[i][-1] != '\n':
            output[i] += "\n"

    return output

for i in glob('./solutions/*.ipynb'):
    output_path = re.sub(r'^./solutions/', './exercices/', i)

    with open(i) as f:
        print("===", i, "===")
        content = json.load(f)
        cells = content['cells']

        for i, cell in enumerate(cells):

            if cell['cell_type'] != "code":
                continue

            if len(cell['source']) and cell['source'][0].lower().startswith('#@title exercice'):
                src = cell['source']
                src = cleanup(src)
                content['cells'][i]['source'] = src
                content['cells'][i]['execution_count'] = None
                content['cells'][i]['outputs'] = []

    with open(output_path, 'w') as f:
        json.dump(content, f)

exemple1 = """
#@title Exercice 3.2
notes = [
    [1, 2, 3],
    [4, 5, 6],
]
#####

### Calculez la variance avec la formule donnée puis affichez-la

### Comparez votre formule avec la version calculée par numpy: arr.var()

### Calculez l'écart-type




""".strip().split('\n')

exemple2 = """
#@title Exercice 1.5
def distance(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

print(distance(p1, p2))
print(distance(p1, p1))
""".strip().split('\n')

exemple3 = """
#@title Exercice 1
notes = [
    22.44, 35.95, 36.97, 37.79, 34.71, 20.94, 30.28, 31.53, 24.04,
    40.  , 13.45, 20.02, 30.05, 30.55, 27.04, 22.22, 29.28, 29.07,
    39.  , 39.76, 24.  , 38.  , 40.  , 23.86, 25.04, 40.  , 32.65,
    38.55
]
#####

### Convertissez la liste en tableau numpy
notes = np.array(notes)

### Quelle est la taille du groupe? Affichez combien il y a de notes dans le tableau
print("Taille = ", len(notes))

### Affichez la différence entre la note maximale et la note minimale
### On notera aussi une autre affaire
print("Différence entre min et max:", notes.max() - notes.min())

### Donnez +1 point bonus à tout le monde
notes = notes + 1
# autre solution qui marche: notes += 1

### Après la dernière étape, la première note devrait donc monter à 23.44, vérifiez ça.
assert notes[0] == 23.44 # Rappel: assert pour vérifier quelque chose
print(notes[0])

### Modifiez les notes pour avoir l'équivalent en pourcents plutôt que sur 40, et affichez le résultat
notes = notes / 40 * 100
print("Notes sur 100:", notes)

### Trouvez la moyenne des notes en pourcents. Utilisez la méthode arr.mean()
### On notera également une autre affaire
print("Moyenne sur 100:", notes.mean())
""".strip().split('\n')

exemple4 = """
#@title Exercice 4

def moyenne_tronquee(array, P):
  # On trie les données
  array = np.sort(array)

  nb_elements_a_enlever_par_cote = len(array) * P/100

  # Important : on ne veut pas finir avec un nombre à virgule ici
  nb_elements_a_enlever_par_cote = round(nb_elements_a_enlever_par_cote)

  # On exclut les premiers et les derniers
  centre_array = array[nb_elements_a_enlever_par_cote : -nb_elements_a_enlever_par_cote]

  # Si le pourcentage spécifié enlève tous les éléments, on peut déclencher une erreur
  assert len(centre_array) > 0

  return centre_array.mean()

### tests
# Quelques cas de test
assert round(moyenne_tronquee(np.array([10, 20, 30]), 33.3)) == 20

assert round(moyenne_tronquee(np.array([60.17, 87.15, 99.87, 14.21, 9999]), 20.0)) == 82

assert round(moyenne_tronquee(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), 10.0), 1) == 4.5
assert round(moyenne_tronquee(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), 20.0), 1) == 4.5
assert round(moyenne_tronquee(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), 30.0), 1) == 4.5
assert round(moyenne_tronquee(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), 40.0), 1) == 4.5

assert round(moyenne_tronquee(np.array([1,2,3,2,1,2,3,3,2,1,2,1,3, -9999, +9999]), 20.0), 2) == 2.0
assert round(moyenne_tronquee(np.array([1,2,3,2,1,2,3,3,2,1,2,1,3, -9999, +9999]), 6.666), 2) == 2.0
""".strip().split('\n')

exemple5 = """
#@title Exercice 11

# Complétez les méthodes suivantes:
def changer_clarete(image, quantite):
  return image # TODO: changer ça

def quantification_image(image, n):
  return image # TODO: changer ça

def ajouter_bruit(image):
  return image # TODO: changer ça

#####################

# Solutions


def changer_clarete(image, quantite):
  return np.pow(image, 1/quantite)
  # Équivalent: return image**(1/quantite)

def quantification_image(image, n):
  return np.round(image * n) / n


def ajouter_bruit(image):
  image = image + np.random.random(image.shape)
  image[image > 1] = 1
  image[image < 0] = 0
  return image


### tests
imshow(changer_clarete(image_test, 5), "Image plus claire")
imshow(changer_clarete(image_test, 0.5), "Image plus foncée")

imshow(quantification_image(image_test, 3), "Image quantifiée entre 0 et 3")

imshow(ajouter_bruit(image_test), "Image bruitée")
""".strip().split('\n')


exemple6 = """
#@title Exercice 12
image_toki_pona = charger_image("https://raw.githubusercontent.com/316k/misc-data/refs/heads/main/images/toki-pona.png")
imshow(image_toki_pona, "Image visée")
image_toki_pona = None

# Utilisez seulement ces 4 prochaines images
image_ijo = charger_image("https://raw.githubusercontent.com/316k/misc-data/refs/heads/main/images/ijo.png")
image_luka = charger_image("https://raw.githubusercontent.com/316k/misc-data/refs/heads/main/images/luka.png")
image_pana = charger_image("https://raw.githubusercontent.com/316k/misc-data/refs/heads/main/images/pana.png")
image_pona = charger_image("https://raw.githubusercontent.com/316k/misc-data/refs/heads/main/images/pona.png")

##################

#### Utilisez des additions et soustractions pour arriver au même résultat que la 5e image
lignes_verticales = image_pana - image_luka

image_reconstruite = image_ijo + lignes_verticales + image_pona

imshow(image_reconstruite, "Image reconstruite")
""".strip().split('\n')

exemple7 = """
#@title Exercice 14

def valider_carre_magique(carre):
  # TODO : Coder la fonction
  return "TODO : CODER LA FONCTION"

######

# Solution :
def valider_carre_magique(carre):
  # Vérifiez que c'est bien un carré : largeur = hauteur
  est_carre = carre.shape[0] == carre.shape[1]

  # Calculez la somme des lignes
  somme_chaque_ligne = carre.sum(axis=0)
  somme_chaque_colonne = carre.sum(axis=1)

  diago1 = carre * np.identity(carre.shape[0])
  # Flip chaque ligne de l'identité
  diago2 = carre * np.flip(np.identity(carre.shape[0]), axis=0)

  valeur_magique = somme_chaque_ligne[0]

  return (
      est_carre and
      np.all(somme_chaque_ligne == valeur_magique) and
      np.all(somme_chaque_colonne == valeur_magique) and
      diago1.sum() == valeur_magique and
      diago2.sum() == valeur_magique
  )
""".strip().split('\n')


exemple8 = """
#@title Exercice 1
notes = [
    22.44, 35.95, 36.97, 37.79, 34.71, 20.94, 30.28, 31.53, 24.04,
    40.  , 13.45, 20.02, 30.05, 30.55, 27.04, 22.22, 29.28, 29.07,
    39.  , 39.76, 24.  , 38.  , 40.  , 23.86, 25.04, 40.  , 32.65,
    38.55
]
#####

### Convertissez la liste en tableau numpy
notes = np.array(notes)

### Quelle est la taille du groupe? Affichez combien il y a de notes dans le tableau
print("Taille = ", len(notes))

### Affichez la différence entre la note maximale et la note minimale
print("Différence entre min et max:", notes.max() - notes.min())

### Calculez la moyenne des notes avec la formule : (somme de tous les éléments)/taille
print("Moyenne sur 40: ", notes.sum() / len(notes))

### Donnez +1 point bonus à tout le monde
notes = notes + 1
# autre solution qui marche: notes += 1

### Après la dernière étape, la première note devrait donc monter à 23.44, vérifiez ça.
assert notes[0] == 23.44 # Rappel: assert pour vérifier quelque chose
print(notes[0])

### Modifiez les notes pour avoir l'équivalent en pourcents plutôt que sur 40, et affichez le résultat
notes = notes / 40 * 100
print("Notes sur 100:", notes)

### Arrondissez les notes à 2 décimales et affichez-les
notes = np.round(notes, 2)
print("Notes arrondies:", notes)

### Vérifiez que la dernière note est bien de 98.87
assert notes[-1] == 98.87

### Trouvez la moyenne des notes en pourcents. Utilisez la méthode arr.mean()
print("Moyenne sur 100:", notes.mean())
""".strip().split('\n')


# print("\n" * 10)
# print("=" * 60)
# print("".join(cleanup(exemple8)))
