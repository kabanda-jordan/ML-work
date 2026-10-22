# Vehicle Management Dashboard

A Django dashboard that reads vehicle records from `dummy_data/vehicles_data_1000.csv` and displays fleet metrics, manufacturer frequency, and charts.

## Run locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser. The example CSV contains the three vehicle records provided with the project request; replace it with additional rows using the same column headers to display a larger dataset.

## Test

```powershell
python manage.py test
```
