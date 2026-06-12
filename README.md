# Calculator API — GitHub Actions CI/CD Demo

A tiny **Flask** web service that does arithmetic, built to teach you how
**GitHub Actions** runs a full **CI/CD** pipeline:

- **CI** (`.github/workflows/ci.yml`) — lints and tests the code on every push/PR.
- **CD** (`.github/workflows/cd.yml`) — builds a Docker image and "deploys" it,
  but only *after* CI passes on `main`.

```
├── app/                  # The application
│   ├── calculator.py     #   pure logic (easy to unit-test)
│   └── main.py           #   Flask web API
├── tests/                # pytest test suite
│   ├── test_calculator.py
│   └── test_api.py
├── .github/workflows/    # ← GitHub Actions lives here
│   ├── ci.yml            #   Continuous Integration
│   └── cd.yml            #   Continuous Deployment
├── Dockerfile            # How to package the app for deployment
├── requirements.txt      # App dependencies
└── requirements-dev.txt  # Test + lint tools
```

---

## Key concepts (read this first)

GitHub Actions is automation that runs **in GitHub's cloud** whenever an event
happens in your repo (a push, a pull request, etc.). The pieces:

| Term | Meaning |
|------|---------|
| **Workflow** | A `.yml` file in `.github/workflows/`. One pipeline. |
| **Event / trigger** (`on:`) | What starts it — e.g. `push`, `pull_request`. |
| **Job** | A group of steps that runs on a fresh virtual machine (a *runner*). |
| **Runner** | The machine the job runs on, e.g. `ubuntu-latest`. |
| **Step** | A single command or a reusable **action** (`uses:`). |
| **Action** | A prebuilt step you reuse, e.g. `actions/checkout@v4`. |
| **Secret** | An encrypted value (API key, password) stored in repo settings. |

**CI = Continuous Integration:** automatically test every change.
**CD = Continuous Deployment:** automatically ship changes that pass.

---

## Part 1 — Run it locally first (optional but recommended)

```powershell
# from the project folder
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements-dev.txt

# run the tests (this is exactly what CI does)
pytest

# run the web app
python -m app.main
# open http://localhost:5000/  and  http://localhost:5000/calc?op=add&a=2&b=3
```

---

## Part 2 — Create the GitHub repository & push (your steps)

### A. Create the repo on GitHub
1. Go to <https://github.com/new>.
2. **Repository name:** `github-actions-demo` (anything is fine).
3. Leave it **empty** — do *not* add a README/.gitignore (we already have them).
4. Click **Create repository**. Copy the URL it shows, e.g.
   `https://github.com/<your-username>/github-actions-demo.git`.

### B. Turn this folder into a repo and push it
Run these in this project folder (replace the URL with yours):

```powershell
git init
git add .
git commit -m "Initial commit: calculator API with CI/CD"
git branch -M main
git remote add origin https://github.com/<your-username>/github-actions-demo.git
git push -u origin main
```

> The first push may ask you to sign in to GitHub — use the browser popup, or a
> Personal Access Token as the password.

### C. Watch the Action run automatically 🎉
- Because `ci.yml` triggers `on: push` to `main`, **the moment you push, CI starts.**
- On GitHub, open your repo → **Actions** tab.
- You'll see the **CI** workflow running. Click it → click the **Lint & Test**
  job to watch each step live. Green check = passed.
- When CI finishes successfully, the **CD** workflow starts on its own
  (it's wired to run *after* CI via `workflow_run`), builds the Docker image,
  smoke-tests it, and runs the simulated deploy.

That's the whole loop: **push → CI tests → CD deploys.**

---

## Part 3 — Make a change and watch CI/CD react

This is the part that makes it "click". Let's add a feature and push it.

### Option 1: a passing change
1. Add a `power` operation in [app/calculator.py](app/calculator.py):
   ```python
   def power(a: float, b: float) -> float:
       return a ** b
   ```
   and add `"power": power,` to the `OPERATIONS` dict.
2. Add a test in [tests/test_calculator.py](tests/test_calculator.py):
   ```python
   def test_power():
       assert calculate("power", 2, 3) == 8
   ```
3. Push it:
   ```powershell
   git add .
   git commit -m "Add power operation"
   git push
   ```
4. Go to the **Actions** tab → CI runs your new test → goes green → CD deploys.

### Option 2: deliberately break it (see CI catch a bug)
1. Change a test to expect a wrong value, e.g. `assert add(2, 3) == 6`.
2. `git commit -am "break a test"` then `git push`.
3. In the **Actions** tab the CI run turns **red ❌**, the failing step shows
   the exact assertion error, and **CD does NOT run** — broken code is blocked.
4. Fix it, commit, push again → green, and CD proceeds.

> **Pro tip — Pull Requests:** Instead of pushing straight to `main`, create a
> branch (`git checkout -b my-feature`), push it, and open a Pull Request on
> GitHub. CI runs *on the PR* and shows a ✓/✗ right on the page — this is how
> teams review code before it merges. Add **branch protection** (Settings →
> Branches) to *require* CI to pass before merging.

---

## Part 4 — Making the deployment real (next step when you're ready)

The CD workflow currently ends in a **simulated** deploy step so it works with
zero setup. To deploy for real, replace that step with one of these:

**Push the image to GitHub's container registry (easiest, free):**
```yaml
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}   # provided automatically

      - name: Push image
        run: |
          docker tag calculator-api:${{ github.sha }} ghcr.io/<your-username>/calculator-api:latest
          docker push ghcr.io/<your-username>/calculator-api:latest
```

**Deploy to a host** (Render, Fly.io, Azure, AWS, etc.): each provides an
official Action. You store credentials as **Secrets** in your repo
(**Settings → Secrets and variables → Actions → New repository secret**) and
reference them as `${{ secrets.MY_SECRET }}` — never hard-code them.

---

## Cheat sheet — the everyday loop

```powershell
# 1. make code changes
# 2. test locally
pytest
# 3. commit and push
git add .
git commit -m "describe your change"
git push
# 4. open the Actions tab on GitHub and watch CI -> CD run
```
