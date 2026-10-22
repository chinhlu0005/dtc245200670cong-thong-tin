from fastapi import FastAPI, Depends, Request, HTTPException, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(user_session: Optional[str] = Cookie(None)):
    return user_session

# Trang chủ
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    posts = db.query(models.Post).order_by(models.Post.id.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts, "user": current_user})

# Tìm kiếm bài viết
@app.get("/search", response_class=HTMLResponse)
def search_posts(request: Request, keyword: Optional[str] = "", db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    posts = db.query(models.Post).filter(
        models.Post.title.ilike(f"%{keyword}%") | models.Post.content.ilike(f"%{keyword}%")
    ).order_by(models.Post.id.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts, "user": current_user, "keyword": keyword})

# Lọc bài viết theo chuyên mục
@app.get("/category/{cat_name}", response_class=HTMLResponse)
def read_category(request: Request, cat_name: str, db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.category == cat_name).order_by(models.Post.id.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts, "user": current_user})

# Chi tiết bài viết
@app.get("/posts/{post_id}", response_class=HTMLResponse)
def read_post(request: Request, post_id: int, db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    
    post.views_count += 1
    db.commit()
    return templates.TemplateResponse(request, "detail.html", {"post": post, "user": current_user})

# Giao diện viết bài (BẮT BUỘC ĐĂNG NHẬP)
@app.get("/writer/new", response_class=HTMLResponse)
def new_post_form(request: Request, current_user: Optional[str] = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/auth/login?msg=required", status_code=303)
    return templates.TemplateResponse(request, "writer/create.html", {"user": current_user})

# Xử lý lưu bài viết
@app.post("/writer/new")
def create_post(
    title: str = Form(...), 
    summary: str = Form(...), 
    content: str = Form(...), 
    category: str = Form("thoisu"), 
    db: Session = Depends(get_db),
    current_user: Optional[str] = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/auth/login?msg=required", status_code=303)
        
    new_post = models.Post(title=title, summary=summary, content=content, category=category)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Trang Đăng nhập
@app.get("/auth/login", response_class=HTMLResponse)
def login_page(request: Request, msg: Optional[str] = None):
    error_msg = "Vui lòng đăng nhập tài khoản để có thể đăng bài viết!" if msg == "required" else None
    return templates.TemplateResponse(request, "auth/login.html", {"error": error_msg})

# Xử lý Đăng nhập
@app.post("/auth/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username, models.User.password == password).first()
    if not user:
        return templates.TemplateResponse(request, "auth/login.html", {"error": "Tên đăng nhập hoặc mật khẩu không đúng!"})
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_session", value=user.username)
    return response

# Trang Đăng ký
@app.get("/auth/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "auth/register.html", {"error": None})

# Xử lý Đăng ký
@app.post("/auth/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse(request, "auth/register.html", {"error": "Tên đăng nhập này đã được sử dụng!"})
    
    new_user = models.User(username=username, password=password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/auth/login", status_code=303)

# Đăng xuất
@app.get("/auth/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_session")
    return response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(user_session: Optional[str] = Cookie(None)):
    return user_session

# Trang chủ
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    posts = db.query(models.Post).order_by(models.Post.id.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts, "user": current_user})

# Tìm kiếm bài viết
@app.get("/search", response_class=HTMLResponse)
def search_posts(request: Request, keyword: Optional[str] = "", db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    posts = db.query(models.Post).filter(
        models.Post.title.ilike(f"%{keyword}%") | models.Post.content.ilike(f"%{keyword}%")
    ).order_by(models.Post.id.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts, "user": current_user, "keyword": keyword})

# Lọc bài viết theo chuyên mục
@app.get("/category/{cat_name}", response_class=HTMLResponse)
def read_category(request: Request, cat_name: str, db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.category == cat_name).order_by(models.Post.id.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts, "user": current_user})

# Chi tiết bài viết
@app.get("/posts/{post_id}", response_class=HTMLResponse)
def read_post(request: Request, post_id: int, db: Session = Depends(get_db), current_user: Optional[str] = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    
    post.views_count += 1
    db.commit()
    return templates.TemplateResponse(request, "detail.html", {"post": post, "user": current_user})

# Giao diện viết bài (BẮT BUỘC ĐĂNG NHẬP)
@app.get("/writer/new", response_class=HTMLResponse)
def new_post_form(request: Request, current_user: Optional[str] = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/auth/login?msg=required", status_code=303)
    return templates.TemplateResponse(request, "writer/create.html", {"user": current_user})

# Xử lý lưu bài viết
@app.post("/writer/new")
def create_post(
    title: str = Form(...), 
    summary: str = Form(...), 
    content: str = Form(...), 
    category: str = Form("thoisu"), 
    db: Session = Depends(get_db),
    current_user: Optional[str] = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/auth/login?msg=required", status_code=303)
        
    new_post = models.Post(title=title, summary=summary, content=content, category=category)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Trang Đăng nhập
@app.get("/auth/login", response_class=HTMLResponse)
def login_page(request: Request, msg: Optional[str] = None):
    error_msg = "Vui lòng đăng nhập tài khoản để có thể đăng bài viết!" if msg == "required" else None
    return templates.TemplateResponse(request, "auth/login.html", {"error": error_msg})

# Xử lý Đăng nhập
@app.post("/auth/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username, models.User.password == password).first()
    if not user:
        return templates.TemplateResponse(request, "auth/login.html", {"error": "Tên đăng nhập hoặc mật khẩu không đúng!"})
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_session", value=user.username)
    return response

# Trang Đăng ký
@app.get("/auth/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "auth/register.html", {"error": None})

# Xử lý Đăng ký
@app.post("/auth/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse(request, "auth/register.html", {"error": "Tên đăng nhập này đã được sử dụng!"})
    
    new_user = models.User(username=username, password=password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/auth/login", status_code=303)

# Đăng xuất
@app.get("/auth/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_session")
    return response