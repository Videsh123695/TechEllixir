import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="TECHELLIXIR Attrition Predictor", page_icon="🔮", layout="centered")

st.title("🔮 TECHELLIXIR Employee Attrition Prediction")
st.subheader("HR teams ke liye real-time prediction")

# Load assets
@st.cache_resource
def load_assets():
    model = joblib.load('models/best_attrition_model.pkl')
    top_features = joblib.load('models/top_features.pkl')
    return model, top_features

model, top_features = load_assets()

def encode_input(df):
    """Encode categorical variables"""
    mappings = {
        'OverTime': {'Yes': 1, 'No': 0},
        'BusinessTravel': {'Travel_Rarely': 1, 'Travel_Frequently': 2, 'Non-Travel': 0},
        'MaritalStatus': {'Married': 1, 'Single': 0, 'Divorced': 2},
        'JobRole': {'Sales Executive': 0, 'Research Scientist': 1, 'Laboratory Technician': 2,
                    'Manufacturing Director': 3, 'Healthcare Representative': 4, 'Manager': 5,
                    'Sales Representative': 6, 'Research Director': 7, 'Human Resources': 8}
    }
    for col, mapping in mappings.items():
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(0)
    return df

# Input Form
st.header("Employee Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 65, 32)
    monthly_income = st.number_input("Monthly Income ($)", 1000, 20000, 5500)
    years_at_company = st.number_input("Years at Company", 0, 40, 3)
    distance = st.number_input("Distance From Home", 1, 30, 15)
    job_satisfaction = st.slider("Job Satisfaction", 1, 4, 2)
    overtime = st.selectbox("OverTime", ["Yes", "No"])

with col2:
    total_years = st.number_input("Total Working Years", 0, 40, 8)
    job_level = st.number_input("Job Level", 1, 5, 2)
    env_satisfaction = st.slider("Environment Satisfaction", 1, 4, 2)
    business_travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
    job_role = st.selectbox("Job Role", ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manager"])

if st.button("🔮 Predict Employee Attrition", type="primary"):
    input_dict = {
        'Age': age,
        'MonthlyIncome': monthly_income,
        'YearsAtCompany': years_at_company,
        'DistanceFromHome': distance,
        'JobSatisfaction': job_satisfaction,
        'OverTime': overtime,
        'TotalWorkingYears': total_years,
        'JobLevel': job_level,
        'EnvironmentSatisfaction': env_satisfaction,
        'BusinessTravel': business_travel,
        'JobRole': job_role,
    }
    
    df = pd.DataFrame([input_dict])
    
    # Ensure all features
    for col in top_features:
        if col not in df.columns:
            df[col] = 0
    
    df = df[top_features]
    df = encode_input(df)
    
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    
    # # Aggressive Threshold for Demo
    # if prob > 0.25:   # Bahut low threshold
    #     st.error(f"🚨 HIGH RISK - Likely to Leave ({prob:.1%} probability)")
    #     st.warning("💡 Strong Recommendation: Retention meeting schedule karein.")
    # else:
    #     st.success(f"✅ LOW RISK - Likely to Stay ({prob:.1%})")
    
    if pred == 'Yes':
        st.error(f"🚨 HIGH RISK - This employee is likely to leave ({prob:.1%})")
        st.warning("💡 Suggestion: Discuss retention plan soon.")
    else:
        st.success(f"✅ LOW RISK - Employee likely to stay ({prob:.1%} leave risk)")
        st.balloons()

st.caption("Model trained with Random Forest • Accuracy ~87%")