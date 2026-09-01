"""
Sports Car Recommendation Engine Backend logic with SQLite database persistence.
"""

import sys
import json
import os

base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

try:
    from database import (
        init_db,
        get_recommendations as db_get_recommendations,
        save_favorite_car,
        get_favorites,
        add_new_car
    )
    init_db()
    USE_DB = True
except Exception as err:
    print(f"[WARN] Database fallback: {err}", file=sys.stderr)
    USE_DB = False


def get_recommendations_csv(u_time, u_price):
    import pandas as pd
    csv_path = os.path.join(base_path, "Sport car price.csv")
    if not os.path.exists(csv_path):
        return []
    df = pd.read_csv(csv_path)

    df["Price (in USD)"] = df["Price (in USD)"].astype(str).str.replace(r'[\$,"]', '', regex=True)
    df["Price (in USD)"] = pd.to_numeric(df["Price (in USD)"], errors="coerce")
    df["0-60 MPH Time (seconds)"] = pd.to_numeric(df["0-60 MPH Time (seconds)"], errors="coerce")
    df.dropna(subset=["Price (in USD)", "0-60 MPH Time (seconds)"], inplace=True)

    make_col = "Car Make" if "Car Make" in df.columns else "Car Name"
    affordable = df[df["Price (in USD)"] <= u_price].copy()
    if affordable.empty:
        affordable = df.copy()
    if affordable.empty:
        return []

    p_max = df["Price (in USD)"].max()
    t_max = df["0-60 MPH Time (seconds)"].max()

    affordable["score"] = (abs(affordable["Price (in USD)"] - u_price) / p_max * 0.8) + (abs(affordable["0-60 MPH Time (seconds)"] - u_time) / t_max * 0.2)
    affordable = affordable.sort_values("score")
    unique_cars = affordable.drop_duplicates(subset=[make_col, "Car Model"])

    results = []
    for _, row in unique_cars.head(5).iterrows():
        results.append({
            "Car_Name": str(row[make_col]),
            "Car_Model": str(row["Car Model"]),
            "Time": float(row["0-60 MPH Time (seconds)"]),
            "Price": float(row["Price (in USD)"])
        })
    return results


def get_recommendations(u_time, u_price):
    if USE_DB:
        try:
            return db_get_recommendations(u_time, u_price, top_n=5)
        except Exception as e:
            print(f"[WARN] Error querying DB: {e}", file=sys.stderr)
            return get_recommendations_csv(u_time, u_price)
    return get_recommendations_csv(u_time, u_price)


if __name__ == "__main__":
    try:
        # CLI routing
        if len(sys.argv) >= 2 and sys.argv[1] == "--favorites":
            print(json.dumps(get_favorites() if USE_DB else []))
        elif len(sys.argv) >= 3 and sys.argv[1] == "--save-fav":
            car_id = int(sys.argv[2])
            note = sys.argv[3] if len(sys.argv) > 3 else "Saved to Garage"
            success = save_favorite_car(car_id, note) if USE_DB else False
            print(json.dumps({"status": "success" if success else "error"}))
        elif len(sys.argv) >= 3:
            time_val = float(sys.argv[1])
            price_val = float(sys.argv[2])
            print(json.dumps(get_recommendations(time_val, price_val)))
        else:
            print(json.dumps([]))
    except Exception as e:
        print(json.dumps([]))
