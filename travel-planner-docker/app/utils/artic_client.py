import httpx
from fastapi import HTTPException

ARTIC_API_URL = "https://api.artic.edu/api/v1"

async def check_place_exists(external_id: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{ARTIC_API_URL}/artworks/{external_id}")
            return response.status_code == 200
    except:
        return False 

async def get_place_info(external_id: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{ARTIC_API_URL}/artworks/{external_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Place with id {external_id} not found")
        return response.json()