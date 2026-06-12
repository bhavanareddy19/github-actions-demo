# The Complete GitHub Actions Learning Guide

A click-by-click tour of **everything** in GitHub Actions: the screens, the
graphs, the visualizations, monitoring, and the experiments to run so you don't
miss anything. Work through it top to bottom.

> Prerequisite: you've pushed this project to GitHub (see README Part 2). All
> the visuals below light up only *after* at least one workflow has run.

---

## 0. The map — where everything lives

In your repository on GitHub, these are the tabs/areas that matter for Actions:

| Where | What you see there |
|-------|--------------------|
| **Actions** tab | The list of all workflow runs + the visual run graph |
| A single **run** page | Job graph, logs, timing, artifacts, summary |
| **Insights** tab → **Actions** | Usage graphs: minutes consumed, run trends |
| **Settings** → **Actions** | Permissions, runners, secrets behavior |
| **Settings** → **Secrets and variables** | Store API keys/passwords |
| **Settings** → **Branches** | Branch protection (require CI to pass) |
| **Pull Request** page | Inline ✓/✗ checks from your workflows |
| Repo home (README) | Status **badge** (green/red shield) |

---

## 1. The Actions tab — the run list

Click the **Actions** tab. This is mission control.

**Left sidebar:** a list of all your workflows (here: **CI** and **CD**).
Click one to filter runs to just that workflow.

**Main area:** every run, newest first. Each row shows:
- 🟢/🔴/🟡 status (success / failure / in-progress),
- the commit message that triggered it,
- the branch, the trigger event (push, pull_request…),
- duration, and how long ago.

**Things to play with here:**
- Use the **filter bar**: `Event:`, `Status:`, `Branch:`, `Actor:` dropdowns.
  Try `Status: failure` to see only broken runs.
- Click any run to open it (next section).
- Top-right of a workflow: **"··· → View runs"** and the `...` menu lets you
  **disable** a workflow or set up notifications.

---

## 2. A single run — THE GRAPH you asked about 📊

Click any run. The top of the page shows the **workflow run graph** — boxes
connected by lines showing every job and how they depend on each other.

For our project you will see:
- In a **CI** run: parallel boxes `Lint & Test (3.11)` and `Lint & Test (3.12)`
  (that's the *matrix* — same job, two Python versions, side by side).
- In a **CD** run: the `Build image & deploy` box.

**Reading the graph:**
- Each box is a **job**. Green check = passed, red X = failed, spinner = running.
- Lines between boxes = **dependencies** (`needs:`). A job waits for the one
  feeding into it. This is the visual "pipeline".
- Click any box to open that job's **step-by-step logs**.

**The job log view (click a box):**
- Every **step** is an expandable row (Checkout, Set up Python, Install,
  Lint, Run tests…).
- Click a step to expand its live console output. This is where you read a
  test failure or a stack trace.
- Each step shows its **duration** on the right — that's your per-step timing.
- 🔍 Use the **search box** inside logs to find a word.
- ⚙️ The gear/`...` menu lets you **download raw logs** or
  **view raw logs** in plain text.

**Top-right of the run page — important buttons:**
- **Re-run jobs** → "Re-run all jobs" or "Re-run failed jobs only" (great for
  flaky failures; re-runs without a new commit).
- **Re-run with debug logging** → adds verbose diagnostics.
- **Cancel run** (while in progress).

---

## 3. Run timing & the "Usage" / duration view

On a finished run page:
- The left panel lists **jobs** with each job's **duration**.
- Click **"Usage"** (or the **billable time** line) to see how many
  **minutes** the run consumed per job — this is your cost/performance monitor.
- Compare matrix legs: you can literally see `3.11` vs `3.12` timing differ.

This is how you "monitor steps": graph → job → step durations → total minutes.

---

## 4. Job Summaries — custom visual reports

Open a finished run; below the graph there's a **Summary** section. GitHub
renders any markdown a job writes to `$GITHUB_STEP_SUMMARY` here — tables,
test results, charts. (Our demo doesn't write one yet — see Experiment 6 to
add one and watch it appear.)

---

## 5. Insights → Actions — the BIG graphs over time 📈

Click the repo's **Insights** tab, then **Actions** in the left sidebar
(also reachable via **Settings → Actions** usage on some plans).

Here you get **aggregate visualizations across many runs**:
- **Workflow runs over time** (line/bar chart of run volume),
- **Number of runs** and **success vs failure** trends,
- **Average run time** and **minutes used** per workflow,
- Filter by **time period** (last 7/30 days) and by **workflow**.

This is the dashboard for "how healthy is my pipeline" — failure spikes, slow
trends, how many minutes you're burning.

> Note: the richest charts appear after you have several runs and depend on
> your plan (free tier shows core graphs; some advanced charts are org-level).

---

## 6. Status badge — the green/red shield

Put a live status image in your README:
```markdown
![CI](https://github.com/<your-username>/github-actions-demo/actions/workflows/ci.yml/badge.svg)
```
It turns green when CI passes, red when it fails. (Actions tab → a workflow →
`...` → **Create status badge** generates this for you.)

---

## 7. Pull Requests — checks inline

Workflows shine on PRs:
1. `git checkout -b feature-x`, make a change, `git push -u origin feature-x`.
2. On GitHub click **Compare & pull request**.
3. At the bottom of the PR you'll see a **Checks** box: each workflow shows
   🟡 running → 🟢/🔴. Click **Details** to jump into the run graph.
4. This is the team workflow: review code while CI verifies it automatically.

---

## 8. Branch protection — make CI *mandatory*

**Settings → Branches → Add branch ruleset / protection rule** for `main`:
- Enable **"Require status checks to pass before merging"**, then pick your
  CI checks (`Lint & Test`).
- Now a red CI **blocks the merge button**. This is how CI actually enforces
  quality, not just reports it.

---

## 9. Secrets & variables — for real deployments

**Settings → Secrets and variables → Actions**:
- **Secrets** (encrypted, masked in logs) → API keys, passwords, tokens.
- **Variables** (plain config) → non-secret settings.
- Reference in YAML as `${{ secrets.NAME }}` / `${{ vars.NAME }}`.
- Watch: if a secret value appears in a log, GitHub auto-masks it as `***`.

---

## 10. Manual triggers & inputs (`workflow_dispatch`)

Add this to a workflow's `on:` block to get a **"Run workflow" button** in the
Actions tab (run on demand, no push needed):
```yaml
on:
  workflow_dispatch:
    inputs:
      message:
        description: "Say something"
        default: "hello"
```
Then **Actions → that workflow → Run workflow** dropdown appears. Try it.

---

## 11. Artifacts — files a run produces

Jobs can upload files (test reports, coverage HTML, built binaries) for you to
download from the run page. Add to a job:
```yaml
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
```
After it runs, the **run page** shows an **Artifacts** section with a download
link. (Pair with `pytest --cov-report=html`.)

---

## 12. Caching — speed monitoring

We already cache pip (`cache: pip` in `setup-python`). On a run, expand the
**Set up Python** step: the first run says *cache not found*, later runs say
*cache restored* and run faster. Watching this teaches you performance tuning.

---

## 13. The Marketplace — reusable actions

Visit <https://github.com/marketplace?type=actions>. Every `uses:` line in our
YAML (`actions/checkout`, `actions/setup-python`, `docker/login-action`) comes
from here. Browse it to see the building blocks you can drop into `steps:`.

---

# ✅ Hands-on checklist — do these in order to learn everything

Tick each one off. Each teaches a different part of the system.

- [ ] **1. Push the repo** and open the **Actions** tab; watch CI run live.
- [ ] **2. Open a CI run** and look at the **run graph** — see the two matrix
      boxes (3.11 / 3.12) run in parallel.
- [ ] **3. Click into a job → expand each step**; read the test output;
      note each step's **duration**.
- [ ] **4. Watch CD trigger by itself** after CI succeeds; open its run.
- [ ] **5. Break a test on purpose** (e.g. `assert add(2,3)==6`), push, and
      watch CI go **red ❌** and CD get **skipped**. Open the failed step and
      read the assertion error. Then fix it and push again.
- [ ] **6. Re-run a job** using "Re-run failed jobs" without a new commit.
- [ ] **7. Add a Job Summary** step and watch it render:
      `echo "### Tests passed ✅" >> $GITHUB_STEP_SUMMARY`
- [ ] **8. Add `workflow_dispatch`** and use the **Run workflow** button.
- [ ] **9. Upload an artifact** (coverage HTML) and download it from the run.
- [ ] **10. Open Insights → Actions** and look at the over-time graphs
      (run count, success rate, minutes used, average duration).
- [ ] **11. Add the status badge** to your README; see it go green.
- [ ] **12. Make a branch + Pull Request**; watch the inline ✓ checks.
- [ ] **13. Turn on branch protection** requiring CI; try to merge a red PR
      and see the merge button blocked.
- [ ] **14. Add a secret**, echo a masked value, confirm it shows as `***`.
- [ ] **15. Browse the Marketplace** and identify where each `uses:` comes from.

Finish all 15 and you will have touched every major surface of GitHub Actions:
triggers, jobs, steps, the run graph, matrices, dependencies, logs, timing,
summaries, artifacts, caching, secrets, manual runs, PR checks, branch
protection, the badge, and the Insights graphs.
```
