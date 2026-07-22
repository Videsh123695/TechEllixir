import pandas as pd
import joblib

# Load everything
model = joblib.load('models/best_attrition_model.pkl')
top_features = joblib.load('models/top_features.pkl')
encoders = joblib.load('models/encoders.pkl')

def predict_attrition(employee_dict):
    df = pd.DataFrame([employee_dict])
    
    # Add missing columns with default value
    for col in top_features:
        if col not in df.columns:
            df[col] = 0
    
    df = df[top_features]
    
    # Apply saved encoders
    for col, encoder in encoders.items():
        if col in df.columns:
            try:
                df[col] = encoder.transform(df[col])
            except:
                df[col] = 0  # fallback
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    print("\n" + "="*70)
    print("🔮 TECHELLIXIR - EMPLOYEE ATTRITION PREDICTION SYSTEM")
    print("="*70)
    print(f"Prediction      : {'🚨 HIGH RISK - Likely to Leave' if prediction == 'Yes' else '✅ LOW RISK - Likely to Stay'}")
    print(f"Leave Probability : {probability:.1%}")
    print("="*70)
    
    if probability > 0.4:
        print("💡 HR Recommendation: Immediate retention action required.")
    else:
        print("💡 HR Recommendation: Employee is stable.")
    
    return prediction, probability


if __name__ == "__main__":
    sample_employee = {
        'Age': 32,
        'MonthlyIncome': 5500,
        'OverTime': 'Yes',
        'JobSatisfaction': 1,
        'YearsAtCompany': 3,
        'DistanceFromHome': 15,
        'TotalWorkingYears': 8,
        'JobLevel': 2,
        'EnvironmentSatisfaction': 2,
        'BusinessTravel': 'Travel_Frequently',
        'DailyRate': 1100,
        'JobRole': 'Sales Executive',
        'MaritalStatus': 'Married',
    }
    
    predict_attrition(sample_employee)