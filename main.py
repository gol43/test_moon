from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.ogranization_handlers import organization_router
from api.activity_handlers import activity_router
from api.buildings_handlers import buildings_router

from seed import seed_data


app = FastAPI(
    openapi_url="/api/v1/moon/openapi.json",
    docs_url="/api/v1/moon/docs"
)

app.include_router(organization_router, prefix='/api/v1/organizations', tags=['organizations'])
app.include_router(activity_router, prefix='/api/v1/activities', tags=['activities'])
app.include_router(buildings_router, prefix='/api/v1/buildings', tags=['buildings'])


@app.post("/api/v1/init_db")
async def init_db():
    try:
        await seed_data()
        return {"ok": True, "message": "База данных успешно созданна!"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})