def prepare_features_for_prediction(df):
    df = df.drop(columns = ["click_event_id"])
    feature_cols = [f"I{i}" for i in range(1,14)] + [f"C{i}" for i in range(1,27)]

    return df[feature_cols]