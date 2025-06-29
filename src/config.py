CLASSES = [
    "Abolladuras",  # dents
    "Intacto",      # no damage
    "Rayones",      # scratches
    "Siniestro"     # structural damage
]

#CLASSES_ZERO_SHOT = [
#    "Un coche con una gran abolladura en la puerta lateral",
#    "Un vehículo limpio y sin ningún tipo de daño visible",
#    "Carro con rayones superficiales visibles en la pintura",
#    "Vehículo siniestrado con daños estructurales severos"
#]

# Mapeo descriptivo → etiqueta base
#CLASS_MAPPING = {
#    "Un coche con una gran abolladura en la puerta lateral": "Abolladuras",
#    "Un vehículo limpio y sin ningún tipo de daño visible": "Intacto",
#    "Carro con rayones superficiales visibles en la pintura": "Rayones",
#    "Vehículo siniestrado con daños estructurales severos": "Siniestro",
#    "indeterminado": "Indeterminado"  # clave consistente en minúscula
#}

# Prompts enriquecidos por clase para Zero-Shot
PROMPTS_BY_CLASS = {
    "Abolladuras": [
        "A car with a large dent on the front side panel",
        "A gray vehicle with visible dents near the wheel arch",
        "A car with a shallow but wide dent on the driver-side door",
        "A front bumper with a significant depression due to impact",
        "A vehicle showing minor collision damage with bent panels",
        "A car with a slightly deformed hood after a front-end hit",
        "A side door displaying a visible dent with surrounding paint intact",
        "A compact car with localized denting above the front wheel",
        "A damaged vehicle with a concave shape on the metallic body",
        "A car that suffered a soft frontal collision, creating visible dents"
    ],
    "Intacto": [
        "A clean car with no visible damage or scratches.",
        "A well-maintained vehicle with a smooth and undamaged body.",
        "A car exterior that shows no dents, scratches, or imperfections.",
        "A spotless automobile parked with no signs of collision or damage.",
        "A silver sedan in perfect condition with no signs of wear or impact.",
        "A black SUV with clean paint and no body damage.",
        "A front view of a pristine vehicle with no broken or deformed parts.",
        "A rear view of a car showing no signs of any impact or damage.",
        "A new-looking vehicle with all panels intact and unmarked.",
        "A side view of a car with a flawless body and no cosmetic issues.",
        "A showroom-quality vehicle with a fully intact exterior.",
        "A close-up of a clean car door without scratches or dents.",
        "A vehicle with no structural or cosmetic damage, parked in daylight.",
        "An undamaged sedan with even paint and no visible flaws.",
        "A car that looks recently washed and completely intact."
    ],
    "Rayones": [
        "A car with scratches on the paint",
        "A vehicle with visible surface scratches",
        "A car with minor scratches on the bumper or doors"        
    ],
    "Siniestro": [
        "A heavily damaged car with crushed structural components",
        "A vehicle with severe frame deformation after a collision",
        "A totaled car exhibiting extensive crumpling and broken parts",
        "An automobile with major body collapse and shattered panels",
        "A wrecked car with bent chassis and exposed internal structure",
        "A severely smashed vehicle showing twisted metal and broken glass",
        "A car with catastrophic damage to the front and side sections"
    ]
}


# Mapping final no necesario si usamos las claves como etiquetas directamente
# Pero lo dejamos por compatibilidad
CLASS_MAPPING = {
    prompt: class_name
    for class_name, prompts in PROMPTS_BY_CLASS.items()
    for prompt in prompts
} | {"indeterminate": "Indeterminado"}  # Python 3.9+ merge de dicts

# Etiquetas únicas para evaluación (sin duplicados)
EVAL_CLASSES = list(PROMPTS_BY_CLASS.keys())

# Eliminamos duplicados con set()
#EVAL_CLASSES = list(set(CLASS_MAPPING.values()))