import pandas as pd
import os

# Load the data
def load_data(file_path):
    df = pd.read_csv(file_path)
    print(f"✅ Data Loaded: {df.shape[0]} rows and {df.shape[1]} columns")
    return df

# Basic Cleaning
def clean_data(df):
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Check missing values
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    # Basic info
    print("\nDataset Info:")
    print(df.info())
    
    # Drop useless columns
    columns_to_drop = ['EmployeeCount', 'EmployeeNumber', 'StandardHours', 'Over18']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
    print(f"\n✅ Final Shape: {df.shape[0]} rows and {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    file_path = r"C:\Users\vides\OneDrive\Documents\IBM_EMPLOYEE_DATA.csv"
    
    # Correct calling
    df = load_data(file_path)        # ← return value ko df mein store kar rahe hain
    df_clean = clean_data(df)        # ← ab df pass kar rahe hain
    
    # Save
    # df_clean.to_csv("data/IBM_Attrition_Final.csv", index=False)
    print("\n🎉 Done! File saved successfully.")
# df=load_data(r"C:\Users\vides\OneDrive\Documents\IBM_EMPLOYEE_DATA.csv")
# df=clean_data(df)




