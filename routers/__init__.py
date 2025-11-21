from fastapi import FastAPI
from routers.userRoute import router as  userRoute
from routers.candidatRoute import router as  candidatRoute
from routers.offreRoute import router as  offreRoute
from routers.matchingRoute import router as  matchingRoute
from routers.auth import router as  authRoute
from routers.extractRoute import router as  extractRoute

ROUTERS = [
    userRoute,
    candidatRoute,
    offreRoute,
    matchingRoute,
    authRoute,
    extractRoute
]

def include_routes(app: FastAPI, api_prefix: str = "/api"):
    for router in ROUTERS:
        app.include_router(router, prefix=api_prefix)
