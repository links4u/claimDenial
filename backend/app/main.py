"""
ClaimPilot™ FastAPI Application

Main application entry point.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import structlog

from app.core.config import settings
from app.db.session import engine, Base
from app.api import claims, appeals, policies, audit

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("application_startup", version="1.0.0")
    
    # Create tables (in production, use Alembic migrations)
    # Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    logger.info("application_shutdown")


# =====================================================
# Create FastAPI Application
# =====================================================

app = FastAPI(
    title="ClaimPilot™ API",
    description="Agentic AI Platform for Professional Claim Denial Intelligence & Appeal Automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# =====================================================
# CORS Middleware
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Health Check Endpoint
# =====================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        from app.db.session import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return JSONResponse(
        status_code=200 if db_status == "healthy" else 503,
        content={
            "status": "healthy" if db_status == "healthy" else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_status,
            "version": "1.0.0"
        }
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ClaimPilot™ API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# =====================================================
# Include Routers
# =====================================================

app.include_router(claims.router, prefix="/api/v1/claims", tags=["Claims"])
app.include_router(appeals.router, prefix="/api/v1/appeals", tags=["Appeals"])
app.include_router(policies.router, prefix="/api/v1/policies", tags=["Policies"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])


# =====================================================
# Global Exception Handler
# =====================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all uncaught exceptions."""
    logger.error(
        "unhandled_exception",
        path=str(request.url),
        method=request.method,
        error=str(exc)
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
