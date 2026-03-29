# 🤖 Autonomous Research Agent
### ReAct-Based AI Report Generator

> **Assignment 2 — Agentic AI**  
> **Name:** Krish Goyal &nbsp;|&nbsp; **System ID:** 2023359271

---

## Overview

This project implements a **ReAct (Reasoning + Acting) autonomous agent** that researches any topic, synthesises information from multiple sources, and generates a structured, formatted research report — all without human intervention after the initial topic prompt.

The agent follows a deterministic reasoning loop:

```
User Input → Thought → Action (Tool) → Observation → Repeat → Final Report
```

Each step is transparent: the agent prints its thought process, chosen action, and observed result before proceeding to the next step.

---

## 🏗️ Project Architecture

```
ReportGenerator/
├── main.py                  # Entry point — python main.py
├── config.py                # All constants (model, width, sections, persona)
├── model.py                 # Lazy model loader (Phi-2 or OpenRouter)
├── agent.py                 # ReAct loop: agent_decide() + run_react_agent()
├── utils.py                 # Shared helpers: text formatting, save_report()
│
├── tools/                   # Pluggable search tools
│   ├── __init__.py          # TOOLS registry dict
│   ├── web_search.py        # DuckDuckGo search → search_web()
│   └── wiki_search.py       # Wikipedia search → search_wikipedia()
│
└── report/                  # Report generation pipeline
    ├── __init__.py
    ├── prompts.py           # build_prompt(), clean_response()
    ├── sections.py          # generate_section(), generate_fallback()
    ├── formatter.py         # format_cover_page(), format_section()
    └── generator.py        # generate_detailed_report() — main orchestrator
```

---

## ⚙️ Agent Workflow (ReAct Loop)

```
┌─────────────────────────────────────────────────────┐
│  STEP 1  💭 Thought: No web data yet                │
│          ⚡ Action : search_web                      │
│          👁  Observe: Retrieved web snippets          │
├─────────────────────────────────────────────────────┤
│  STEP 2  💭 Thought: Need encyclopedic context      │
│          ⚡ Action : search_wikipedia                │
│          👁  Observe: Retrieved Wikipedia summary    │
├─────────────────────────────────────────────────────┤
│  STEP 3  💭 Thought: Have all context. Write report │
│          ⚡ Action : generate_report                 │
│          👁  Observe: 5-section report generated     │
└─────────────────────────────────────────────────────┘
```

The decision function (`agent_decide`) is **rule-based** — no LLM is consumed for the reasoning step itself, only for content generation.

---

## 🌿 Two Branches — Two Deployment Modes

| Feature | `main` branch | `openrouter` branch |
|---|---|---|
| **Model** | Microsoft Phi-2 (local) | Any model via OpenRouter API |
| **GPU Required** | Yes (T4 recommended) | No |
| **Download Size** | ~5.56 GB | None |
| **Best Run On** | Google Colab (free T4) | Locally or any machine |
| **API Key** | None (HuggingFace token) | OpenRouter key (free tier available) |
| **Speed** | ~2 min/report (T4) | ~10–30 sec/report |
| **Default Model** | `microsoft/phi-2` | `meta-llama/llama-3.1-8b-instruct:free` |
| **Setup Guide** | `COLAB_GUIDE.md` | `OPENROUTER_GUIDE.md` |

---

## 🚀 Quick Start

### Option A — OpenRouter Branch (Recommended for Local Use)

```bash
# 1. Switch to the openrouter branch
git checkout openrouter

# 2. Install lightweight dependencies (no PyTorch needed)
pip install -r requirements.txt

# 3. Set your API key (get one free at openrouter.ai/keys)
echo OPENROUTER_API_KEY=sk-or-v1-your-key-here > .env

# 4. Run
python main.py
```

### Option B — Main Branch on Google Colab (Free GPU)

1. Upload this folder to Google Drive (zip it first)
2. Open [colab.research.google.com](https://colab.research.google.com) → `Runtime → Change runtime type → T4 GPU`
3. Follow the step-by-step guide in **`COLAB_GUIDE.md`**

---

## 🛠️ Tools Used

| Tool | Purpose |
|---|---|
| **DuckDuckGo (`ddgs`)** | Real-time web search for current facts and news |
| **Wikipedia** | Encyclopedic background context |
| **LangChain** | LLM orchestration, prompt management |
| **Microsoft Phi-2** *(main)* | Local 2.7B parameter language model for report generation |
| **OpenRouter API** *(openrouter)* | Hosted model gateway — access Llama, Mistral, GPT-4o, Claude, etc. |

---

## 📊 Report Structure

Every generated report follows this fixed 5-section structure:

```
═══════════════════════════════════════════════════════
             RESEARCH REPORT
───────────────────────────────────────────────────────
              {TOPIC IN CAPS}
═══════════════════════════════════════════════════════
 TABLE OF CONTENTS
  1. Introduction
  2. Key Findings
  3. Challenges
  4. Future Scope
  5. Conclusion
═══════════════════════════════════════════════════════

  1. INTRODUCTION     — 3-sentence factual definition + context
  2. KEY FINDINGS     — 5 evidence-based bullet points with stats
  3. CHALLENGES       — 4 bullets: TECHNICAL / ETHICAL / ECONOMIC / SOCIAL
  4. FUTURE SCOPE     — 3-sentence near-term + long-term outlook
  5. CONCLUSION       — 3-sentence synthesis + key challenge + closing

═══════════════════════════════════════════════════════
                    END OF REPORT
═══════════════════════════════════════════════════════
```

Reports are saved to:
```
outputs/{Topic_Name}/{Topic_Name}.txt
```

---

## 📁 Sample Outputs

Three sample reports are included in the `outputs/` directory (generated on `main` branch with Phi-2):

| Topic | File |
|---|---|
| Upcoming advances in AI | [`outputs/Upcoming_advances_in_AI/`](outputs/Upcoming_advances_in_AI/Upcoming_advances_in_AI.txt) |
| Advantages of using AI in research | [`outputs/Advantages_of_using_AI_in_research/`](outputs/Advantages_of_using_AI_in_research/Advantages_of_using_AI_in_research.txt) |
| Jobs created by AI | [`outputs/Jobs_created_by_AI/`](outputs/Jobs_created_by_AI/Jobs_created_by_AI.txt) |

---

## 🔧 Switching Models (OpenRouter Branch)

Edit `config.py` to change the model. Any OpenRouter model slug works:

```python
# config.py
OPENROUTER_MODEL = "meta-llama/llama-3.1-8b-instruct:free"   # default (free)
```

Popular alternatives:

| Model | Slug | Cost |
|---|---|---|
| Llama 3.1 8B | `meta-llama/llama-3.1-8b-instruct:free` | Free |
| Mistral 7B | `mistralai/mistral-7b-instruct:free` | Free |
| GPT-4o Mini | `openai/gpt-4o-mini` | ~$0.15/1M tokens |
| Claude Haiku 3 | `anthropic/claude-3-haiku` | ~$0.25/1M tokens |
| Llama 3.1 70B | `meta-llama/llama-3.1-70b-instruct` | ~$0.35/1M tokens |

Browse all models at [openrouter.ai/models](https://openrouter.ai/models)

---

## 📦 Dependencies

### Main Branch (`requirements.txt`)
```
langchain, langchain-community, langchain-huggingface
transformers, accelerate, torch
huggingface_hub, ddgs, wikipedia
```

### OpenRouter Branch (`requirements.txt`)
```
langchain, langchain-community, langchain-openai
openai, python-dotenv, ddgs, wikipedia
```

---

## 📝 Assignment Details

| Field | Value |
|---|---|
| **Course** | Agentic AI |
| **Assignment** | 2 — Autonomous Research Agent |
| **Student** | Krish Goyal |
| **System ID** | 2023359271 |
| **Agent Type** | ReAct (Rule-Based Decision + LLM Generation) |
| **Primary Model** | Microsoft Phi-2 (`main`) / OpenRouter (`openrouter`) |
| **Tools** | DuckDuckGo Web Search + Wikipedia |
| **Framework** | LangChain + HuggingFace Transformers |

---

## 📄 License

This project is submitted as academic coursework. All generated report content intended for educational purposes only.
