# Spécifications et Dimensions Officielles : Huawei P30 (ELE-L29 / ELE-L09)

## 1. Sources Officielles & Références
- **Huawei Official Consumer Specifications** :
  - URL : `https://consumer.huawei.com/en/phones/p30/specs/`
  - Longueur (Hauteur) : **149.1 mm**
  - Largeur : **71.36 mm** (arrondi d'usage : 71.4 mm)
  - Épaisseur du châssis : **7.57 mm** (arrondi d'usage : 7.6 mm)
  - Poids : ~165 g
- **GSMArena** :
  - URL : `https://www.gsmarena.com/huawei_p30-9523.php`
  - Dimensions : 149.1 × 71.4 × 7.6 mm
  - Écran : 6.1 pouces OLED plat (bords non courbés contrairement au Pro)
  - Épaisseur du module caméra ("bump") : saillie de ~1.8 mm (hauteur locale ~9.3 mm)

---

## 2. Synthèse des cotes pour la modélisation

| Paramètre | Valeur Smartphone | Valeur Coque (avec jeu + parois) | Remarque |
| :--- | :--- | :--- | :--- |
| **Longueur ($Y$)** | 149.1 mm | Cavité interne = **149.9 mm** ($+2 \times 0.4\text{ mm}$)<br>Externe = **152.9 mm** ($+2 \times 1.5\text{ mm}$) | Tolérance bounding box : $\pm 0.1\text{ mm}$ |
| **Largeur ($X$)** | 71.4 mm | Cavité interne = **72.2 mm** ($+2 \times 0.4\text{ mm}$)<br>Externe = **75.2 mm** ($+2 \times 1.5\text{ mm}$) | Tolérance bounding box : $\pm 0.1\text{ mm}$ |
| **Épaisseur ($Z$)** | 7.6 mm (corps) | Fond = **1.5 mm**<br>Cavité = **8.0 mm** ($7.6 + 0.4\text{ mm}$)<br>Lèvre frontale = **1.0 mm**<br>Total externe = **10.5 mm** | Tolérance bounding box : $\pm 0.1\text{ mm}$ |
| **Rayons de courbure** | Rayon coins corps $\approx 9.0\text{ mm}$ | Cavité = $9.4\text{ mm}$<br>Profil extérieur arrondi = **Rayon 4.0 mm** (selon consigne) | Chanfrein sur la lèvre frontale |

---

## 3. Repère de référence pour le positionnement des découpes
- **Origine $(0, 0, 0)$** : 
  - $X = 0$ : Plan médian de symétrie gauche/droite.
  - $Y = 0$ : Plan médian de symétrie haut/bas.
  - $Z = 0$ : Face inférieure extérieure du fond de la coque (posée à plat sur le plateau FDM).

### Coordonnées et dimensions des découpes prévues :
1. **Module Caméra triple + Flash (Face arrière $Z \le 1.5$)** :
   - Vu de dos (fond orienté vers l'observateur, haut vers $+Y$) : situé en haut à gauche (donc $X < 0$, $Y > 0$).
   - Centre : $X = -22.5\text{ mm}$, $Y = 44.0\text{ mm}$.
   - Dimensions : $18.0\text{ mm} \times 44.0\text{ mm}$, coins arrondis $R = 4.0\text{ mm}$.
2. **Port USB-C (Tranche basse $Y = -76.45\text{ mm}$)** :
   - Centre : $X = 0.0\text{ mm}$, $Z = 5.5\text{ mm}$ (centré sur l'épaisseur du téléphone).
   - Dimensions : $13.0\text{ mm} \times 6.5\text{ mm}$, coins arrondis $R = 2.5\text{ mm}$.
3. **Grille Haut-Parleur (Tranche basse $Y = -76.45\text{ mm}$)** :
   - Position : à droite de l'USB-C vu de face ($X = +17.0\text{ mm}$).
   - Centre : $X = 17.0\text{ mm}$, $Z = 5.5\text{ mm}$.
   - Dimensions : fente de $15.0\text{ mm} \times 4.5\text{ mm}$.
4. **Microphone principal (Tranche basse $Y = -76.45\text{ mm}$)** :
   - Position : petit orifice d'accès micro à gauche de l'USB-C ($X = -12.0\text{ mm}$, $Z = 5.5\text{ mm}$).
   - Diamètre : $\varnothing 3.0\text{ mm}$.
   *(Rappel : Pas de prise jack 3.5 mm conformément à votre consigne)*.
5. **Microphone secondaire d'ambiance (Tranche haute $Y = +76.45\text{ mm}$)** :
   - Centre : $X = 8.0\text{ mm}$, $Z = 5.5\text{ mm}$, diamètre $\varnothing 3.0\text{ mm}$.
6. **Boutons Latéraux Volume et Power (Tranche droite $X = +37.60\text{ mm}$)** :
   - Centre : $Y = 22.0\text{ mm}$, $Z = 5.5\text{ mm}$.
   - Dégagement ouvert : longueur $56.0\text{ mm}$, hauteur $5.5\text{ mm}$, coins arrondis $R = 2.0\text{ mm}$.
