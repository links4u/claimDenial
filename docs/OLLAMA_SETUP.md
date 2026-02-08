# ClaimPilot™ - Ollama Setup Guide

## Why Ollama?

Ollama enables running LLMs locally on your machine with:
- **Zero API costs** ($0 per appeal vs $0.01-0.02 with cloud)
- **Data privacy** (no external API calls)
- **Offline capability** (run without internet)
- **Enterprise control** (models stay on-premises)

## Installation

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

###Windows
```powershell
# Download installer from https://ollama.ai/download
# Run installer, then:
ollama serve
```

## Pull Llama 3.1 Model

```bash
# Download Llama 3.1 8B (4.7GB)
ollama pull llama3.1:8b

# Verify installation
ollama list
```

## Start Ollama Service

```bash
# Start server (runs on port 11434)
ollama serve
```

Leave this running in a terminal window.

## Test Installation

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.1:8b",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'
```

Expected response: JSON with generated text.

## Configure ClaimPilot™

In `.env`:
```bash
LLM_PROVIDER=local
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

That's it! ClaimPilot™ will now use local Llama 3.1.

## Performance Expectations

### CPU (M1/M2 Mac or equivalent)
- Classification: ~3-5s
- Drafting: ~8-12s
- Guardrail: ~3-5s
- **Total**: ~15-20s per appeal

### GPU (NVIDIA with 8GB+ VRAM)
- Classification: ~1-2s
- Drafting: ~3-5s
- Guardrail: ~1-2s
- **Total**: ~5-10s per appeal

## Quality Comparison

| Task | Llama 3.1 Quality | Claude Quality |
|------|-------------------|----------------|
| Classification | ✅ Excellent | ✅ Excellent |
| Policy Retrieval | N/A (vector search) | N/A (vector search) |
| Appeal Drafting | ✅ Good | ✅ Excellent |
| Compliance Check | ✅ Good | ✅ Excellent |

**Verdict**: Llama 3.1 is suitable for prototypes and pilots. Use Claude for production quality.

## Troubleshooting

### "Connection refused" error
```bash
# Ensure Ollama is running
ollama serve

# Check status
curl http://localhost:11434
```

### "Model not found" error
```bash
# Re-pull model
ollama pull llama3.1:8b

# List installed models
ollama list
```

### Slow performance
- Use smaller model: `ollama pull llama3.1:8b` (not 70b!)
- Close other applications  
- Use GPU if available (auto-detected by Ollama)

## Switching to Cloud LLM

Edit `.env`:
```bash
# Switch to Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Or OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

No code changes needed - agents automatically use new provider.

## Resources

- Ollama Docs: https://ollama.ai/docs
- Llama 3.1 Model Card: https://ollama.ai/library/llama3.1
- ClaimPilot™ LLM Abstraction: `backend/app/core/llm_factory.py`
