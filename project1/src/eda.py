import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
def load_cleaned_data():
    df = pd.read_csv("data/IBM_Attrition_Final.csv")
    print(f"✅ EDA Data Loaded: {df.shape}")
    return df

def perform_eda(df):
    print("\n🔍 Starting Exploratory Data Analysis...\n")
    
    # 1. Attrition Distribution (Target)
    print("Attrition Distribution:")
    print(df['Attrition'].value_counts(normalize=True) * 100)
    
    # 2. Key Insights
    print("\nAverage Monthly Income (Stayed vs Left):")
    print(df.groupby('Attrition')['MonthlyIncome'].mean())
    
    print("\nOvertime Impact:")
    print(df.groupby('OverTime')['Attrition'].value_counts(normalize=True))
    
    # Visualizations
    plt.figure(figsize=(15, 10))
    
    # Attrition by Department
    plt.subplot(2, 2, 1)
    sns.countplot(x='Department', hue='Attrition', data=df)
    plt.title('Attrition by Department')
    plt.xticks(rotation=45)
    
    # Age Distribution
    plt.subplot(2, 2, 2)
    sns.histplot(data=df, x='Age', hue='Attrition', kde=True)
    plt.title('Age Distribution by Attrition')
    
    # Job Satisfaction
    plt.subplot(2, 2, 3)
    sns.boxplot(x='Attrition', y='JobSatisfaction', data=df)
    plt.title('Job Satisfaction vs Attrition')
    
    # Monthly Income
    plt.subplot(2, 2, 4)
    sns.boxplot(x='Attrition', y='MonthlyIncome', data=df)
    plt.title('Monthly Income vs Attrition')
    
    plt.tight_layout()
    plt.savefig('data/eda_visualizations.png')
    print("\n📊 Visualizations saved as: data/eda_visualizations.png")
    
    return df

if __name__ == "__main__":
    df = load_cleaned_data()
    perform_eda(df)
    print("\n🎯 EDA Completed! Key insights ready for model building.")