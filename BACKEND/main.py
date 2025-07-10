from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from scraper.scheduler import start_scheduler

from models.user import Base
from database import engine
from routes import auth, leak_events, keyword, alerts

app = FastAPI(
    title="Data Sentinel API",
    version="1.0.0",
    description="API for Data Sentinel with JWT Authentication"
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include your routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(leak_events.router, prefix="/leak-events", tags=["Leak Events"])
app.include_router(keyword.router, prefix="/keywords", tags=["Keywords"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Data Sentinel!"}


# Custom OpenAPI to add global JWT bearer auth, excluding public endpoints
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Define Bearer Auth
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security globally, but exclude /, /auth/login, /auth/register
    public_paths = {"/", "/auth/login", "/auth/register"}
    for path in openapi_schema["paths"]:
        if path in public_paths:
            continue
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ✅ Wire the scheduler to run on startup
@app.on_event("startup")
async def on_startup():
    print("[Data Sentinel] Starting background scheduler...")
    start_scheduler()
