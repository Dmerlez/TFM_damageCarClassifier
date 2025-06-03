import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.preprocessing import label_binarize

# Cargar datos extraídos previamente
X = np.load("/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/X_clip.npy")
y = np.load("/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/y_labels.npy")

# Codificar etiquetas string a números
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# División de entrenamiento
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, stratify=y_encoded, test_size=0.2, random_state=42)

scaler = StandardScaler()
scaler.fit(X_train)

# ✅ Transformar datos
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

classes = np.unique(y_train)
class_weights_array = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
class_weight_dict = dict(zip(classes, class_weights_array))
y_test_bin = label_binarize(y_test, classes=classes)

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
        eval_metric='mlogloss',
        learning_rate=0.1,
        n_estimators=1000,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        gamma=0.2
    )
}

# Entrenamiento y evaluación
for name, model in models.items():
    print(f"\n🔍 Entrenando: {name}")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    # Reconvertir etiquetas numéricas a string
    y_test_labels = le.inverse_transform(y_test)
    y_pred_labels = le.inverse_transform(y_pred)

    # Métricas
    acc = accuracy_score(y_test_labels, y_pred_labels)
    print(f"\n✅ Accuracy ({name}): {round(acc, 4)}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test_labels, y_pred_labels))

    print("\n📊 Matriz de Confusión:")
    print(pd.DataFrame(confusion_matrix(y_test_labels, y_pred_labels), 
                       index=le.classes_, columns=le.classes_))
    
    # Guardar modelo
    joblib.dump(model, f"/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/{name}_clip_model.pkl")
    joblib.dump(scaler, f"/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/{name}_scaler.pkl")
    # Guardar LabelEncoder
    joblib.dump(le, f"/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/models/{name}_label_encoder.pkl")
