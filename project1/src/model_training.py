import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import os

os.makedirs('models', exist_ok=True)

def load_data():
    df = pd.read_csv("data/IBM_Attrition_Final.csv")
    print(f"✅ Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def preprocess_and_select_features(df):
    X = df.drop('Attrition', axis=1)
    y = df['Attrition']
    
    # Encode categorical columns
    categorical_cols = X.select_dtypes(include=['object']).columns
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
    
    # Feature Selection
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X, y)
    feature_importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    print("\n🔝 Top 10 Important Features:")
    print(feature_importance.head(10))
    
    top_features = feature_importance.head(15).index.tolist()
    X = X[top_features]
    
    # Scale features
    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    
    return X, y, encoders, scaler, top_features

def train_multiple_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced'),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM": SVC(kernel='rbf', probability=True)
    }
    
    best_model = None
    best_acc = 0
    best_name = ""
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        print(f"\n📊 {name} Accuracy: {acc:.4f}")
        
        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name
    
    print(f"\n🏆 Best Model: {best_name} with Accuracy: {best_acc:.4f}")
    
    # Save everything
    joblib.dump(best_model, 'models/best_attrition_model.pkl')
    joblib.dump(top_features, 'models/top_features.pkl')
    joblib.dump(encoders, 'models/encoders.pkl')
    
    print("✅ Model, features and encoders saved successfully!")
    return best_model

if __name__ == "__main__":
    df = load_data()
    X, y, encoders, scaler, top_features = preprocess_and_select_features(df)
    
    # Save top features
    joblib.dump(top_features, 'models/top_features.pkl')
    
    model = train_multiple_models(X, y)
    print("\n🎯 Model Training Completed as per Project Description!")