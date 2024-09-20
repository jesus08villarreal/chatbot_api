# crud/company_crud.py
from models.company import Company
from database import companies_collection
from bson import ObjectId

# Crear una compañía
async def create_company(company: Company):
    company_data = company.dict()
    result = await companies_collection.insert_one(company_data)
    return str(result.inserted_id)

# Obtener compañías
async def get_companies():
    companies = []
    async for company in companies_collection.find():
        companies.append(Company(**company))
    return companies

# Obtener una compañía por nombre
async def get_company_by_name(name: str):
    company = await companies_collection.find_one({"name": name})
    if company:
        return Company(**company)

# Actualizar compañía
async def update_company(id: str, company: Company):
    await companies_collection.update_one({"_id": ObjectId(id)}, {"$set": company.dict()})

# Eliminar compañía
async def delete_company(id: str):
    await companies_collection.delete_one({"_id": ObjectId(id)})
