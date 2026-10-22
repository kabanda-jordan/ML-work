from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parent.parent / "dummy_data" / "vehicles_data_1000.csv"
REQUIRED_COLUMNS = {
    "vin",
    "manufacturer",
    "year",
    "color",
    "body_type",
    "engine_type",
    "transmission",
    "fuel_type",
    "seating_capacity",
    "price",
    "status",
    "registration_date",
}


def load_vehicle_data():
    dataframe = pd.read_csv(DATA_FILE)
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Vehicle CSV is missing required columns: {missing}")
    if dataframe.empty:
        raise ValueError(f"Vehicle CSV contains no records: {DATA_FILE}")
    return dataframe


def summarize_vehicles(dataframe):
    manufacturer_counts = (
        dataframe["manufacturer"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("manufacturer")
        .reset_index(name="count")
    )
    manufacturer_prices = (
        dataframe.groupby("manufacturer", dropna=False)["price"]
        .mean()
        .rename("average_price")
        .reset_index()
    )
    manufacturer_prices["manufacturer"] = manufacturer_prices[
        "manufacturer"
    ].fillna("Unknown")

    vehicles = dataframe.fillna("").to_dict(orient="records")
    for vehicle in vehicles:
        vehicle["price"] = f"${float(vehicle['price']):,.2f}"

    statuses = dataframe["status"].fillna("Unknown").value_counts()
    average_price = float(dataframe["price"].mean())

    return {
        "total_vehicles": len(dataframe),
        "active_vehicles": int(dataframe["status"].eq("active").sum()),
        "sold_vehicles": int(dataframe["status"].eq("sold").sum()),
        "average_price": f"${average_price:,.2f}",
        "manufacturer_rows": [
            {
                "manufacturer": str(row.manufacturer),
                "count": int(row.count),
            }
            for row in manufacturer_counts.itertuples(index=False)
        ],
        "vehicles": vehicles,
        "chart_data": {
            "manufacturer_labels": manufacturer_counts["manufacturer"].astype(str).tolist(),
            "manufacturer_counts": manufacturer_counts["count"].astype(int).tolist(),
            "status_labels": statuses.index.astype(str).tolist(),
            "status_counts": statuses.astype(int).tolist(),
            "price_labels": manufacturer_prices["manufacturer"].astype(str).tolist(),
            "average_prices": manufacturer_prices["average_price"].astype(float).tolist(),
        },
    }
