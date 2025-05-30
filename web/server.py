from fastapi import FastAPI, Request as FastAPIRequest, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from database.db import Session
from database.models import User, Request as DBRequest
from web.models import RequestModel
from utils.vless import generate_vless_string
from config.settings import BOT_TOKEN
from telegram import Bot
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uuid
import secrets
import logging
import json
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# JWT settings
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "securepassword123"

XRAY_CONFIG_PATH = "/opt/xray/config.json"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(request: FastAPIRequest):
    token = request.headers.get("Authorization", "").replace("Bearer ", "") or request.cookies.get("access_token")
    if not token:
        logger.debug("No token provided, redirecting to login")
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != ADMIN_USERNAME:
            logger.error("Invalid credentials")
            return None
        return username
    except JWTError:
        logger.error("Invalid token")
        return None

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: FastAPIRequest, username: str = Depends(verify_token)):
    if username:
        logger.debug("User already logged in, redirecting to /")
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: FastAPIRequest, username: str = Form(...), password: str = Form(...)):
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        logger.error("Login failed: Invalid credentials")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    access_token = create_access_token(data={"sub": username})
    logger.debug(f"Login successful, token: {access_token}")
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/", response_class=HTMLResponse)
async def admin_panel(request: FastAPIRequest, username: str = Depends(verify_token)):
    if not username:
        logger.debug("User not logged in, redirecting to /login")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    session = Session()
    db_requests = session.query(DBRequest).filter_by(status="pending").all()
    logger.debug(f"Found {len(db_requests)} pending requests")
    requests = []
    for req in db_requests:
        user = session.query(User).filter_by(id=req.user_id).first()
        req_data = RequestModel(
            id=req.id,
            user_id=req.user_id,
            username=user.username if user else "Unknown",
            comment=req.comment,
            status=req.status
        )
        requests.append(req_data)
    session.close()
    return templates.TemplateResponse("admin.html", {"request": request, "requests": requests})

'''def update_xray_config(user_id, key):
    config_path = "./xray/config.json"  # Локальный путь для обновления
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Добавляем клиента в конфигурацию
    client = {
        "id": str(key),
        "flow": "xtls-rprx-direct",
        "level": 0
    }
    config["inbounds"][0]["settings"]["clients"].append(client)
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    # Копируем обновлённую конфигурацию в контейнер
    os.system("docker cp ./xray/config.json xray:/opt/xray/config.json")
    os.system("docker restart xray")'''

def update_xray_config(user_id, key):
    pass

@app.post("/approve/{request_id}")
async def approve_request(request_id: int, username: str = Depends(verify_token)):
    if not username:
        logger.debug("User not logged in, redirecting to /login")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    session = Session()
    request = session.query(DBRequest).filter_by(id=request_id).first()
    if request:
        user = session.query(User).filter_by(id=request.user_id).first()
        user.vless_key = str(uuid.uuid4())
        user.is_active = True
        request.status = "approved"
        session.commit()
        
        # Обновляем конфигурацию Xray
        update_xray_config(user.telegram_id, user.vless_key)
        
        bot = Bot(token=BOT_TOKEN)
        vless_string = generate_vless_string(user.vless_key)
        await bot.send_message(
            chat_id=user.telegram_id,
            text=f"Ваша заявка одобрена!\nVLESS: {vless_string}"
        )
        logger.debug(f"Approved request ID {request_id}")
    else:
        logger.error(f"Request ID {request_id} not found")
    session.close()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/reject/{request_id}")
async def reject_request(request_id: int, username: str = Depends(verify_token)):
    if not username:
        logger.debug("User not logged in, redirecting to /login")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    session = Session()
    request = session.query(DBRequest).filter_by(id=request_id).first()
    if request:
        user = session.query(User).filter_by(id=request.user_id).first()
        request.status = "rejected"
        session.commit()
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            chat_id=user.telegram_id,
            text="Ваша заявка отклонена."
        )
        logger.debug(f"Rejected request ID {request_id}")
    else:
        logger.error(f"Request ID {request_id} not found")
    session.close()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)