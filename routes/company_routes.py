# routes/company_route.py
from fastapi import APIRouter, HTTPException
from crud.company_crud import create_company, get_companies, update_company, delete_company
from models.company import Company

router = APIRouter()

@router.post("/companies/")
async def create_new_company(company: Company):
    return await create_company(company)

@router.get("/companies/")
async def get_all_companies():
    return await get_companies()

@router.put("/companies/{id}")
async def update_company_data(id: str, company: Company):
    await update_company(id, company)
    return {"message": "Company updated"}

@router.delete("/companies/{id}")
async def delete_company_data(id: str):
    await delete_company(id)
    return {"message": "Company deleted"}
