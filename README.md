```markdown
# Weather Service - Rainfall Forecast API (FastAPI)

Simple FastAPI app that exposes `/products` endpoints to create and retrieve rainfall-forecast products.

Requirements
- Python 3.9+
- Install dependencies: `pip install -r requirements.txt`

Run locally
- Start server:
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

API
- POST /products
  - Create a rainfall forecast product.
  - Request JSON:
    {
      "name": "Forecast for city X",
      "location": {"lat": 51.5, "lon": -0.1},
      "date": "2026-01-16"
    }
- GET /products
  - List products or query forecasts with `lat`, `lon`, and `date` query parameters.
- GET /products/{product_id}
  - Get a single product by id.

Notes
- Forecast implementation is a stub (deterministic placeholder). Replace `app.services.forecast.generate_rainfall_forecast` with your model or external API call.
```