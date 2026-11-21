"""
Train the disease prediction model.
Run:  ./venv/bin/python train_model.py
"""
import re
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def clean(text):
    """Remove extra spaces from a name."""
    return re.sub(r"\s+", " ", str(text)).strip()


# 1. Load the data
df = pd.read_csv("data/Training.csv")
print("Original shape:", df.shape)

# 2. Clean the data
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]                 # remove empty columns
df.columns = [clean(c).replace(" ", "_") for c in df.columns]        # clean symptom names
df["prognosis"] = df["prognosis"].map(clean)                         # clean disease names
print("Missing values:", int(df.isnull().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
df = df.drop_duplicates()                                            # remove duplicates
print("Shape after cleaning:", df.shape)

# 3. Split into input (symptoms) and output (disease)
X = df.drop("prognosis", axis=1)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["prognosis"])                     # disease name -> number
print("Symptoms:", X.shape[1], "| Diseases:", len(label_encoder.classes_))

# 4. Train / test split (80% / 20%)
smallest_class = pd.Series(y).value_counts().min()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,
    stratify=y if smallest_class >= 2 else None,
)

# 5. Compare three models
models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Naive Bayes": BernoulliNB(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
}
print("\nModel comparison (accuracy on test data):")
for name, model in models.items():
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"  {name:<15} {accuracy:.3f}")

# 6. Save the Random Forest (with the label encoder and symptom list) in ONE file
with open("models/model.pkl", "wb") as f:
    pickle.dump({
        "model": models["Random Forest"],
        "label_encoder": label_encoder,
        "symptoms": list(X.columns),
    }, f)
print("\nSaved models/model.pkl")
