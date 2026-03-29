# OpenRouter Branch — Setup Guide

This branch replaces the local Phi-2 model (5.56 GB download, GPU required)
with the **OpenRouter API** — runs anywhere, even on a basic laptop.

---

## 1 — Get a Free OpenRouter API Key

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Go to **Keys** → **Create Key**
3. Copy the key (starts with `sk-or-v1-...`)

> Free-tier models (marked `:free`) have no cost but may have rate limits.

---

## 2 — Set Your API Key

```bash
# In the project root, copy the template:
cp .env.example .env

# Edit .env and paste your key:
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

The key is read automatically at runtime via `python-dotenv`. It is in `.gitignore` so it will never be committed.

---

## 3 — Install Dependencies

Much lighter than the Colab branch — no PyTorch or Transformers needed:

```bash
pip install -r requirements.txt
```

---

## 4 — Run

```bash
python main.py
```

You'll be prompted for a topic, then the agent runs in ~seconds (API call vs. local inference).

---

## Changing the Model

Edit `config.py`:

```python
OPENROUTER_MODEL = "meta-llama/llama-3-8b-instruct:free"   # default (free)
```

Any OpenRouter model slug works. Popular options:

| Model | Slug | Cost |
|---|---|---|
| Llama 3 8B | `meta-llama/llama-3-8b-instruct:free` | Free |
| Mistral 7B | `mistralai/mistral-7b-instruct:free` | Free |
| GPT-4o Mini | `openai/gpt-4o-mini` | ~$0.15/1M tokens |
| Claude Haiku | `anthropic/claude-3-haiku` | ~$0.25/1M tokens |

Full list: [openrouter.ai/models](https://openrouter.ai/models)

---

## Output

Reports are saved to:
```
outputs/{Topic_Name}/{Topic_Name}.txt
```
