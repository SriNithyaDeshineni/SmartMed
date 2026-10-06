from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import psycopg2
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from database import get_db_connection

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY or JWT_SECRET_KEY in {"your_new_jwt_secret", "your_generated_jwt_secret"}:
    raise RuntimeError("Set a private JWT_SECRET_KEY in backend/.env before starting the API")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
bearer_scheme = HTTPBearer(auto_error=False)


app = FastAPI(
    title="SmartMed API",
    description="Smart expired medicine disposal and tracking system",
    version="1.0.0"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# JWT AUTHENTICATION
# =========================

def create_access_token(subject_id: int, role: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {"sub": str(subject_id), "role": role, "exp": expires_at}
    return jwt.encode(claims, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_identity(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer token required",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        claims = jwt.decode(credentials.credentials, JWT_SECRET_KEY,
                             algorithms=[JWT_ALGORITHM])
        subject = claims.get("sub")
        role = claims.get("role")
        if not subject or role not in {"user", "admin"}:
            raise ValueError("Invalid token claims")
        identity_id = int(subject)
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"})
    return {"id": identity_id, "role": role}


def get_current_user(identity: dict = Depends(get_current_identity)):
    if identity["role"] != "user":
        raise HTTPException(status_code=403, detail="User access required")
    return identity


def get_current_admin(identity: dict = Depends(get_current_identity)):
    if identity["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return identity


# =========================
# REQUEST MODELS
# =========================

class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class DisposalRequest(BaseModel):
    user_id: int
    medicine_id: int
    quantity: int = 1
    expiry_date: str | None = None
    disposal_guidance: str | None = None


class TrackingStatusUpdate(BaseModel):
    status: str


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"message": "SmartMed Backend is running!"}


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# =========================
# SEARCH MEDICINES
# =========================

@app.get("/medicines/search")
def search_medicines(q: str = Query(..., min_length=1)):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT medicine_id, brand_name, medicine_type,
                           strength, package_size
                    FROM medicines
                    WHERE brand_name ILIKE %s
                    ORDER BY brand_name
                    LIMIT 20
                    """,
                    (f"%{q}%",)
                )
                return {"results": cur.fetchall()}

    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# GET MEDICINE DETAILS
# =========================

@app.get("/medicines/{medicine_id}")
def get_medicine(medicine_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT medicine_id, brand_name, medicine_type, slug,
                           dosage_form_id, generic_id, strength,
                           manufacturer_id, package_container, package_size
                    FROM medicines
                    WHERE medicine_id = %s
                    """,
                    (medicine_id,)
                )
                medicine = cur.fetchone()

                if medicine is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Medicine not found"
                    )

                return medicine

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# CREATE DISPOSAL REQUEST
# =========================

@app.post("/disposal-requests", status_code=201)
def create_disposal_request(payload: DisposalRequest, current_user: dict = Depends(get_current_user)):

    if payload.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You can only create requests for your own account")

    if payload.user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Valid user_id is required"
        )

    if payload.medicine_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Valid medicine_id is required"
        )

    if payload.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be a positive integer"
        )

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO disposal_requests
                        (user_id, medicine_id, quantity, expiry_date,
                         disposal_guidance)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING request_id, user_id, medicine_id, quantity,
                              expiry_date, disposal_guidance, status, created_at
                    """,
                    (
                        payload.user_id,
                        payload.medicine_id,
                        payload.quantity,
                        payload.expiry_date,
                        payload.disposal_guidance
                    )
                )
                return cur.fetchone()

    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=400,
            detail="User or medicine ID does not exist"
        )

    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# CREATE TRACKING
# =========================

@app.post("/tracking/{request_id}", status_code=201)
def create_tracking(request_id: int, current_user: dict = Depends(get_current_user)):
    tracking_code = "SM-" + uuid4().hex[:12].upper()

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT status, user_id
                    FROM disposal_requests
                    WHERE request_id = %s
                    """,
                    (request_id,)
                )
                request = cur.fetchone()

                if request is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Disposal request not found"
                    )
                if request["user_id"] != current_user["id"]:
                    raise HTTPException(status_code=403, detail="You can only track your own requests")

                cur.execute(
                    """
                    INSERT INTO tracking
                        (request_id, tracking_code, status)
                    VALUES (%s, %s, %s)
                    RETURNING tracking_id, request_id, tracking_code,
                              status, updated_at
                    """,
                    (
                        request_id,
                        tracking_code,
                        request["status"]
                    )
                )
                return cur.fetchone()

    except HTTPException:
        raise
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A tracking record already exists for this request"
        )
    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# GET TRACKING
# =========================

@app.get("/tracking/{tracking_code}")
def get_tracking(tracking_code: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT t.tracking_id, t.request_id, t.tracking_code,
                           t.status, t.updated_at,
                           d.medicine_id, d.quantity, d.expiry_date
                    FROM tracking t
                    JOIN disposal_requests d
                      ON t.request_id = d.request_id
                    WHERE t.tracking_code = %s
                    """,
                    (tracking_code,)
                )
                tracking = cur.fetchone()

                if tracking is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Tracking code not found"
                    )

                return tracking

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# UPDATE TRACKING STATUS
# =========================

@app.put("/tracking/{tracking_code}/status")
def update_tracking_status(
    tracking_code: str,
    payload: TrackingStatusUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    new_status = payload.status.upper()

    allowed_statuses = [
        "REQUESTED",
        "APPROVED",
        "COLLECTED",
        "DISPOSED",
        "REJECTED"
    ]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    UPDATE tracking
                    SET status = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE tracking_code = %s
                    RETURNING tracking_id, request_id, tracking_code,
                              status, updated_at
                    """,
                    (new_status, tracking_code)
                )
                tracking = cur.fetchone()

                if tracking is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Tracking code not found"
                    )

                cur.execute(
                    """
                    UPDATE disposal_requests
                    SET status = %s
                    WHERE request_id = %s
                    """,
                    (new_status, tracking["request_id"])
                )

                return tracking

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# GET USER DISPOSAL REQUESTS
# =========================

@app.get("/users/{user_id}/disposal-requests")
def get_user_disposal_requests(user_id: int, current_user: dict = Depends(get_current_user)):
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You can only view your own requests")

    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Valid user_id is required"
        )

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        d.request_id,
                        d.user_id,
                        d.medicine_id,
                        m.brand_name,
                        m.strength,
                        d.quantity,
                        d.expiry_date,
                        d.disposal_guidance,
                        d.status,
                        d.created_at
                    FROM disposal_requests d
                    JOIN medicines m
                        ON d.medicine_id = m.medicine_id
                    WHERE d.user_id = %s
                    ORDER BY d.created_at DESC
                    """,
                    (user_id,)
                )

                return {
                    "user_id": user_id,
                    "requests": cur.fetchall()
                }

    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# ADMIN: GET ALL REQUESTS
# =========================

@app.get("/admin/disposal-requests")
def get_all_disposal_requests(current_admin: dict = Depends(get_current_admin)):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        d.request_id,
                        d.user_id,
                        u.name AS user_name,
                        u.email,
                        d.medicine_id,
                        m.brand_name,
                        m.strength,
                        d.quantity,
                        d.expiry_date,
                        d.disposal_guidance,
                        d.status,
                        d.created_at
                    FROM disposal_requests d
                    JOIN users u
                        ON d.user_id = u.user_id
                    JOIN medicines m
                        ON d.medicine_id = m.medicine_id
                    ORDER BY d.created_at DESC
                    """
                )

                return {"requests": cur.fetchall()}

    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# USER REGISTRATION
# =========================

@app.post("/users/register", status_code=201)
def register_user(user: UserRegistration):

    if len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    if not user.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    password_hash = pwd_context.hash(user.password)

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO users (name, email, password_hash, phone)
                    VALUES (%s, %s, %s, %s)
                    RETURNING user_id, name, email, phone, created_at
                    """,
                    (
                        user.name.strip(),
                        str(user.email).lower(),
                        password_hash,
                        user.phone
                    )
                )

                return cur.fetchone()

    except psycopg2.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists"
        )

    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )


# =========================
# USER LOGIN
# =========================

@app.post("/users/login")
def login_user(user: UserLogin):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT user_id, name, email, password_hash
                    FROM users
                    WHERE LOWER(email) = LOWER(%s)
                    """,
                    (str(user.email),)
                )

                db_user = cur.fetchone()

                if db_user is None:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid email or password"
                    )

                try:
                    password_is_valid = pwd_context.verify(
                        user.password,
                        db_user["password_hash"]
                    )
                except (ValueError, TypeError):
                    password_is_valid = False

                if not password_is_valid:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid email or password"
                    )

                token = create_access_token(db_user["user_id"], "user")
                return {
                    "message": "Login successful",
                    "access_token": token,
                    "token_type": "bearer",
                    "user_id": db_user["user_id"],
                    "name": db_user["name"],
                    "email": db_user["email"]
                }

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )

# =========================
# ADMIN LOGIN
# =========================

@app.post("/admin/login")
def login_admin(user: UserLogin):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT admin_id, name, email, password_hash
                    FROM admins
                    WHERE LOWER(email) = LOWER(%s)
                    """,
                    (str(user.email),)
                )
                db_admin = cur.fetchone()

                if db_admin is None:
                    raise HTTPException(status_code=401, detail="Invalid email or password")

                try:
                    password_is_valid = pwd_context.verify(
                        user.password, db_admin["password_hash"]
                    )
                except (ValueError, TypeError):
                    password_is_valid = False

                if not password_is_valid:
                    raise HTTPException(status_code=401, detail="Invalid email or password")

                token = create_access_token(db_admin["admin_id"], "admin")
                return {
                    "message": "Admin login successful",
                    "access_token": token,
                    "token_type": "bearer",
                    "admin_id": db_admin["admin_id"],
                    "name": db_admin["name"],
                    "email": db_admin["email"]
                }

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database query failed")
