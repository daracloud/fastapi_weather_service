from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import uuid4
from app.schemas import ProductCreateRequest, ProductResponse
from app.services import forecast as forecast_service

router = APIRouter()

# Simple in-memory store for demo purposes.
# In production replace with a persistent database.
_store = {}


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreateRequest):
    """
    Create a rainfall forecast product.
    """
    # generate forecast (replace with production model/API)
    f = forecast_service.generate_rainfall_forecast(
        lat=payload.location.lat,
        lon=payload.location.lon,
        forecast_date=payload.date,
    )

    prod_id = str(uuid4())
    product = {
        "id": prod_id,
        "name": payload.name,
        "location": payload.location.dict(),
        "date": payload.date,
        "forecast": {
            "rainfall_mm": f["rainfall_mm"],
            "probability": f["probability"],
        },
    }
    _store[prod_id] = product
    return product


@router.get("", response_model=List[ProductResponse])
def list_products(
    lat: Optional[float] = Query(None, description="Filter by latitude"),
    lon: Optional[float] = Query(None, description="Filter by longitude"),
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
):
    """
    List all products. If lat/lon/date are provided, filter roughly by equality.
    """
    results = list(_store.values())
    if lat is not None:
        results = [r for r in results if abs(r["location"]["lat"] - lat) < 1e-6]
    if lon is not None:
        results = [r for r in results if abs(r["location"]["lon"] - lon) < 1e-6]
    if date is not None:
        from datetime import datetime

        try:
            qdate = datetime.fromisoformat(date).date()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        results = [r for r in results if r["date"] == qdate]
    return results


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    """
    Retrieve a product by id.
    """
    product = _store.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product