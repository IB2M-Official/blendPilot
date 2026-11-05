# Instructions et Règles Permanentes : blendPilot (Impression 3D via Blender MCP)

Ce fichier définit les standards techniques et la méthodologie systématique pour toute tâche de modélisation 3D destinée à la fabrication additive (FDM / Résine). Le niveau attendu est celui d'une **pièce technique propre, pas d'un prototype**.

---

## 💎 Standards de Qualité (Obligatoires pour toute modélisation)

### 1. Précision et dimensions
- **Aucune dimension n’est inventée** : chaque produit ou pièce dispose obligatoirement d'un fichier de spécification `specs/<modele>_dimensions.md` indiquant la source précise (fiche constructeur officielle, datasheet, relevé physique mesuré par l'utilisateur au pied à coulisse) et la date de relevé.
- **Blocage en cas de doute** : si la source est absente ou incertaine, s'arrêter immédiatement et demander les valeurs à l'utilisateur avant d'écrire la moindre ligne de code.
- **Paramètres déclarés et sourcés** : toute cote utilisée dans le script est déclarée sous forme de constante / paramètre nommé en tête de script, avec son unité ($mm$) et sa source exacte en commentaire.
- **Tolérances d'exécution** :
  - Tolérance dimensionnelle globale : $\pm 0,1\text{ mm}$ sur la bounding box.
  - Tolérance d'ajustement : $\pm 0,05\text{ mm}$ sur les découpes critiques et alésages.

### 2. Forme et esthétique
- **Profils 2D réalistes** : pas de cube ni de cylindre brut comme base. Le contour externe est tracé en 2D (rectangle à coins arrondis, profil composé ou spline/courbe) puis extrudé, avec un rayon de congé cohérent avec le produit réel.
- **Arrondis propres et lisses** : chanfreins / biseaux (`bevel`) avec un nombre de segments suffisant (minimum 3 à 5 segments sur les congés visibles) pour éliminer toute facette apparente.
- **Régularité des lignes de construction** : mêmes rayons appliqués sur toutes les arêtes fonctionnellement équivalentes. Symétries scrupuleusement respectées lorsque le produit physique l'est.
- **Finitions des arêtes** : chanfreins ou congés sur les bords de chaque découpe pour supprimer les arêtes vives et faciliter l'impression 3D.

### 3. Construction technique
- **Méthode de conception volumique** :
  1. Génération du corps plein extérieur extrudé.
  2. Évidement interne par offset ou soustraction booléenne d'un noyau.
  3. Découpes booléennes des ouvertures, perçages et passages.
  4. Jamais de « trous » ou d'éléments simplement superposés ou posés en surface sans fusion booléenne étanche.
- **Application totale des modificateurs** : tous les modificateurs (Booléens, Bevel, Solidify, etc.) doivent être formellement appliqués avant l'export STL. Aucun modificateur non appliqué ne doit subsister dans le fichier final.
- **Repère de découpe rigoureux** : les découpes doivent être positionnées à partir d'un repère d'origine clairement défini dans la fiche de spec (origine monde, axes, face d'appui de référence), jamais estimées « à l'œil ».
- **Fidélité au produit réel** : ne créer une découpe ou un dégagement que si l'élément existe formellement sur le produit réel.

### 4. Adaptation à l'impression 3D
- **Épaisseurs minimales de parois** :
  - $\ge 1,2\text{ mm}$ pour le TPU (flexibilité maîtrisée et étanchéité des passes).
  - $\ge 1,5\text{ mm}$ pour le PLA / PETG (rigidité mécanique et tenue dimensionnelle).
- **Surplombs** : angles de porte-à-faux $\le 45^\circ$ par rapport à la verticale, ou supports explicitement prévus et orientés.
- **Plateau d'impression** : face d'appui plane positionnée en $Z = 0$, pièce centrée en $(X=0, Y=0)$. L'orientation recommandée pour l'impression doit être stipulée dans la spec.
- **Jeu d'ajustement mécanique** : le jeu fonctionnel (clearance) est toujours paramétré (entre $0,3\text{ mm}$ et $0,5\text{ mm}$ selon le matériau et le type d'emboîtement), jamais codé en dur (« hardcodé ») dans la géométrie.

### 5. Contrôles obligatoires avant présentation
- Avant de présenter le résultat à l'utilisateur, mesurer par code Python dans Blender :
  - **Bounding box** réelle ($X \times Y \times Z$).
  - **Volume** de matière estimé ($mm^3$ et $cm^3$).
  - **Épaisseur minimale** de paroi mesurée.
  - **Zéro arête non-manifold**.
  - **Zéro arête ouverte** (boundary edge / trou dans le maillage).
- **Rendus visuels de contrôle multi-angles** : générer systématiquement dans `out/` :
  - Vue de dessus (`_top.png`)
  - Vue de dessous (`_bottom.png`)
  - Vue de profil (`_side.png` ou perspective isométrique)
  - Vue en coupe (`_section.png`) si la pièce comporte une cavité ou un volume intérieur creux.
- **Auto-correction obligatoire** : si un contrôle échoue (paroi trop fine, arête ouverte, volume incorrect), **corriger le script et ré-exécuter le modèle avant d'afficher la réponse**. Indiquer clairement à l'utilisateur ce qui a été corrigé.

### 6. Livrables complets
Chaque demande terminée doit obligatoirement fournir :
1. Le script paramétré : `scripts/<nom>.py`
2. Le fichier modèle : `out/<nom>.stl`
3. La fiche de cotation et sourcing : `specs/<nom>_dimensions.md`
4. Les rendus de validation : `out/<nom>_*.png`
5. Dans le message de restitution :
   - Un **tableau comparatif des contrôles** (Valeur mesurée vs Cible théorique vs Écart).
   - La liste exhaustive des **limites connues du modèle**.

---

## ⚙️ Procédure Standard de Modélisation (Étapes systématiques)

Pour toute nouvelle demande (« *modélise-moi un X* »), exécuter rigoureusement les 5 phases suivantes :

### Phase 1 : Cadrage, sourcing et fiche de dimensions
- Créer ou exiger `specs/<modele>_dimensions.md`.
- Si les dimensions ou la source sont absentes ou incomplètes, poser au maximum 3 questions ciblées :
  1. *Dimensions et cotes fonctionnelles exactes* (avec source/datasheet).
  2. *Usage, contraintes mécaniques et type d'assemblage*.
  3. *Matériau (PLA, PETG, TPU) et imprimante envisagés*.
- **Ne pas commencer le code tant que les cotes ne sont pas validées.**

### Phase 2 : Rédaction du script bpy paramétré
- Rédiger un script Python autonome dans `scripts/<nom_du_modele>.py`.
- Le script applique les standards :
  - Paramètres nommés, unités en mm et sources en tête de fichier.
  - Définition 2D extrudée, congés avec segments suffisants, évidement par offset/soustraction booléenne.
  - Positionnement des découpes selon le repère de référence de la spec.
  - Application de tous les modificateurs (`bpy.ops.object.modifier_apply`).
  - Vérification de la topologie via bmesh.
  - Export STL dans `out/<nom_du_modele>.stl`.

### Phase 3 : Exécution via Blender MCP
- Exécuter le script via l'outil `execute_blender_code`.
- Vérifier la bonne exécution et récupérer les logs de sortie.

### Phase 4 : Contrôles de validation et rendus
- Exécuter la routine de contrôle qualité (Bounding Box, Volume, épaisseur minimale, 0 arête non-manifold, 0 arête ouverte).
- Générer les rendus PNG multi-angles (dessus, dessous, profil, et coupe si creux).
- Si un critère échoue, auto-corriger immédiatement.

### Phase 5 : Présentation des livrables
- Fournir les liens cliquables vers les fichiers produits (STL, script, fiche spec, images de rendu).
- Afficher le tableau de conformité (Mesure vs Cible vs Écart).
- Détailler les limites connues du modèle et les recommandations d'impression (supports, orientation plateau).
- Attendre l'avis de l'utilisateur avant toute itération.
