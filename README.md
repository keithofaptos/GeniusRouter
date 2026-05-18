GeniusRouter  ---SOTA 3-Tier IQ LLM Router (May 2026)

Easiest way to route prompts by intelligence: Low / Medium / High IQ tiers.

Features
- Edit only `config.yaml` to choose any models
- Supports 3 separate GPU rigs + OpenRouter + any API
- Tiny Granite4 classifier + semantic first-pass
- Full OpenAI-compatible proxy
- Docker one-click deploy

Quickstart
1. Edit config.yaml (pick your low/medium/high models)
2. Add API keys to .env
3. docker compose up -d

--

# GeniusRouter — SOTA 3-Tier IQ LLM Router (May 2026)

**The easiest way to route prompts by intelligence required** — Low / Medium / High IQ tiers.

Built by intelligently combining the best-of-class components from multiple state-of-the-art open-source repositories.

## Quick Start (2 minutes)

1. Clone the repository:
   ```bash
   git clone https://github.com/keithofaptos/GeniusRouter.git
   cd GeniusRouter

2:Start the router with Docker (one command):

docker compose up -d --build

3:Test it

curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "geniusrouter/auto",
    "messages": [{"role": "user", "content": "What is 2 + 2?"}]
  }'

4:Check health and current configuration:

curl http://localhost:8000/health

The router is now running as a full OpenAI-compatible proxy at http://localhost:8000.

Features
•  Simple config.yaml — choose any models for Low / Medium / High IQ
•  Full support for up to 3 separate local GPU rigs + OpenRouter + any API provider
•  Tiny Granite4 350M classifier + semantic first-pass routing (<10ms decisions)
•  Redis semantic cache for maximum tokenomics and speed
•  70–92% cost savings while preserving quality
•  Docker one-click deployment

--
 
## Contributing

Contributions are warmly welcomed and greatly appreciated!

If you are interested in assisting or contributing to GeniusRouter, please feel free to open an Issue on GitHub.  

We are particularly seeking help with a clean deployment script for Vast.ai. This will enable us to easily provision GPU instances for accelerated testing, integration, and debugging of the router.

GeniusRouter was architected by integrating the strongest state-of-the-art (SOTA) components from multiple best-in-class open-source repositories. Our immediate focus is comprehensive testing to identify and resolve any bugs or edge cases.

**Roadmap**  
Once GeniusRouter is fully stable and production-ready, the next major initiative will be the **GeniusRALPH** goal-oriented agent framework in its own dedicated repository.  

When both GeniusRouter and GeniusRALPH are mature and reliable, the long-term vision is to combine them into a true JARVIS-level intelligent cognative assistant system.

We look forward to collaborating with the Open Source MIT licensed community!

    • wanna take a ride? •
