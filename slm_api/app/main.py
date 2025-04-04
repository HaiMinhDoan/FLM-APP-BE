from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import json
from app.routers import users, sectors, pre_quotes, merchandises, agents, customers, contents, brands, mini_admins
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(users.router, prefix="/api", tags=["User"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(merchandises.router, prefix="/api", tags=["Merchandise"])
app.include_router(sectors.router, prefix="/api", tags=["Sector"])
app.include_router(pre_quotes.router, prefix="/api", tags=["PreQuote"])
app.include_router(customers.router, prefix="/api", tags=["Customer"])
app.include_router(contents.router, prefix="/api", tags=["Content"])
app.include_router(brands.router, prefix="/api", tags=["Brand"])
app.include_router(mini_admins.router, prefix="/api", tags=["Mini Admin"])
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Danh sách nguồn được phép
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các header
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)