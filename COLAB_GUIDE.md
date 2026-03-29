# Running ReportGenerator on Google Colab

Google Colab gives you a **free T4 GPU** with ~15 GB VRAM — plenty for Phi-2 (5.56 GB).
The steps below take about **5 minutes** start to finish.

---

## Step 1 — Upload Your Project to Google Drive

1. Zip your project folder:
   - Right-click `ReportGenerator/` → **Send to → Compressed (zipped) folder**
2. Go to [drive.google.com](https://drive.google.com) and upload the `.zip`
3. In Drive, right-click the zip → **Extract Here** (using a Drive app) — **OR** just let Colab unzip it (see Step 3)

---

## Step 2 — Open a New Colab Notebook

Go to [colab.research.google.com](https://colab.research.google.com) → **New notebook**

**Enable GPU first:**
`Runtime → Change runtime type → T4 GPU → Save`

---

## Step 3 — Paste These Cells into Colab

Copy each code block below into a separate Colab cell and run them in order.

---

### Cell 1 — Mount Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

---

### Cell 2 — Unzip & Set Working Directory

```python
import zipfile, os

# Adjust this path to wherever you uploaded the zip in Drive
ZIP_PATH = '/content/drive/MyDrive/ReportGenerator.zip'
EXTRACT_TO = '/content/ReportGenerator'

with zipfile.ZipFile(ZIP_PATH, 'r') as z:
    z.extractall(EXTRACT_TO)

os.chdir(EXTRACT_TO)
print("✅ Working directory:", os.getcwd())
print("📂 Files:", os.listdir('.'))
```

> **Tip:** If you already extracted the folder in Drive, skip the unzip and just set:
> ```python
> os.chdir('/content/drive/MyDrive/ReportGenerator')
> ```

---

### Cell 3 — Install Dependencies

```python
!pip install -q -r requirements.txt
print("✅ Dependencies installed")
```

---

### Cell 4 — Accept Hugging Face Terms (one-time)

Phi-2 requires a Hugging Face account. If you haven't already:

1. Go to [huggingface.co/microsoft/phi-2](https://huggingface.co/microsoft/phi-2) and accept the terms
2. Get your token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

```python
from huggingface_hub import login
login()   # paste your HF token when prompted
```

---

### Cell 5 — Run the Agent

```python
import sys
sys.path.insert(0, '.')   # ensure local modules are found

from agent import run_react_agent
run_react_agent()
```

Colab will prompt you: `📌 Enter research topic:` — type your topic and press **Enter**.

---

## What Happens Next

```
🤖 REACT RESEARCH AGENT — STARTING
📌 Enter research topic: Artificial Intelligence

✅ Topic: 'Artificial Intelligence'
🖥️  Running on: CUDA

⏳ Loading tokenizer...
⏳ Loading model...          ← takes ~2 min on T4 first run (cached after)

🔁 STEP 1  → search_web
🔁 STEP 2  → search_wikipedia
🔁 STEP 3  → generate_report

📋 FINAL REPORT  (printed + saved as Artificial_Intelligence.txt)
```

---

## Saving the Output Report

The `.txt` report is saved to the current directory. To copy it to Drive:

```python
import shutil
shutil.copy('Artificial_Intelligence.txt', '/content/drive/MyDrive/')
print("✅ Report saved to Drive")
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError` | Re-run Cell 3 (pip install) and restart runtime |
| `OutOfMemoryError` on CPU | Make sure T4 GPU is selected (`Runtime → Change runtime type`) |
| `Repository not found` | Log in with `huggingface_hub.login()` (Cell 4) |
| `KeyboardInterrupt` downloading model | Re-run Cell 5 — model resumes from cache |
