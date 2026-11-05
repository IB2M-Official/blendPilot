"""
test_cube.py - Modélisation paramétrique d'un cube de test 20mm avec alésage traversant 5mm.
Conforme aux règles blendPilot (centré sur l'origine, base sur Z=0, manifold garanti).
"""

import bpy
import bmesh
import math
import os

# --- Paramètres de conception (en millimètres) ---
CUBE_SIZE = 20.0       # Largeur, Longueur, Hauteur (mm)
HOLE_DIAMETER = 5.0    # Diamètre du trou traversant (mm)
CYLINDER_VERTICES = 64 # Définition circulaire pour impression propre

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
STL_OUTPUT = os.path.join(BASE_DIR, "out", "test_cube.stl")
PNG_OUTPUT = os.path.join(BASE_DIR, "out", "test_cube_preview.png")

def setup_units():
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 0.001  # 1 unité = 1 mm
    scene.unit_settings.length_unit = 'MILLIMETERS'

def clean_objects():
    # Supprime uniquement les maillages existants pour un environnement propre
    bpy.ops.object.select_all(action='DESELECT')
    for obj in list(bpy.data.objects):
        if obj.type == 'MESH':
            bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)

def build_model():
    # 1. Création du cube 20x20x20 mm
    # Primitive Blender : 'size' correspond à l'arête totale
    bpy.ops.mesh.primitive_cube_add(
        size=CUBE_SIZE,
        location=(0.0, 0.0, CUBE_SIZE / 2.0) # Base du cube posée sur Z = 0
    )
    cube_obj = bpy.context.active_object
    cube_obj.name = "TestCube"

    # 2. Création du cylindre soustractif (alésage)
    radius = HOLE_DIAMETER / 2.0
    depth = CUBE_SIZE + 4.0 # Déborde légèrement en haut et en bas pour un booléen propre
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=depth,
        vertices=CYLINDER_VERTICES,
        location=(0.0, 0.0, CUBE_SIZE / 2.0)
    )
    cutter_obj = bpy.context.active_object
    cutter_obj.name = "HoleCutter"

    # 3. Opération booléenne de soustraction
    bpy.context.view_layer.objects.active = cube_obj
    mod = cube_obj.modifiers.new(name="BoreHole", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.operand_type = 'OBJECT'
    mod.object = cutter_obj
    mod.solver = 'EXACT'

    bpy.ops.object.modifier_apply(modifier=mod.name)

    # 4. Suppression de l'outil de découpe
    bpy.data.objects.remove(cutter_obj, do_unlink=True)

    # 5. Application des transformations géométriques
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    return cube_obj

def analyze_mesh(obj):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    # Détection des arêtes non-manifold ou de bordures
    non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
    boundary_edges = [e for e in bm.edges if e.is_boundary]

    # Calcul du volume exact
    volume = bm.calc_volume()

    # Bounding box
    bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    min_x = min(v.x for v in bbox)
    max_x = max(v.x for v in bbox)
    min_y = min(v.y for v in bbox)
    max_y = max(v.y for v in bbox)
    min_z = min(v.z for v in bbox)
    max_z = max(v.z for v in bbox)

    bm.free()

    dim_x = max_x - min_x
    dim_y = max_y - min_y
    dim_z = max_z - min_z

    return {
        "non_manifold_count": len(non_manifold_edges),
        "boundary_count": len(boundary_edges),
        "volume_mm3": volume,
        "bbox_dimensions": (dim_x, dim_y, dim_z),
        "min_z": min_z,
        "max_z": max_z
    }

def export_model_stl(obj, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Blender 4.2 supporte le nouvel exporteur C++ wm.stl_export
    try:
        bpy.ops.wm.stl_export(
            filepath=filepath,
            export_selected_objects=True,
            apply_modifiers=True
        )
    except Exception:
        # Fallback exportateur standard
        bpy.ops.export_mesh.stl(
            filepath=filepath,
            use_selection=True,
            use_mesh_modifiers=True
        )

def render_preview(obj, filepath):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = filepath
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600

    # Création ou réutilisation de la caméra pour cadrer l'objet
    cam = bpy.data.objects.get("Camera")
    if not cam:
        bpy.ops.object.camera_add(location=(35.0, -35.0, 30.0), rotation=(math.radians(60), 0, math.radians(45)))
        cam = bpy.context.active_object
        cam.name = "Camera"
    else:
        cam.location = (35.0, -35.0, 30.0)
        cam.rotation_euler = (math.radians(60), 0, math.radians(45))
    scene.camera = cam

    # Lumière
    light = bpy.data.objects.get("Light")
    if not light:
        bpy.ops.object.light_add(type='SUN', location=(10.0, -10.0, 40.0))
        light = bpy.context.active_object
        light.name = "Light"

    bpy.ops.render.render(write_still=True)

import mathutils
setup_units()
clean_objects()
cube = build_model()
stats = analyze_mesh(cube)
export_model_stl(cube, STL_OUTPUT)
render_preview(cube, PNG_OUTPUT)

print("--- RESULTATS DE VERIFICATION ---")
print(f"FICHIER_STL: {STL_OUTPUT}")
print(f"FICHIER_PNG: {PNG_OUTPUT}")
print(f"BOUNDING_BOX: X={stats['bbox_dimensions'][0]:.2f}mm, Y={stats['bbox_dimensions'][1]:.2f}mm, Z={stats['bbox_dimensions'][2]:.2f}mm")
print(f"ALTITUDE_Z: Min Z={stats['min_z']:.2f}mm (base au plateau), Max Z={stats['max_z']:.2f}mm")
print(f"VOLUME_MM3: {stats['volume_mm3']:.2f} mm3")
print(f"NON_MANIFOLD_EDGES: {stats['non_manifold_count']}")
print(f"BOUNDARY_EDGES: {stats['boundary_count']}")
