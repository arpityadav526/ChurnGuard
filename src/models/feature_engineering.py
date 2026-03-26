import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. AvgMonthlySpend
    df["AvgMonthlySpend"] = df["TotalCharges"] / (df["tenure"] + 1)

    # 2. TenureGroup
    def tenure_group(t):
        if t <= 12:
            return "New"
        elif t <= 24:
            return "Mid"
        else:
            return "Loyal"

    df["TenureGroup"] = df["tenure"].apply(tenure_group)

    # 3. TotalServices
    services = [
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]

    service_mapping = {
        "No": 0,
        "Yes": 1,
        "No internet service": 0,
        "No phone service": 0,
        "Fiber optic": 1,
        "DSL": 1,
    }

    for col in services:
        df[col] = df[col].replace(service_mapping)

    df["TotalServices"] = df[services].sum(axis=1)

    # 4. ContractRisk
    df["ContractRisk"] = df["Contract"].map({
        "Month-to-month": 2,
        "One year": 1,
        "Two year": 0
    })

    return df