import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import joblib
import matplotlib.pyplot as plt


DATA_PATH = Path(__file__).parent / "data" / "PCOS_extended_dataset.csv"

df = pd.read_csv(DATA_PATH)
print("=" * 50)
print("Dataset Loaded Successfully")
print("=" * 50)

print("Shape:", df.shape)

print("\nColumns:\n")
print(df.columns.tolist())

print("\nFirst Five Rows:\n")
print(df.head())

features = [
    ' Age (yrs)',
    'Weight (Kg)',
    'Height(Cm) ',
    'BMI',
    'Cycle(R/I)',
    'Cycle length(days)',
    'Weight gain(Y/N)',
    'hair growth(Y/N)',
    'Skin darkening (Y/N)',
    'Hair loss(Y/N)',
    'Pimples(Y/N)',
    'Fast food (Y/N)',
    'Reg.Exercise(Y/N)'
]

target = 'PCOS (Y/N)'

X = df[features]
y = df[target]

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
print("\nTraining Data:", X_train.shape)
print("Testing Data:", X_test.shape)
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("=" * 60)
print("MODEL ACCURACY")
print("=" * 60)

print(f"Accuracy: {accuracy:.2%}")

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(classification_report(y_test, y_pred))

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print(confusion_matrix(y_test, y_pred))

# Save trained model
joblib.dump(model, "models/pcos_model.pkl")

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY!")
print("=" * 60)

# ============================================
# FEATURE IMPORTANCE
# ============================================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)
plt.figure(figsize=(8,6))

plt.barh(
    importance["Feature"],
    importance["Importance"]
)

plt.title("Feature Importance")

plt.xlabel("Importance")

plt.tight_layout()

plt.show()


# print("=" * 60)
# print("DATASET INFORMATION")
# print("=" * 60)
# print(df.info())
#
# print("=" * 60)
# print("MISSING VALUES")
# print("=" * 60)
# print(df.isnull().sum())
#
# print("=" * 60)
# print("DUPLICATE ROWS")
# print("=" * 60)
# print(df.duplicated().sum())
#
# print("=" * 60)
# print("TARGET DISTRIBUTION")
# print("=" * 60)
# print(df["PCOS (Y/N)"].value_counts())
#
# print("=" * 60)
# print("SUMMARY STATISTICS")
# print("=" * 60)
# print(df.describe())
#
# print("Model Trained Successfully!")
