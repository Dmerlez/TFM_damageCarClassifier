import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from collections import Counter
from sklearn.utils.class_weight import compute_class_weight

# Calcular pesos por clase

# Cargar datos extraídos previamente
X = np.load("/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/X_clip.npy")
y = np.load("/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/y_labels.npy")

# Codificar etiquetas string a números
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# División de entrenamiento
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, stratify=y_encoded, test_size=0.2, random_state=42)

# Modelos a comparar
models = {
    "LogisticRegression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "RandomForest": RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42),
    "MLPClassifier": MLPClassifier(
        hidden_layer_sizes=(256,),
        activation='relu',
        max_iter=1000,
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        use_label_encoder=False,
        eval_metric='mlogloss',
        learning_rate=0.05,
        n_estimators=300,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42
    ),
    "KNN": KNeighborsClassifier(n_neighbors=3)
}

# Entrenamiento y evaluación
for name, model in models.items():
    print(f"\n🔍 Entrenando: {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Reconvertir etiquetas numéricas a string
    y_test_labels = le.inverse_transform(y_test)
    y_pred_labels = le.inverse_transform(y_pred)

    # Métricas
    acc = accuracy_score(y_test_labels, y_pred_labels)
    print(f"\n✅ Accuracy ({name}): {round(acc, 4)}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test_labels, y_pred_labels))

    #print("\n📊 Matriz de Confusión:")
    #print(pd.DataFrame(confusion_matrix(y_test_labels, y_pred_labels), 
    #                   index=le.classes_, columns=le.classes_))

    # Guardar modelo
    joblib.dump(model, f"/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/{name}_clip_model.pkl")
