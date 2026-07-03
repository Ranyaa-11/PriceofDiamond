import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import pickle

# Load and prepare data
df = pd.read_csv("diamonds.csv")
df = df.drop(columns=df.columns[0])

# Encode categorical variables
quality_map = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
color_map = {'D': 0, 'E': 1, 'F': 2, 'G': 3, 'H': 4, 'I': 5, 'J': 6}
clarity_map = {'IF': 0, 'VVS1': 1, 'VVS2': 2, 'VS1': 3, 'VS2': 4, 'SI1': 5, 'SI2': 6, 'I1': 7}

df['quality_encoded'] = df['quality'].map(quality_map)
df['color_encoded'] = df['color'].map(color_map)
df['clarity_encoded'] = df['clarity'].map(clarity_map)

# Train model
features = ['carat', 'depth', 'table', 'x', 'y', 'z', 'quality_encoded', 'color_encoded', 'clarity_encoded']
X = df[features]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

from pathlib import Path

BASE_DIR = Path(__file__).parent

model = joblib.load(BASE_DIR / "diamond_price_model.pkl")
encoders = joblib.load(BASE_DIR / "label_encoders.pkl")
feature_columns = joblib.load(BASE_DIR / "feature_columns.pkl")
encoders = {'quality': quality_map, 'color': color_map, 'clarity': clarity_map}
with open("label_encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)

print("✅ Model ready!")
