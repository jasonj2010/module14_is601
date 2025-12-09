# 📘 IS601 Module 14 – Project Setup & Development Guide

This repo contains your personal copy of the Module 14 project, including your feature branch work (e.g., exponent calculation for the final project).  
You control this repo — nothing pushes to your professor’s repository.

---

# 📦 1. Install Homebrew (Mac Only)

Skip if you’re on Windows.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

---

# 🧰 2. Install & Configure Git

### Install Git
**Mac**
```bash
brew install git
```

**Windows**  
Download the Git installer: https://git-scm.com/download/win

Verify:
```bash
git --version
```

### Set Git Globals
```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

---

# 🔑 3. Generate SSH Keys (Recommended)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Copy your key:

- **macOS:** `pbcopy < ~/.ssh/id_ed25519.pub`
- **Windows (Git Bash):** `cat ~/.ssh/id_ed25519.pub | clip`

Add it here: https://github.com/settings/keys

Test:
```bash
ssh -T git@github.com
```

---

# 📥 4. Clone Your Personal Repository

This ensures **nothing** goes to your professor’s repo.

```bash
git clone git@github.com:yourusername/repo
cd repo
```

---

# 🐍 5. Python Setup

Install Python 3.10+  
(Create/activate venv):

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

# 🐳 6. Docker Setup (Used in Module 14)

Make sure Docker Desktop is installed.

Start the stack:
```bash
docker compose up -d
```

Stop:
```bash
docker compose down
```

Rebuild (if needed):
```bash
docker compose up -d --build
```

---

# 🧪 7. Running Tests (Unit + Integration)

Activate venv and run:
```bash
python -m pytest tests/unit -vv
python -m pytest tests/integration -vv
```

Test coverage:
```bash
pytest --cov=app
```

---

# 🚀 8. Running the App

```bash
docker compose up -d
```

App runs at:
```
http://localhost:8000
```

API docs:
```
http://localhost:8000/docs
```

---

# 🧾 Useful Commands Cheat Sheet

| Action | Command |
|-------|---------|
| Activate venv | `source venv/bin/activate` / `venv\Scripts\activate` |
| Install deps | `pip install -r requirements.txt` |
| Run tests | `pytest -vv` |
| Start Docker | `docker compose up -d` |
| Stop Docker | `docker compose down` |
| Create branch | `git checkout -b newbranch` |
| Push branch | `git push -u origin newbranch` |

 
