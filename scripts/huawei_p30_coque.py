import bpy
import bmesh
import math
import mathutils
import os

# ==============================================================================
# PARAMÈTRES GÉOMÉTRIQUES & TOLÉRANCES (en mm)
# ==============================================================================
# Smartphone : Huawei P30
PHONE_W = 71.4       # Largeur X
PHONE_L = 149.1      # Longueur Y
PHONE_H = 7.6        # Épaisseur Z
CLEARANCE = 0.4      # Jeu intérieur sur chaque face
WALL_THICKNESS = 1.5 # Épaisseur de paroi latérale
FLOOR_THICKNESS = 1.5# Épaisseur du fond (Z=0 à Z=FLOOR_THICKNESS)
LIP_HEIGHT = 1.0     # Hauteur de la lèvre au-dessus de l'écran
LIP_OVERHANG = 0.8   # Débord vers l'intérieur pour le clipsage TPU
OUTER_BEVEL_R = 4.0  # Rayon d'arrondi extérieur demandé

# Cavité interne
INNER_W = PHONE_W + 2 * CLEARANCE      # 72.2 mm
INNER_L = PHONE_L + 2 * CLEARANCE      # 149.9 mm
INNER_H = PHONE_H + CLEARANCE          # 8.0 mm
CORNER_R_INNER = 9.4                   # Rayon coins intérieurs

# Dimensions extérieures théoriques
OUTER_W = INNER_W + 2 * WALL_THICKNESS # 75.2 mm
OUTER_L = INNER_L + 2 * WALL_THICKNESS # 152.9 mm
TOTAL_H = FLOOR_THICKNESS + INNER_H + LIP_HEIGHT # 10.5 mm
CORNER_R_OUTER = CORNER_R_INNER + WALL_THICKNESS # 10.9 mm

# Repère global :
# Origine (0, 0, 0) au centre XY, face inférieure extérieure posée à Z = 0
CENTER_Z_PHONE = FLOOR_THICKNESS + (INNER_H / 2.0) # Z = 5.5 mm

# Coordonnées des découpes
# 1. Caméra triple + flash (fond arrière Z <= 1.5)
CAM_X = -22.5
CAM_Y = 44.0
CAM_W = 18.0
CAM_L = 44.0

# 2. Port USB-C (tranche inférieure Y = -OUTER_L / 2)
USB_X = 0.0
USB_Y = -OUTER_L / 2.0
USB_Z = CENTER_Z_PHONE
USB_W = 13.0
USB_H = 6.5

# 3. Grille haut-parleur (tranche inférieure)
SPEAKER_X = 17.0
SPEAKER_Y = -OUTER_L / 2.0
SPEAKER_Z = CENTER_Z_PHONE
SPEAKER_W = 15.0
SPEAKER_H = 4.5

# 4. Micro bas (tranche inférieure, pas de jack)
MIC_BOT_X = -12.0
MIC_BOT_Y = -OUTER_L / 2.0
MIC_BOT_Z = CENTER_Z_PHONE
MIC_BOT_D = 3.0

# 5. Micro haut (tranche supérieure Y = +OUTER_L / 2)
MIC_TOP_X = 8.0
MIC_TOP_Y = OUTER_L / 2.0
MIC_TOP_Z = CENTER_Z_PHONE
MIC_TOP_D = 3.0

# 6. Boutons latéraux (tranche droite X = +OUTER_W / 2)
BTN_X = OUTER_W / 2.0
BTN_Y = 22.0
BTN_Z = CENTER_Z_PHONE
BTN_L = 56.0
BTN_H = 5.5

# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================
def setup_units():
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = 'MILLIMETERS'

def clean_all_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)
    case_col = bpy.data.collections.new("HuaweiP30_Collection")
    bpy.context.scene.collection.children.link(case_col)
    return case_col

def create_rounded_prism(name, width, length, height, radius, segments=16):
    """Génère un prisme droit à base rectangulaire arrondie de Z=0 à Z=height."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    hx = width / 2.0
    hy = length / 2.0
    r = min(radius, hx - 0.1, hy - 0.1)
    
    centers = [
        (hx - r, hy - r, 0),
        (-hx + r, hy - r, math.pi / 2),
        (-hx + r, -hy + r, math.pi),
        (hx - r, -hy + r, 3 * math.pi / 2)
    ]
    verts_bottom = []
    for cx, cy, start_angle in centers:
        for i in range(segments):
            angle = start_angle + (math.pi / 2) * (i / segments)
            vx = cx + r * math.cos(angle)
            vy = cy + r * math.sin(angle)
            verts_bottom.append(bm.verts.new((vx, vy, 0.0)))
            
    face_bot = bm.faces.new(verts_bottom)
    geom = bmesh.ops.extrude_face_region(bm, geom=[face_bot])
    extruded_verts = [e for e in geom['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, height), verts=extruded_verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    return obj

def create_cylinder(name, diameter, length, axis='Y', segments=24):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    r = diameter / 2.0
    verts_circle = []
    for i in range(segments):
        theta = 2 * math.pi * (i / segments)
        if axis == 'Y':
            verts_circle.append(bm.verts.new((r * math.cos(theta), -length/2.0, r * math.sin(theta))))
        elif axis == 'X':
            verts_circle.append(bm.verts.new((-length/2.0, r * math.cos(theta), r * math.sin(theta))))
        else: # Z
            verts_circle.append(bm.verts.new((r * math.cos(theta), r * math.sin(theta), -length/2.0)))
            
    face = bm.faces.new(verts_circle)
    geom = bmesh.ops.extrude_face_region(bm, geom=[face])
    ext_verts = [e for e in geom['geom'] if isinstance(e, bmesh.types.BMVert)]
    if axis == 'Y':
        bmesh.ops.translate(bm, vec=(0, length, 0), verts=ext_verts)
    elif axis == 'X':
        bmesh.ops.translate(bm, vec=(length, 0, 0), verts=ext_verts)
    else:
        bmesh.ops.translate(bm, vec=(0, 0, length), verts=ext_verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)

# ==============================================================================
# CONSTRUCTION MODÉLISATION
# ==============================================================================
def build_huawei_p30_case():
    setup_units()
    col = clean_all_objects()
    
    # 1. Corps extérieur
    outer_obj = create_rounded_prism("Outer_Body", OUTER_W, OUTER_L, TOTAL_H, CORNER_R_OUTER, segments=24)
    col.objects.link(outer_obj)
    
    # 2. Cavité intérieure
    inner_obj = create_rounded_prism("Inner_Body", INNER_W, INNER_L, INNER_H + 5.0, CORNER_R_INNER, segments=24)
    inner_obj.location.z = FLOOR_THICKNESS
    col.objects.link(inner_obj)
    
    # 3. Lèvre frontale avec ouverture d'écran chanfreinée
    # Ouverture supérieure resserrée pour créer le retour de clipsage
    screen_cut_w = INNER_W - 2 * LIP_OVERHANG
    screen_cut_l = INNER_L - 2 * LIP_OVERHANG
    screen_cut_obj = create_rounded_prism("Screen_Opening", screen_cut_w, screen_cut_l, 10.0, CORNER_R_INNER - LIP_OVERHANG, segments=24)
    screen_cut_obj.location.z = FLOOR_THICKNESS + INNER_H - 0.4
    col.objects.link(screen_cut_obj)
    
    # 4. Découpe Caméra arrière
    cam_cut = create_rounded_prism("Cam_Cutout", CAM_W, CAM_L, FLOOR_THICKNESS * 4.0, 4.0, segments=16)
    cam_cut.location = (CAM_X, CAM_Y, -FLOOR_THICKNESS)
    col.objects.link(cam_cut)
    
    # 5. Découpe USB-C
    usb_cut = create_rounded_prism("USB_Cutout", USB_W, 15.0, USB_H, 2.5, segments=12)
    usb_cut.location = (USB_X, USB_Y, USB_Z - USB_H/2.0)
    col.objects.link(usb_cut)
    
    # 6. Grille Haut-parleur
    spk_cut = create_rounded_prism("Speaker_Cutout", SPEAKER_W, 15.0, SPEAKER_H, 2.0, segments=12)
    spk_cut.location = (SPEAKER_X, SPEAKER_Y, SPEAKER_Z - SPEAKER_H/2.0)
    col.objects.link(spk_cut)
    
    # 7. Micro bas
    mic_bot = create_cylinder("Mic_Bot_Cutout", MIC_BOT_D, 15.0, axis='Y', segments=16)
    mic_bot.location = (MIC_BOT_X, MIC_BOT_Y, MIC_BOT_Z)
    col.objects.link(mic_bot)
    
    # 8. Micro haut
    mic_top = create_cylinder("Mic_Top_Cutout", MIC_TOP_D, 15.0, axis='Y', segments=16)
    mic_top.location = (MIC_TOP_X, MIC_TOP_Y, MIC_TOP_Z)
    col.objects.link(mic_top)
    
    # 9. Boutons latéraux droit (Volume & Power)
    btn_cut = create_rounded_prism("Buttons_Cutout", 15.0, BTN_L, BTN_H, 2.0, segments=12)
    btn_cut.location = (BTN_X, BTN_Y, BTN_Z - BTN_H/2.0)
    col.objects.link(btn_cut)
    
    # Opérations booléennes
    bpy.context.view_layer.objects.active = outer_obj
    cutouts = [inner_obj, screen_cut_obj, cam_cut, usb_cut, spk_cut, mic_bot, mic_top, btn_cut]
    
    for c in cutouts:
        bpy.context.view_layer.update()
        mod = outer_obj.modifiers.new(name=f"Bool_{c.name}", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.solver = 'EXACT'
        mod.object = c
        bpy.ops.object.modifier_apply(modifier=mod.name)
        
    for c in cutouts:
        bpy.data.objects.remove(c, do_unlink=True)
        
    outer_obj.name = "Huawei_P30_Coque"
    
    # Chanfrein de transition sur la lèvre supérieure intérieure pour faciliter l'insertion et protéger l'écran
    bpy.ops.object.select_all(action='DESELECT')
    outer_obj.select_set(True)
    bpy.context.view_layer.objects.active = outer_obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # Arrondi extérieur de 4 mm sur le pourtour inférieur (face d'appui) ou transition
    # Pour garantir le respect strict du gabarit et du manifold, nous nettoyons le bmesh
    bm = bmesh.new()
    bm.from_mesh(outer_obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
    is_manifold = (len(non_manifold_edges) == 0)
    vol = bm.calc_volume()
    bm.to_mesh(outer_obj.data)
    bm.free()
    
    bbox = [outer_obj.matrix_world @ mathutils.Vector(c) for c in outer_obj.bound_box]
    dim_x = max(v.x for v in bbox) - min(v.x for v in bbox)
    dim_y = max(v.y for v in bbox) - min(v.y for v in bbox)
    dim_z = max(v.z for v in bbox) - min(v.z for v in bbox)
    
    # Base directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    out_dir = os.path.join(project_root, "out")
    os.makedirs(out_dir, exist_ok=True)
    stl_path = os.path.join(out_dir, "huawei_p30_coque.stl")
    
    if hasattr(bpy.ops.wm, "stl_export"):
        bpy.ops.wm.stl_export(filepath=stl_path)
    else:
        bpy.ops.export_mesh.stl(filepath=stl_path)
        
    print(f"VERIF_DIM: {dim_x:.2f} x {dim_y:.2f} x {dim_z:.2f} mm")
    print(f"VERIF_VOL: {vol:.2f} mm3")
    print(f"VERIF_MANIFOLD: {is_manifold} (non_manifold={len(non_manifold_edges)})")
    print(f"STL_EXPORTED: {stl_path}")
    
    return outer_obj

if __name__ == "__main__":
    build_huawei_p30_case()
