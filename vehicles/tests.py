import pandas as pd
from django.test import SimpleTestCase

from .dashboard import summarize_vehicles


class VehicleDashboardTests(SimpleTestCase):
    def test_summary_groups_manufacturers_and_statuses(self):
        dataframe = pd.DataFrame(
            {
                "vin": ["VIN-1", "VIN-2", "VIN-3"],
                "manufacturer": ["Toyota", "Ford", "Toyota"],
                "year": [2020, 2018, 2021],
                "color": ["black", "white", "silver"],
                "body_type": ["Sedan", "SUV", "Coupe"],
                "engine_type": ["petrol", "diesel", "electric"],
                "transmission": ["manual", "automatic", "manual"],
                "fuel_type": ["gasoline", "diesel", "electric"],
                "seating_capacity": [5, 7, 4],
                "price": [20000.0, 25000.0, 30000.0],
                "status": ["active", "sold", "inactive"],
                "registration_date": ["2020-05-20", "2018-07-15", "2021-01-10"],
            }
        )

        summary = summarize_vehicles(dataframe)

        self.assertEqual(summary["total_vehicles"], 3)
        self.assertEqual(summary["active_vehicles"], 1)
        self.assertEqual(summary["sold_vehicles"], 1)
        self.assertEqual(
            summary["manufacturer_rows"],
            [
                {"manufacturer": "Toyota", "count": 2},
                {"manufacturer": "Ford", "count": 1},
            ],
        )
        self.assertEqual(
            summary["chart_data"]["status_labels"],
            ["active", "sold", "inactive"],
        )
        self.assertEqual(
            summary["chart_data"]["price_labels"],
            ["Ford", "Toyota"],
        )
        self.assertEqual(
            summary["chart_data"]["average_prices"],
            [25000.0, 25000.0],
        )

    def test_dashboard_route_renders_csv_data(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vehicle Management Dashboard")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "1HGCM82633A123456")
