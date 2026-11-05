# Fiche de Spécifications Techniques : Tour de Mage / Tour à Dés Fantastique (Arcane Dice Tower)

## 1. Informations Générales & Sourcing
- **Nom du modèle :** `arcane_dice_tower`
- **Catégorie :** Architecture fantastique / Accessoire de jeu de rôle (RPG)
- **Concours :** Fantasy 3D Print Contest
- **Procédé de fabrication :** Impression 3D FDM (dépôt de fil fondu) / Résine
- **Matériaux cibles :** PLA / PETG (optionnel : ABS/ASA)
- **Source des spécifications :** Cahier des charges officiel Fantasy Contest 3D Print & Standards dimensionnels standard D&D (dés D4 à D20 jusqu'à Ø24 mm circonscrit)
- **Date de relevé / spécification :** 30 octobre 2026
- **Objectif d'impression :** 100% imprimable sans aucun support d'impression (`supportless`).

---

## 2. Encombrement et Tolérances Métrologiques

| Paramètre | Valeur Cible | Tolérance / Seuil | Remarque |
| :--- | :--- | :--- | :--- |
| **Largeur hors-tout ($X$)** | **130.0 mm** | $\pm 0,1\text{ mm}$ | Cour basse + débord latéral tour/mâchicoulis |
| **Profondeur hors-tout ($Y$)**| **160.0 mm** | $\pm 0,1\text{ mm}$ | Arrière de la tour vers l'extrémité de la cour basse |
| **Hauteur hors-tout ($Z$)**   | **185.0 mm** | $\pm 0,1\text{ mm}$ | Du plateau ($Z=0$) au sommet des créneaux |
| **Épaisseur paroi fût**       | **3.0 mm**   | $\pm 0,05\text{ mm}$ | Exigence minimale blendPilot : $\ge 1.5\text{ mm}$ |
| **Épaisseur parois réceptacle**| **2.5 mm**  | $\pm 0,05\text{ mm}$ | Rigidité et maintien des chocs de dés |
| **Épaisseur rampes internes** | **3.0 mm**   | $\pm 0,05\text{ mm}$ | Résistance à l'impact répété |
| **Surplomb maximal**          | **$\le 45^\circ$** | Strict | Par rapport à l'axe vertical $Z$ (aucun support) |
| **Positionnement plateau**    | **$Z_{\min} = 0.0\text{ mm}$** | Strict | Centrage $(X=0, Y=0)$ pour adhérence optimale |

---

## 3. Architecture Géométrique Détaillée

### A. Fût Principal
- **Section :** Cylindrique octogonale régulière (esthétique fortifiée fantastique).
- **Diamètre extérieur ($D_{ext}$) :** $75.0\text{ mm}$ (rayon circonscrit $R = 37.5\text{ mm}$).
- **Diamètre intérieur ($D_{int}$) :** $69.0\text{ mm}$ (dégagement utile pour passage fluide de dés D20 de 22-24 mm).
- **Hauteur de base du fût :** $160.0\text{ mm}$.

### B. Couronnement / Mâchicoulis & Trémie d'Introduction
- **Évasement supérieur :** Transition à $45^\circ$ passant de $\varnothing 75.0\text{ mm}$ à $\varnothing 88.0\text{ mm}$.
- **Trémie d'introduction (Entonnoir) :** Pente interne inversée à $45^\circ$ dirigeant immédiatement le dé vers le puits central.
- **Créneaux de fortification :**
  - Hauteur : $12.0\text{ mm}$ (atteignant la hauteur totale de $185.0\text{ mm}$).
  - Largeur de merlon / créneau : $8.0\text{ mm}$.
  - Arêtes supérieures chanfreinées à $45^\circ$ pour éviter tout pontage à plat.

### C. Guidage Interne (Chicanes / Rampes sans support)
- **Nombre de chicanes :** 3 rampes hélicoïdales alternées étagées sur la hauteur.
- **Pente des rampes :** $40^\circ$ par rapport à l'horizontale ($50^\circ$ par rapport à la verticale, conforme à l'auto-supportage sous-jacent et glissement dynamique optimal).
- **Épaisseur de chaque rampe :** $3.0\text{ mm}$.
- **Profil inférieur des rampes :** Sous-face biseautée / chanfreinée à $45^\circ$ pour supprimer tout surplomb à plat.
- **Dégagement de passage de dé :** Hauteur libre minimale entre rampes $\ge 32.0\text{ mm}$ (compatible D20 jusqu'à 24 mm).

### D. Sortie Basse (Portail Ogival Gothique)
- **Largeur utile :** $38.0\text{ mm}$.
- **Hauteur totale sous clé d'ogive :** $48.0\text{ mm}$.
- **Profil d'arche :** Arc brisé gothique avec angle au sommet $\le 40^\circ$ par rapport à la verticale (auto-portant en impression FDM, zéro support).
- **Semelle de sortie :** Pente de dégagement final guidant le dé directement dans la cour.

### E. Réceptacle / Cour Basse (Dice Tray)
- **Hauteur des remparts de cour :** $25.0\text{ mm}$.
- **Dimensions intérieures utiles :** Largeur $80.0\text{ mm} \times$ Longueur $65.0\text{ mm}$.
- **Parois de retenue :** Profil intérieur avec léger chanfrein ou lèvre de retenue anti-rebond.
- **Fond de cour :** Épaisseur $3.0\text{ mm}$ ($Z \in [0, 3]\text{ mm}$), face inférieure parfaitement coplanaire avec la tour ($Z = 0.0\text{ mm}$).

### F. Texture & Détails de Maçonnerie (Inspirés pierre de taille)
- **Rainurage :** Joints en creux horizontaux et verticaux de largeur $1.0\text{ mm}$ et profondeur $0.8\text{ mm}$.
- **Profil de rainure :** Section en V à $45^\circ$ ou chanfreinée pour garantir une impression sans fil pendouillant ni porte-à-faux horizontal.

---

## 4. Repère de Référence et Coordonnées
- **Origine $(0, 0, 0)$ :**
  - $X = 0.0\text{ mm}$ : Axe central de symétrie gauche/droite de la tour et du réceptacle.
  - $Y = 0.0\text{ mm}$ : Axe vertical central du fût de la tour. La cour s'étend vers $+Y$.
  - $Z = 0.0\text{ mm}$ : Face plane inférieure posée sur le plateau d'impression.
- **Centrage global sur plateau :** La pièce complète (tour + cour) est centrée globalement en $(X=0, Y=0)$ lors de l'assemblage final pour équilibrer la bounding box sur le plateau.

---

## 5. Critères d'Acceptation Qualité (Obligatoires avant livraison)
1. **Topologie 100% Manifold :** 0 arête non-manifold, 0 arête ouverte (boundary edge).
2. **Conformité Bounding Box :**
   - $X \in [129.9, 130.1]\text{ mm}$
   - $Y \in [159.9, 160.1]\text{ mm}$
   - $Z \in [184.9, 185.1]\text{ mm}$
3. **Épaisseurs mesurées :** $\ge 2.5\text{ mm}$ en tout point.
4. **Vérification Surplomb :** Aucun angle $> 45^\circ$ sans raccord biseauté.
5. **Rendus métrologiques :** ISO avant, dessus, dessous ($Z=0$), coupe longitudinale montrant les rampes.
