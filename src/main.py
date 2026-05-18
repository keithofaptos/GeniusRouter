import os
import json
import yaml
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import litellm
from semantic_router import SemanticRouter, Route
from semantic_router.encoders import HuggingFaceEncoder
import redis.asyncio as redis
import ollama
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GeniusRouter — 3-Tier IQ Hybrid Router (2026)")

# Load user config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Redis cache
r = redis.from_url(os.getenv("REDIS_URL"))

# Semantic first-pass
routes = [
    Route(name="low", utterances=["simple", "translate", "summarize", "hello", "basic", "quick"]),
    Route(name="medium", utterances=["explain", "code", "how", "compare", "list"]),
    Route(name="high", utterances=["design", "architecture", "reason", "analyze", "strategy", "multi-step"])
]
encoder = HuggingFaceEncoder(model_name="sentence-transformers/all-MiniLM-L6-v2")
semantic_router = SemanticRouter(encoder=encoder, routes=routes)

# Tiny classifier
async def classify_iq(prompt: str) -> str:
    if not config["classifier"]["enabled"]:
        return "medium"
    try:
        resp = ollama.chat(model=config["classifier"]["model"],
                           messages=[{"role": "user", "content": f"Classify exactly: LOW | MEDIUM | HIGH\nPrompt: {prompt[:500]}"}])
        tier = resp['message']['content'].strip().lower()
        return tier if tier in ["low", "medium", "high"] else "medium"
    except:
        return "medium"

# Get model for tier (handles rigs + OpenRouter)
def get_model_for_tier(tier: str) -> str:
    base = config["routing"][f"{tier}_iq"]
    rig_url = config["local_rigs"].get(f"{tier}_url", "")
    if rig_url:
        litellm.register_model({"model": base, "api_base": rig_url})
        return base
    return base

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    prompt = " ".join([m.get("content", "") for m in body.get("messages", []) if isinstance(m.get("content"), str)])

    semantic_tier = semantic_router(prompt).name or "medium"
    iq_tier = await classify_iq(prompt)
    model = get_model_for_tier(iq_tier)

    cache_key = f"cache:{hash(prompt + model)}"
    if config["cache"]["enabled"]:
        cached = await r.get(cache_key)
        if cached:
            return JSONResponse(content=json.loads(cached))

    response = await litellm.acompletion(
        model=model,
        messages=body["messages"],
        **{k: v for k, v in body.items() if k not in ["model", "messages"]}
    )

    result = response.model_dump()
    if config["cache"]["enabled"]:
        await r.setex(cache_key, config["cache"]["ttl_seconds"], json.dumps(result))

    return JSONResponse(content=result)

@app.get("/health")
async def health():
    return {"status": "healthy", "router": "GeniusRouter 3-Tier IQ (2026)", "config": config["routing"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
