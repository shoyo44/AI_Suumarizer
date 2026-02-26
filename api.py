"""
AI Summarizer — FastAPI Backend
- Cloudflare Workers AI for LLM analysis
- Firebase Admin SDK for authentication
- MongoDB Atlas for storing analysis history
"""

import json
import os
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx
import certifi
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

# ── Load environment variables ──────────────────────────────────────────────
load_dotenv()

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_MODEL = "@cf/meta/llama-3.1-8b-instruct"
MONGODB_URI = os.getenv("MONGODB_URI")

if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
    raise RuntimeError(
        "Missing CLOUDFLARE_ACCOUNT_ID or CLOUDFLARE_API_TOKEN in .env file"
    )
if not MONGODB_URI:
    raise RuntimeError("Missing MONGODB_URI in .env file")

CLOUDFLARE_API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{CLOUDFLARE_MODEL}"
)

# ── Initialize Firebase Admin SDK ───────────────────────────────────────────
SERVICE_ACCOUNT_PATH = Path(__file__).parent / "serviceAccountKey.json"
cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
firebase_admin.initialize_app(cred)

# ── Initialize MongoDB (async via Motor) ────────────────────────────────────
mongo_client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
db = mongo_client["ai_summarizer"]
history_collection = db["analysis_history"]
users_collection = db["users"]

# ── Load use cases from JSON ────────────────────────────────────────────────
JSON_PATH = Path(__file__).parent / "ai_summarizer_usecases.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    _config = json.load(f)

USECASES: dict[str, dict] = {uc["id"]: uc for uc in _config["usecases"]}
GLOBAL_SETTINGS = _config["global_settings"]
SYSTEM_INSTRUCTION = GLOBAL_SETTINGS["system_instruction"]

# ── FastAPI App ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Summarizer API",
    description="Analyze text using AI-powered use cases. Firebase auth + MongoDB history.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Logger ──────────────────────────────────────────────────────────────────
logger = logging.getLogger("uvicorn.error")


# ── Health check helpers ────────────────────────────────────────────────────
async def check_mongodb() -> dict:
    """Ping MongoDB and verify indexes."""
    try:
        result = await db.command("ping")
        if result.get("ok") == 1.0:
            # Ensure indexes exist
            await history_collection.create_index([("user_uid", 1), ("created_at", -1)])
            await users_collection.create_index("uid", unique=True)
            idx = await history_collection.index_information()
            return {"status": "✅ connected", "database": db.name, "indexes": list(idx.keys())}
        return {"status": "❌ ping failed"}
    except Exception as e:
        return {"status": f"❌ error: {e}"}


async def check_cloudflare() -> dict:
    """Send a tiny test request to Cloudflare Workers AI."""
    try:
        payload = {
            "messages": [{"role": "user", "content": "Say OK"}],
            "max_tokens": 5,
        }
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(CLOUDFLARE_API_URL, json=payload, headers=headers)
        if resp.status_code == 200 and resp.json().get("success"):
            return {"status": "✅ connected", "model": CLOUDFLARE_MODEL}
        return {"status": f"❌ API returned {resp.status_code}", "body": resp.text[:200]}
    except Exception as e:
        return {"status": f"❌ error: {e}"}


def check_firebase() -> dict:
    """Verify Firebase Admin SDK is initialized."""
    try:
        fb_app = firebase_admin.get_app()
        return {
            "status": "✅ initialized",
            "project_id": fb_app.project_id,
        }
    except Exception as e:
        return {"status": f"❌ error: {e}"}


def check_usecases() -> dict:
    """Verify use cases loaded from JSON."""
    count = len(USECASES)
    ids = list(USECASES.keys())
    return {"status": f"✅ {count} use cases loaded", "ids": ids}


# ── Startup / Shutdown ─────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_diagnostics():
    """Run full diagnostics on startup."""
    logger.info("═" * 60)
    logger.info("  AI Summarizer — Startup Diagnostics")
    logger.info("═" * 60)

    # 1. Firebase
    fb = check_firebase()
    logger.info(f"  Firebase Admin SDK : {fb['status']}")
    if "project_id" in fb:
        logger.info(f"    Project ID       : {fb['project_id']}")

    # 2. MongoDB
    mongo = await check_mongodb()
    logger.info(f"  MongoDB            : {mongo['status']}")
    if "indexes" in mongo:
        logger.info(f"    Database         : {mongo['database']}")
        logger.info(f"    Indexes          : {mongo['indexes']}")

    # 3. Cloudflare Workers AI
    cf = await check_cloudflare()
    logger.info(f"  Cloudflare AI      : {cf['status']}")
    if "model" in cf:
        logger.info(f"    Model            : {cf['model']}")

    # 4. Use cases
    uc = check_usecases()
    logger.info(f"  Use Cases          : {uc['status']}")

    logger.info("═" * 60)
    logger.info("  All checks complete. Server is ready.")
    logger.info("═" * 60)


@app.on_event("shutdown")
async def shutdown_db():
    mongo_client.close()


# ── Firebase Auth Dependency ────────────────────────────────────────────────
security = HTTPBearer()


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify Firebase ID token from Authorization header."""
    token = credentials.credentials
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token has expired. Please sign in again.")
    except firebase_auth.RevokedIdTokenError:
        raise HTTPException(status_code=401, detail="Token has been revoked. Please sign in again.")
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not verify credentials.")


# ── Models ──────────────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=GLOBAL_SETTINGS["max_input_length"])
    usecase_id: str
    target_language: Optional[str] = None


class UsecaseInfo(BaseModel):
    id: str
    name: str
    description: str
    output_format: str
    category: str
    extra_params: list[str] = []


class AnalyzeResponse(BaseModel):
    usecase_id: str
    usecase_name: str
    result: str
    user_email: Optional[str] = None
    history_id: Optional[str] = None


class HistoryItem(BaseModel):
    id: str
    usecase_id: str
    usecase_name: str
    input_preview: str
    input_text: str
    result: str
    created_at: str


class UserInfo(BaseModel):
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    total_analyses: int = 0


# ── Helper: call Cloudflare Workers AI ──────────────────────────────────────
async def call_llm(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 2048,
        "temperature": GLOBAL_SETTINGS["temperature"],
        "top_p": GLOBAL_SETTINGS["top_p"],
    }

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(CLOUDFLARE_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Cloudflare API error ({response.status_code}): {response.text}",
        )

    data = response.json()
    if not data.get("success"):
        raise HTTPException(status_code=502, detail=f"Cloudflare AI errors: {data.get('errors', [])}")

    return data["result"]["response"]


# ── Helper: save/update user in MongoDB ─────────────────────────────────────
async def track_user(decoded_token: dict):
    """Upsert user profile in MongoDB on every authenticated request."""
    await users_collection.update_one(
        {"uid": decoded_token["uid"]},
        {
            "$set": {
                "email": decoded_token.get("email"),
                "name": decoded_token.get("name"),
                "picture": decoded_token.get("picture"),
                "last_active": datetime.now(timezone.utc),
            },
            "$setOnInsert": {
                "uid": decoded_token["uid"],
                "created_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


# ── Public Routes ───────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "AI Summarizer API is running",
        "docs": "/docs",
        "health": "/health",
        "usecases_endpoint": "/usecases",
    }


@app.get("/health")
async def health_check():
    """Live health check — verifies all service connections on demand."""
    mongo = await check_mongodb()
    cf = await check_cloudflare()
    fb = check_firebase()
    uc = check_usecases()

    all_ok = all(
        s.get("status", "").startswith("✅")
        for s in [mongo, cf, fb, uc]
    )

    return {
        "status": "healthy" if all_ok else "degraded",
        "services": {
            "firebase": fb,
            "mongodb": mongo,
            "cloudflare_ai": cf,
            "usecases": uc,
        },
    }


@app.get("/usecases", response_model=list[UsecaseInfo])
async def list_usecases():
    """List all available analysis use cases (public)."""
    return [
        UsecaseInfo(
            id=uc["id"],
            name=uc["name"],
            description=uc["description"],
            output_format=uc["output_format"],
            category=uc["category"],
            extra_params=uc.get("extra_params", []),
        )
        for uc in _config["usecases"]
    ]


# ── Protected Routes ───────────────────────────────────────────────────────
@app.get("/me", response_model=UserInfo)
async def get_current_user(user: dict = Depends(verify_firebase_token)):
    """Returns authenticated user info + total analysis count."""
    await track_user(user)
    total = await history_collection.count_documents({"user_uid": user["uid"]})
    return UserInfo(
        uid=user["uid"],
        email=user.get("email"),
        name=user.get("name"),
        picture=user.get("picture"),
        total_analyses=total,
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(
    request: AnalyzeRequest,
    user: dict = Depends(verify_firebase_token),
):
    """Analyze text with a use case — saves result to MongoDB history."""

    # Validate use case
    usecase = USECASES.get(request.usecase_id)
    if not usecase:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown usecase_id '{request.usecase_id}'. Available: {list(USECASES.keys())}",
        )

    # Build prompt
    user_prompt = usecase["prompt_template"].replace("{input_text}", request.text)

    if "target_language" in usecase.get("extra_params", []):
        if not request.target_language:
            raise HTTPException(status_code=400, detail="'target_language' is required for this use case.")
        user_prompt = user_prompt.replace("{target_language}", request.target_language)

    # Call LLM
    result = await call_llm(SYSTEM_INSTRUCTION, user_prompt)

    # Save to MongoDB history
    history_doc = {
        "user_uid": user["uid"],
        "user_email": user.get("email"),
        "usecase_id": request.usecase_id,
        "usecase_name": usecase["name"],
        "input_text": request.text,
        "result": result,
        "target_language": request.target_language,
        "created_at": datetime.now(timezone.utc),
    }
    insert_result = await history_collection.insert_one(history_doc)

    # Track user activity
    await track_user(user)

    return AnalyzeResponse(
        usecase_id=request.usecase_id,
        usecase_name=usecase["name"],
        result=result,
        user_email=user.get("email"),
        history_id=str(insert_result.inserted_id),
    )


@app.get("/history", response_model=list[HistoryItem])
async def get_history(
    user: dict = Depends(verify_firebase_token),
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
):
    """Get the authenticated user's analysis history (most recent first)."""
    cursor = (
        history_collection.find({"user_uid": user["uid"]})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    items = []
    async for doc in cursor:
        items.append(
            HistoryItem(
                id=str(doc["_id"]),
                usecase_id=doc["usecase_id"],
                usecase_name=doc["usecase_name"],
                input_preview=doc["input_text"][:150] + ("..." if len(doc["input_text"]) > 150 else ""),
                input_text=doc["input_text"],
                result=doc["result"],
                created_at=doc["created_at"].isoformat(),
            )
        )
    return items


@app.delete("/history/{history_id}")
async def delete_history_item(
    history_id: str,
    user: dict = Depends(verify_firebase_token),
):
    """Delete a specific history entry (only the owner can delete)."""
    from bson import ObjectId

    result = await history_collection.delete_one(
        {"_id": ObjectId(history_id), "user_uid": user["uid"]}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="History item not found.")
    return {"message": "Deleted successfully."}


# ── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
