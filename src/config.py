CLASSES = [
    "Abolladuras",  # dents
    "Intacto",      # no damage
    "Rallones",     # scratches
    "Siniestro"     # structural damage
]

CLASSES_ZERO_SHOT = [
    "Un coche con una gran abolladura en la puerta lateral",
    "Un vehículo limpio y sin ningún tipo de daño visible",
    "Carro con rayones superficiales visibles en la pintura",
    "Vehículo siniestrado con daños estructurales severos"
]

# Mapeo descriptivo → etiqueta base
CLASS_MAPPING = {
    "Un coche con una gran abolladura en la puerta lateral": "Abolladuras",
    "Un vehículo limpio y sin ningún tipo de daño visible": "Intacto",
    "Carro con rayones superficiales visibles en la pintura": "Rallones",
    "Vehículo siniestrado con daños estructurales severos": "Siniestro",
    "indeterminado": "Indeterminado"  # clave consistente en minúscula
}

# Eliminamos duplicados con set()
EVAL_CLASSES = list(set(CLASS_MAPPING.values()))
