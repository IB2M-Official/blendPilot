# Spécifications de modélisation : Coque Huawei P30

## 1. Cotes de référence du téléphone (Huawei P30 non-Pro)
- Longueur ($Y$) : 149.1 mm
- Largeur ($X$) : 71.4 mm
- Épaisseur ($Z$) : 7.6 mm (corps)
- Rayon des coins : ~9.0 mm

## 2. Paramètres de la coque (TPU / FDM)
- Jeu interne (clearance) : 0.4 mm sur chaque face
  - Cavité intérieure ($X \times Y \times Z$) : $72.2 \times 149.9 \times 8.0\text{ mm}$
- Épaisseur de paroi (fond et côtés) : 1.5 mm
- Dimensions externes brutes ($X \times Y \times Z$) : $75.2 \times 152.9 \times 10.5\text{ mm}$
  - Dont fond = 1.5 mm, cavité = 8.0 mm, lèvre frontale = 1.0 mm
- Lèvre frontale : débord de 1.0 mm vers l'intérieur avec biseau à $45^\circ$ pour clipser l'écran.

## 3. Découpes fonctionnelles
- **Caméra arrière & flash** : 
  - Découpe en haut à gauche : environ $18\text{ mm} \times 44\text{ mm}$ avec congés de 3 mm.
- **Tranche inférieure** :
  - Port USB-C : découpe centrale $13\text{ mm} \times 7\text{ mm}$.
  - Prise Jack 3.5 mm : ouverture circulaire $\varnothing 6.5\text{ mm}$ à gauche de l'USB-C.
  - Haut-parleur & micro : fentes/ouvertures à droite de l'USB-C.
- **Tranche droite** :
  - Boutons volume (+/-) et bouton Power : découpe ouverte / fenêtre de dégagement d'accès.

## 4. Orientation & Plateau
- Face arrière plane posée en $Z=0$ pour une adhésion optimale sans support.
- Unités Blender configurées en Millimètres (1:1 pour export STL).
