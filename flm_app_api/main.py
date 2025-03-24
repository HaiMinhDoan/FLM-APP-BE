from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import json
from flm_app_api.routers import users, sectors, pre_quotes, merchandises, agents

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["User"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(merchandises.router, prefix="/api", tags=["Merchandise"])
app.include_router(sectors.router, prefix="/api", tags=["Sector"])
app.include_router(pre_quotes.router, prefix="/api", tags=["PreQuote"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("flm_app_api.main:app", host="localhost", port=8080, reload=True)