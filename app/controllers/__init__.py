from fastapi import APIRouter
from app.controllers.auth import router as auth_router
from app.controllers.validate import router as validate_router
from app.controllers.dashboard import router as dashboard_router
from app.controllers.history import router as history_router
from app.controllers.users import router as users_router
from app.controllers.audit import router as audit_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(validate_router, prefix="/validate", tags=["Document Validation"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard & KPIs"])
api_router.include_router(history_router, prefix="/history", tags=["KYC History"])
api_router.include_router(users_router, prefix="/users", tags=["User Administration"])
api_router.include_router(audit_router, prefix="/audit", tags=["Security Audit Logs"])
