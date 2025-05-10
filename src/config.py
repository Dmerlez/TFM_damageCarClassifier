CLASSES = [
    "Abolladuras",  # dents
    "Intacto",      # no damage
    "Rallones",     # scratches
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
#    "Carro con rayones superficiales visibles en la pintura": "Rallones",
#    "Vehículo siniestrado con daños estructurales severos": "Siniestro",
#    "indeterminado": "Indeterminado"  # clave consistente en minúscula
#}

# Prompts enriquecidos por clase para Zero-Shot
PROMPTS_BY_CLASS = {
    "Abolladuras": [
        "A car with a single pronounced dent on the side door",
        "A vehicle exhibiting a noticeable dent near the front fender",
        "A car with a deep dent above the wheel arch",
        "A sedan displaying a small but visible dent on the rear quarter panel",
        "An automobile with a shallow dent on the passenger door",
        "A vehicle showing multiple small dents on the door surface",
        "A car with a large depression in the metal near the door handle"
    ],
    "Intacto": [
        "A pristine vehicle with absolutely no visible dents or scratches",
        "A showroom-condition car without any signs of wear or damage",
        "A well-maintained automobile with flawless paint and bodywork",
        "A perfect car exterior free of blemishes or imperfections",
        "A car in mint condition with no dents, scratches, or paint chips",
        "An undamaged vehicle appearing straight from the factory",
        "A clean, untouched car body with smooth, glossy finish"
    ],
    "Rallones": [
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
