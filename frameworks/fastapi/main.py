# Acknowledgements____
# Feeding my own work and youtube tutorials into ChatGPT to catch
# blindspots
# ChatGPT - model o3


"""
FastAPI Concepts Tutorial
=====================================
This single file demonstrates **five additional concepts** that senior
Python engineers are expected to know *beyond* the introductory CRUD
sample you already built.  Each concept is introduced with *teaching-style*
commentary so you can treat the file itself as a living notebook.

Run with:
    uvicorn main:app --reload

New concepts covered
--------------------
1. **AsyncIO & cooperative concurrency** - high-throughput I/O without
   blocking the event loop.
2. **Dependency Injection (DI) with `Depends`** - structuring reusable
   components and keeping handlers thin.
3. **Middleware & custom exception handling** - cross-cutting concerns
   and graceful error responses.
4. **Testing FastAPI with PyTest** - fixtures, async test clients, and
   why TDD matters.
5. **Modern static typing with Pydantic generics** - self-documenting
   contracts that super-charge editor tooling and catch bugs early.

Anything prefixed with "###" is a *teaching block*; skim them later if
you only need the code.
"""

# ---------------------------------------------------------------------------
# Imports – stdlib, external libs, local
# ---------------------------------------------------------------------------
import asyncio
from typing import List, Generic, Optional, TypeVar, Annotated

import httpx  # third‑party async HTTP client
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Path,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel  # for v1/v2 compatibility

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(title="FastAPI Demo")

# Middleware is *application‑wide* glue for cross‑cutting concerns like
# CORS, auth, or request timing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Never do this in prod; restrict your domains!
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Existing beginner CRUD sample (lightly cleaned up)
# ---------------------------------------------------------------------------


class Item(BaseModel):
    """A to-do item - unchanged from your starter project."""

    text: str = Field(..., max_length=60)
    is_done: bool = False


items: List[Item] = []


@app.get("/")
async def root():
    return {"hello": "world"}


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items", response_model=List[Item])
async def list_items(limit: int = 10):
    return items[:limit]


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: Annotated[int, Path(ge=0, lt=1_000_000)]):
    try:
        return items[item_id]
    except IndexError as exc:
        raise HTTPException(status_code=404, detail="Item not found") from exc


# ---------------------------------------------------------------------------
# 1️⃣  AsyncIO & cooperative concurrency
# ---------------------------------------------------------------------------
# Why it matters
# Senior engineers must squeeze maximum throughput from a single process.
# When most of your time is spent *waiting* (DB calls, remote APIs), async I/O
# lets other tasks run instead of blocking a thread.

T = TypeVar("T")


async def fetch_url(session: httpx.AsyncClient, url: str) -> str:
    """Pretend we scrape a page - realistically you'll return JSON, etc."""
    resp = await session.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text[:80]  # first 80 chars for brevity


async def fetch_many(urls: List[str]) -> List[str]:
    async with httpx.AsyncClient() as session:
        return await asyncio.gather(*(fetch_url(session, u) for u in urls))


@app.get("/scrape")
async def scrape(urls: str):
    """Comma-separated list of URLs -> concurrent scrape."""
    results = await fetch_many(urls.split(","))
    return {"results": results}

# ---------------------------------------------------------------------------
# 2️⃣  Dependency Injection (DI) with Depends
# ---------------------------------------------------------------------------
# Why it matters
# DI keeps handlers thin, testable, and single‑responsibility by pushing IO
# and config lookups into provider functions that FastAPI wires up.


class Settings(BaseModel):
    app_name: str = "DemoApp"
    debug: bool = True


def get_settings() -> Settings:  # could pull from env or secrets manager
    return Settings()


@app.get("/settings")
async def read_settings(settings: Settings = Depends(get_settings)):
    return settings

# ---------------------------------------------------------------------------
# 3️⃣  Middleware & custom exception handling
# ---------------------------------------------------------------------------
# Why it matters
# Production APIs need consistent error shapes and observability. Middleware
# runs *around* every request; exception handlers translate uncaught errors
# to JSON responses so clients never see default HTML stack traces.

# TODO: Mezmorize this


class ExternalServiceError(Exception):
    """Raised when a downstream service returns 5xx."""


@app.exception_handler(ExternalServiceError)
async def ext_service_exception_handler(_: Request, exc: ExternalServiceError):
    return JSONResponse(
        status_code=503,
        content={"error": "external_service_unavailable", "detail": str(exc)},
    )

# ---------------------------------------------------------------------------
# 4️⃣  Testing with PyTest
# ---------------------------------------------------------------------------
# Why it matters
# Confidence to refactor fast comes from *fast* feedback loops. Below is a
# template you can paste into `test_app.py`.
#
# See test_app.py

# ---------------------------------------------------------------------------
# 5️⃣  Static typing & Pydantic generics
# ---------------------------------------------------------------------------
# Why it matters
# Type hints unlock IDE auto‑complete, refactoring safety, and runtime schema
# generation.  FastAPI still expects **Pydantic v1‑style generics**, so we use
# `GenericModel` for broad compatibility.  If you upgrade to FastAPI > 0.111
# *and* Pydantic v2, this continues to work.


class APIResponse(GenericModel, Generic[T]):  # Note GenericModel first
    data: T
    success: bool = True


@app.get("/items/{item_id}/wrap", response_model=APIResponse[Item])
async def get_wrapped_item(item_id: int):
    try:
        return APIResponse(data=items[item_id])
    except IndexError as exc:
        raise HTTPException(status_code=404, detail="Item not found") from exc

# ---------------------------------------------------------------------------
#  ⚡  Quick performance tip
# ---------------------------------------------------------------------------
# Want 2–10× more throughput?
# * Run with Uvicorn's `--workers` flag (processes) or behind Gunicorn using
#   `uvicorn.workers.UvicornWorker`.
# * Profile first – `asyncio` fixes I/O wait, not CPU‑bound work.  Heavy number
#   crunching belongs in Celery/RQ workers or `asyncio.to_thread`.

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True
    )
