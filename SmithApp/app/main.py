from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.database import engine, Base, get_db
from api.endpoints import auth, users
from api.deps import get_optional_current_user, get_current_user
from schemas.user import SA_PROVINCES

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Law Firm Management System")

# Middleware & Static Files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include API Routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

# ============================================================================
# FRONTEND PAGE ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request, user: dict = Depends(get_optional_current_user)):
    """Login page - Redirects to home if already logged in"""
    if user:
        return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request, user: dict = Depends(get_current_user)):
    """Home dashboard"""
    return templates.TemplateResponse("home.html", {"request": request, "user": user})

@app.get("/users/add", response_class=HTMLResponse)
async def add_user_page(request: Request, user: dict = Depends(get_current_user)):
    """Form to add a new user"""
    return templates.TemplateResponse(
        "users/add_user.html", 
        {"request": request, "user": user, "provinces": SA_PROVINCES}
    )

@app.get("/users/manage", response_class=HTMLResponse)
async def manage_users_page(
    request: Request, 
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """User listing with management options"""
    from services.user_service import UserService
    users_list = UserService.get_all_users(db)
    return templates.TemplateResponse(
        "users/manage_users.html", 
        {"request": request, "user": user, "users": users_list}
    )

@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_page(
    request: Request, 
    user_id: int, 
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Edit existing user details"""
    from services.user_service import UserService
    user_data = UserService.get_user_by_id(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "users/edit_user.html", 
        {"request": request, "user": user, "user_data": user_data}
    )

@app.get("/users/delete/{user_id}", response_class=HTMLResponse)
async def delete_user_page(
    request: Request, 
    user_id: int, 
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Confirmation page for user deletion"""
    from services.user_service import UserService
    user_data = UserService.get_user_by_id(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "users/delete_user.html", 
        {"request": request, "user": user, "user_data": user_data}
    )

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    if "text/html" in request.headers.get("accept", ""):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc.detail)}
    )


# ============================================================================
# UTILITY ROUTES
# ============================================================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "software": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
