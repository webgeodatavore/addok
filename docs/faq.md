# Foire aux questions (FAQ)

## Est-ce que je peux effectuer une recherche sur plusieurs valeurs pour un filtre donné?

Par exemple: /?type=street&type=housenumber

Addok s'appuye sur l'opération intersect de Redis qui joint seulement les
termes avec "AND" et ne sait pas ce qu'est "OR".

Il serait trop coûteux de faire plusieurs passes pour chaque terme OR.


## Est-ce que la position  est pertinente dans la chaîne en entrée?

Par exemple: "33 bd Bordeaux Troyes" vs. "bd de Troyes 33 Bordeaux"

Réponse rapide: Non. Tous les pays n'utilisent pas le même ordre pour les
adresses. Même dans un pays, nous pouvons avoir certaines subtilités comme
l'illustre l'exemple ci-dessus.


## Pourquoi j'ai des résultats inconsistants avec les abbréviations?

Par exemple: Je cherche en utilisant "BD République" et "Rue République"
arrive avant "Boulevard République" dans les résultats.

Addok ne résout les abréviations que pour la recherche mais jamais pour le
scoring. C'est parce que lors de la recherche, il essaie de faire de son mieux
pour deviner ce que l'utilisateur recherche vraiment. Au moment du scoring et
par conception, nous gardons seulement l'entrée originale pour être sûr que
nos suppositions ne sont pas trop magiques et trop éloignées de la réalité.
