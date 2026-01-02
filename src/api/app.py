"""FastAPI service scaffold for LifeGrid.

Exposes minimal endpoints for session management, stepping, and streaming.
This is an initial stub that wraps the core Simulator for HTTP and WebSocket
clients.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Dict, Optional
import uuid

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.simulator import Simulator
from core.config import SimulatorConfig


app = FastAPI(title="LifeGrid API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class SessionState:
    simulator: Simulator
    session_id: str
    last_grid: Optional[np.ndarray] = None
    metadata: Dict[str, str] = field(default_factory=dict)


class CreateSessionRequest(BaseModel):
    width: int = Field(64, ge=4, le=2048)
    height: int = Field(64, ge=4, le=2048)
    mode: str = "Conway's Game of Life"
    birth_rule: Optional[str] = None
    survival_rule: Optional[str] = None
    pattern: Optional[str] = None


class StepRequest(BaseModel):
    steps: int = Field(1, ge=1, le=1000)


class PatternRequest(BaseModel):
    rle: Optional[str] = None
    pattern_name: Optional[str] = None


_sessions: Dict[str, SessionState] = {}


def _parse_rule(rule: Optional[str]) -> Optional[set[int]]:
    """Convert a rule string like "23" into a set of ints {2, 3}."""
    if rule is None:
        return None
    digits = [int(ch) for ch in rule if ch.isdigit()]
    return set(digits)


def _get_session(session_id: str) -> SessionState:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/session")
def create_session(req: CreateSessionRequest) -> Dict[str, str]:
    session_id = str(uuid.uuid4())
    config = SimulatorConfig(
        width=req.width,
        height=req.height,
        automaton_mode=req.mode,
        birth_rule=_parse_rule(req.birth_rule),
        survival_rule=_parse_rule(req.survival_rule),
    )
    sim = Simulator(config)
    sim.initialize(mode=req.mode, pattern=req.pattern)
    _sessions[session_id] = SessionState(simulator=sim, session_id=session_id)
    return {"session_id": session_id}


@app.post("/session/{session_id}/step")
def step_session(session_id: str, req: StepRequest) -> Dict[str, int]:
    session = _get_session(session_id)
    session.simulator.step(req.steps)
    session.last_grid = session.simulator.get_grid()
    return {"generation": int(session.simulator.generation)}


@app.get("/session/{session_id}/state")
def get_state(session_id: str) -> Dict[str, object]:
    session = _get_session(session_id)
    grid = session.simulator.get_grid()
    session.last_grid = grid
    return {
        "generation": int(session.simulator.generation),
        "width": int(grid.shape[1]),
        "height": int(grid.shape[0]),
        "grid": grid.astype(int).tolist(),
    }


@app.post("/session/{session_id}/pattern")
def load_pattern(session_id: str, req: PatternRequest) -> Dict[str, str]:
    session = _get_session(session_id)
    if req.rle:
        # TODO: integrate proper RLE parsing; for now, clear grid
        grid = session.simulator.get_grid()
        grid[:] = 0
        session.simulator.automaton.grid = grid
    if req.pattern_name and hasattr(
            session.simulator.automaton,
            "load_pattern"):
        session.simulator.automaton.load_pattern(req.pattern_name)
    session.last_grid = session.simulator.get_grid()
    return {"status": "ok"}


@app.websocket("/session/{session_id}/stream")
async def stream_state(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    session = _get_session(session_id)
    try:
        while True:
            session.simulator.step()
            grid = session.simulator.get_grid()
            payload = {
                "generation": int(session.simulator.generation),
                "width": int(grid.shape[1]),
                "height": int(grid.shape[0]),
                "grid": grid.astype(int).tolist(),
            }
            await websocket.send_json(payload)
            await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        return
