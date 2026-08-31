---
title: AlloyCode — Bug Log
status: living
last_verified: 2026-06-19
companion_doc: CHANGELOG.md
ai_guidance: |
  This is the LIVING incident-and-fix log. Each entry is dated, has an ID
  (DL-001 ... DL-NNN), describes the symptom, and records the exact fix
  applied. Append-only — never rewrite past entries. Companion to
  CHANGELOG.md, which records intentional changes; this file records
  incidents and the fixes that landed.

  FORMAT: entries are ordered OLDEST FIRST and numbered `## N. Area — DL-0NN
  Title`, with **Problem** / **Root cause** / **Fix** / **Thinking** sections.
  This is the shape Alloygraph's devlog importer parses
  (`src/importers/devlog.py`), so this log can be loaded as queryable project
  memory. Keep the shape when appending: next entry is `## 27.`. Sections the
  importer does not model (Date, Severity, Affected, Lesson, Notes) live under
  **Thinking** with their labels intact.
---
# Development Log — AlloyCode

> Running record of significant issues encountered during development and the exact fixes applied.
> Oldest first; append new entries at the bottom.

---

## 1. Frontend — DL-001 Frontend Hardcoded Backend URLs

**Problem**
All API calls in the frontend were hardcoded to `http://localhost:8000`:

```typescript
const res = await fetch("http://localhost:8000/api/v1/assessments");
```

This made the frontend non-deployable to any environment other than local development and tightly coupled it to the backend's exact location.

**Root cause**
Initial development convenience — URLs were hardcoded during rapid prototyping and never centralized.

**Fix**
Created a centralized API configuration module:

```typescript
// frontend/src/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8004";

export const api = {
    base: API_BASE,
    assessments: `${API_BASE}/api/v1/assessments`,
    approvals: `${API_BASE}/api/v1/approvals`,
    statistics: `${API_BASE}/api/v1/statistics`,
    documents: (id: string) => `${API_BASE}/api/v1/documents/${id}`,
    assessment: (id: string) => `${API_BASE}/api/v1/assessments/${id}`,
    approval: (id: string) => `${API_BASE}/api/v1/approvals/${id}`,
    approvalDecide: (id: string) => `${API_BASE}/api/v1/approvals/${id}/decide`,
};
```

Updated all page components to import from `@/lib/api` instead of hardcoding URLs.

**Thinking**
**Date:**

2026-03-21

**Severity:**

Medium

**Affected:**

All frontend page components

**Additional Bug Found:**

In `approvals/page.tsx`, line 14 had a string literal instead of a template literal:

```typescript
// BUG — double quotes, not backticks
const res = await fetch("${api.approvals}");

// Should be
const res = await fetch(`${api.approvals}`);
```

**Files Changed:**

- `frontend/src/lib/api.ts` — created
- `frontend/src/app/page.tsx` — updated
- `frontend/src/app/assessments/new/page.tsx` — updated
- `frontend/src/app/assessments/[id]/page.tsx` — updated
- `frontend/src/app/approvals/page.tsx` — updated (+ template literal bug)

---

## 2. Git — DL-002 `git mv` Permission Denied on Batch Rename

**Problem**
Running all three directory renames in sequence:

```bash
git mv core_1 sentinel && git mv core_2_knowledge_base knowledge_engine && git mv core_3 orchestrator
```

The first rename succeeded, but `git mv core_2_knowledge_base knowledge_engine` failed with `Permission denied`.

**Root cause**
On Windows, when `git mv` renames a directory, the filesystem may not fully release file handles before the next `git mv` starts. Running three renames chained with `&&` did not leave enough time between operations.

**Fix**
Ran each rename individually with pauses between:

```bash
git mv core_1 sentinel        # succeeded
git mv core_3 orchestrator     # succeeded
git mv core_2_knowledge_base knowledge_engine  # succeeded
```

After the renames, updated all references in:
- `docker-compose.yml` — build paths and volume mounts
- `start-all-modules.ps1` — module paths
- `stop-all-modules.ps1` — module paths
- `.env` — comments
- `04_IMPLEMENTATION_AUDIT.md` — module references

**Thinking**
**Date:**

2026-03-21

**Severity:**

Low

**Affected:**

Repository root directories

---

## 3. Vector Store — DL-003 ChromaDB Shows 0 Collections (Vector Store Misidentification)

**Problem**
Running `chromadb.PersistentClient` against the `chroma_data/` directory returned 0 collections:

```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_data")
print(client.list_collections())  # []
```

This initially suggested the vector database was empty.

**Root cause**
The project had **migrated from ChromaDB to a custom JSON-backed VectorStore** due to ChromaDB's incompatibility with Python 3.14. The `chroma_data/` directory name was kept, but the files inside are JSON documents — not ChromaDB's SQLite format.

The actual vector store is implemented in `knowledge_engine/src/stores/vector_store.py`:

```python
# Comment in source: "ChromaDB incompatible with Python 3.14"
class VectorStore:
    # Stores documents as JSON files in chroma_data/
    # Implements cosine similarity search manually
    # Uses Gemini text-embedding-004 embeddings (768 dims)
```

**Fix**
**Resolution:**

No fix needed — data was fully populated. The misleading directory name was kept for backward compatibility.

**Thinking**
**Date:**

2026-03-21

**Severity:**

Informational (false alarm)

**Affected:**

`knowledge_engine/chroma_data/`

**Verification:**

Direct inspection of the JSON files confirmed 2,198 documents with embeddings across 7 collections:
- `obligations` (1,421), `recitals` (353), `articles` (212), `definitions` (90)
- `interpretive` (56), `concepts` (47), `rights` (19)

---

## 4. PowerShell — DL-004 PowerShell Script Parse Errors

**Problem**
Running the script produced a cascade of parse errors:

```
The Try statement is missing its Catch or Finally block.
Missing closing '}' in statement block or type definition.
```

Multiple errors at lines 72, 75, 76, 100, 142, 201, 206, 218, 222.

**Root cause**
Three contributing factors:

1. **3-argument `Join-Path`** — `Join-Path $ProjectRoot $mod ".env"` only works in PowerShell 7+ (the `-AdditionalChildPath` parameter). Windows PowerShell 5.1 only accepts two positional arguments, causing the parser to misinterpret subsequent statements.

2. **Unicode box-drawing characters** — Characters like `=`, `=`, `|`, `*`, `v`, `x`, `!` in strings can cause parse issues when the file is saved as UTF-8 without BOM and read by Windows PowerShell 5.1 (which defaults to ANSI encoding without BOM).

3. **Brace placement** — `} catch {` on the same line is fine in PS 7+ but can cause issues in PS 5.1 under certain encoding conditions.

**Fix**
- Replaced `Join-Path $a $b $c` with nested calls: `$modPath = Join-Path $a $b; Join-Path $modPath $c`
- Replaced all Unicode decorative characters with ASCII equivalents (`[OK]`, `[X]`, `[!]`, `->`, `=====`)
- Placed `catch` and `else` on separate lines after closing braces

**Thinking**
**Date:**

2026-03-22

**Severity:**

High

**Affected:**

`start-all-modules.ps1`

**Files Changed:**

- `start-all-modules.ps1` — full rewrite with PS 5.1 compatible syntax
- `stop-all-modules.ps1` — matching syntax update

---

## 5. Config — DL-005 Orchestrator `.env` Missing `GEMINI_API_KEY`

**Problem**
Orchestrator crashed on startup with:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
gemini_api_key
  Field required [type=missing, ...]
```

**Root cause**
The `.env` file was generated from an old template that predated the switch from OpenAI to Gemini:

```bash
# Old (broken)
OPENAI_API_KEY=sk-your-openai-key-here

# Expected by config.py
GEMINI_API_KEY=your-gemini-api-key-here
```

The `Settings` class in `orchestrator/src/config.py` has `gemini_api_key: str = Field(...)` (required, no default), but the `.env` only had `OPENAI_API_KEY`.

**Fix**
Updated `orchestrator/.env` to use `GEMINI_API_KEY` and removed the stale `OPENAI_API_KEY` entry.

**Thinking**
**Date:**

2026-03-22

**Severity:**

Critical (blocks orchestrator startup)

**Affected:**

`orchestrator/.env`

**Files Changed:**

- `orchestrator/.env` — replaced `OPENAI_API_KEY` with `GEMINI_API_KEY`

---

## 6. SQLAlchemy — DL-006 SQLAlchemy Reserved Attribute `metadata`

**Problem**
Sentinel module crashed on import with:

```
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved
when using the Declarative API.
```

**Root cause**
The `DecisionLog` model used `metadata` as a column attribute name:

```python
class DecisionLog(Base):
    metadata = Column(JSON, nullable=True)  # RESERVED
```

In SQLAlchemy's declarative API, `Base.metadata` refers to the `MetaData` object that tracks table schemas. Using `metadata` as a column attribute name shadows this internal attribute.

**Fix**
Renamed the Python attribute while preserving the database column name using SQLAlchemy's column-name override:

```python
# Keep DB column as "metadata", use different Python attribute
decision_metadata = Column("metadata", JSON, nullable=True)
```

Updated all references:
- `main.py:271` — `metadata=request.metadata` to `decision_metadata=request.metadata`
- `gdpr.py:84` — `decision.metadata` to `decision.decision_metadata`

Note: `Base.metadata.create_all()` in `session.py` and Pydantic model fields named `metadata` were unaffected (different scope).

**Thinking**
**Date:**

2026-03-22

**Severity:**

Critical (blocks sentinel startup)

**Affected:**

`sentinel/src/database/models.py`

**Files Changed:**

- `sentinel/src/database/models.py` — renamed column attribute
- `sentinel/src/api/main.py` — updated constructor kwarg
- `sentinel/src/compliance/gdpr.py` — updated attribute access

---

## 7. Python Env — DL-007 `uv run uvicorn` — "Failed to canonicalize script path"

**Problem**
Running `uv run uvicorn src.api.main:app` from any module directory produced:

```
Failed to canonicalize script path
```

The error occurred even when running directly in the terminal, not just inside `Start-Job`.

**Root cause**
The `uv run <script>` command resolves the `uvicorn` script entry point by canonicalizing its filesystem path. When the working directory contains spaces (our path: `D:\60 Days\Projects\Portfolio_Series\Project_1_EU AI Regulatory Compliance Engine\...`), `uv` 0.9.x fails to canonicalize the script path.

This is a known `uv` behavior with paths containing spaces on Windows.

**Fix**
Use `uv run python -m uvicorn` instead of `uv run uvicorn`:

```bash
# BROKEN — fails with spaces in path
uv run uvicorn src.api.main:app --port 8000

# WORKING — bypasses script path resolution
uv run python -m uvicorn src.api.main:app --port 8000
```

`python -m uvicorn` uses Python's module system to find uvicorn, which handles spaces correctly.

**Thinking**
**Date:**

2026-03-22

**Severity:**

High

**Affected:**

All three backend modules

**Files Changed:**

- `start-all-modules.ps1` — changed all `uv run uvicorn` to `uv run python -m uvicorn`

---

## 8. PowerShell — DL-008 `Start-Job` Cannot Find `uv` or `npm`

**Problem**
All three backend jobs started but immediately entered a `Failed` or `Completed` state with no useful output. Services never came up.

**Root cause**
PowerShell `Start-Job` runs script blocks in a **separate child process** with its own environment. The `uv` executable (`C:\Users\SAB\.local\bin\uv.exe`) was in the parent session's PATH but not inherited by the child process. Same issue for `npm`.

**Fix**
Resolve the full executable path in the parent session using `Get-Command`, then pass it into the job:

```powershell
# Parent: resolve once
$script:UvPath = (Get-Command uv -ErrorAction Stop).Source

# Child job: use absolute path
$job = Start-Job -ScriptBlock {
    param($uvExe, $path, $port)
    Set-Location $path
    & $uvExe run python -m uvicorn src.api.main:app --port $port
} -ArgumentList $script:UvPath, $modulePath, $module.Port
```

**Thinking**
**Date:**

2026-03-22

**Severity:**

High

**Affected:**

`start-all-modules.ps1`

**Files Changed:**

- `start-all-modules.ps1` — resolve `$script:UvPath` and `$script:NpmPath` upfront, pass into all `Start-Job` blocks

---

## 9. Windows — DL-009 Stale Processes Block Pipeline Restart

**Problem**
Running the start script after a previous session left stale processes (e.g., a different API server) occupying port 8000. The script saw the port as occupied and either skipped the module or hung waiting for a service that never started.

```
[!] Port 8000 already in use - skipping orchestrator
```

Visiting `http://localhost:8000` returned a response from a completely different project ("Cafe Rota Management System API").

**Root cause**
Previous development sessions or other projects left processes listening on ports 8000, 8001, 8002, or 3000. The original start script had no cleanup phase — it assumed clean ports.

**Fix**
Added a `Stop-PortProcess` function and a cleanup phase at the top of `start-all-modules.ps1`:

```powershell
# Kill anything listening on our ports before starting
$targetPorts = @(8000, 8001, 8002, 3000)
foreach ($port in $targetPorts) {
    Stop-PortProcess -Port $port
}
```

The function uses `Get-NetTCPConnection` to find listening PIDs and `Stop-Process -Force` to terminate them. Also clears any stale PowerShell background jobs from previous runs.

**Thinking**
**Date:**

2026-03-22

**Severity:**

Medium

**Affected:**

`start-all-modules.ps1`

**Files Changed:**

- `start-all-modules.ps1` — added `Stop-PortProcess` function + cleanup phase before module startup

---

## 10. Windows — DL-010 Windows Zombie TCP Ports (8000 and 8003)

**Problem**
After killing a process on ports 8000 and 8003, `Get-NetTCPConnection` still shows LISTEN state with the old PID. `Get-Process -Id <pid>` returns "not found" and `taskkill /F /PID <pid>` says "not found", but the port remains occupied indefinitely. New servers cannot bind to the port.

**Root cause**
Windows TCP stack bug — when a process dies ungracefully (e.g., `Stop-Process -Force`), the kernel may hold the socket in LISTEN state with a stale PID that no longer exists. This only clears on reboot.

**Fix**
**Workaround:**

Migrated the orchestrator port from 8000 -> 8003 -> 8004. Updated all references:
- `start-all-modules.ps1` — target ports and orchestrator port
- `stop-all-modules.ps1` — cleanup ports
- `frontend/src/lib/api.ts` — default API URL
- `DEPLOYMENT_GUIDE.md` — all port references

**Thinking**
**Date:**

2026-03-22

**Severity:**

Medium

**Affected:**

`start-all-modules.ps1`, `frontend/src/lib/api.ts`, `DEPLOYMENT_GUIDE.md`

**Current Port Assignments:**

- Monitor: 8002
- Knowledge Engine: 8001
- Orchestrator: **8004** (was 8000, then 8003)
- Frontend: 3000

---

## 11. Persistence — DL-011 In-Memory Fallback Not Persisting Assessments

**Problem**
POST `/api/v1/assessments` returns 200 (assessment created), but GET `/api/v1/assessments/{session_id}` returns 404 ("Assessment not found") when PostgreSQL is unavailable.

**Root cause**
When the database is unavailable (`db is None`), the POST handler skipped `repo.create(state)` entirely:
```python
if db is not None:
    repo = AssessmentRepository(db)
    await repo.create(state)
```
This meant the assessment was never stored in the in-memory fallback (`_memory_store`). The background task's `repo.update()` also failed silently because the session_id didn't exist in memory.

**Fix**
Always create the repo and store the state, regardless of DB availability:
```python
repo = AssessmentRepository(db)
await repo.create(state)
```
When `db is None`, the repo automatically uses the in-memory store.

**Thinking**
**Date:**

2026-03-22

**Severity:**

High

**Affected:**

`orchestrator/src/api/main.py`

---

## 12. PowerShell — DL-011.5 PowerShell Deploy Scripts — Multiple Pitfalls

**Problem**
Multiple failures during GCP Cloud Run deployment:

### A. `$args` is a Reserved Automatic Variable
```
docker build showed Docker help page instead of building
```
The `Invoke-DockerBuild` function used `$args` as a local variable. PowerShell's `$args` is an automatic variable containing unbound arguments — assigning to it is silently ignored, so `docker @args` splatted nothing.

**Fix**
Renamed to `$dockerArgs`.

### B. gcloud stderr Triggers NativeCommandError
```
NativeCommandError: Listing items under project aegis-compliance-engine...
```
With `$ErrorActionPreference = "Stop"`, gcloud's informational stderr output (e.g., "Listing items under project...") triggers a terminating error in PowerShell — even with `2>$null` redirection.

Created `Invoke-GcloudQuery` helper that temporarily sets `$ErrorActionPreference = "Continue"` before running gcloud read-only commands.

### C. `$script:` Scope vs Function-Local Scope
```
setup-secrets.ps1 always tried to CREATE secrets that already existed
```
Inside `Push-Secret`, the gcloud list was captured as `$script:currentList` inside an `Invoke-Native` scriptblock. But the `if ($currentList -contains $name)` check read the function-local `$currentList` (initialized to `@()`) — always empty, always creating.

Replaced with `Invoke-GcloudQuery { gcloud secrets describe $name }` — directly checks if the specific secret exists, no scope tricks needed.

**Thinking**
**Date:**

2026-03-23

**Severity:**

High (blocks deployment)

**Affected:**

`deploy.ps1`, `deploy_gcp.ps1`, `setup-secrets.ps1`

---

## 13. Cloud Run — DL-012 CORS Blocks Frontend → Orchestrator on Cloud Run

**Problem**
Deployed frontend shows "Failed to connect to AlloyCode API" on every action. Browser console shows CORS errors — the orchestrator rejects requests from the Cloud Run frontend URL.

**Root cause**
The orchestrator's CORS config only allowed `localhost:3000` and `localhost:8080` in production mode. In development mode it allowed `*`, but Cloud Run deploys with `ENVIRONMENT=production`. The Cloud Run frontend URL (`https://aegis-frontend-xxxxx.europe-west1.run.app`) was not in the allowed list.

Since the orchestrator deploys before the frontend, the frontend URL isn't known at orchestrator deploy time — a chicken-and-egg problem.

**Fix**
1. Updated `orchestrator/src/config.py` — `get_cors_origins()` now supports `*` as a value in the origins list (not just in development mode)
2. Updated `deploy.ps1` — added `CORS_ORIGINS=*` to the orchestrator's `--set-env-vars`

For a public portfolio demo with `--allow-unauthenticated`, wildcard CORS is acceptable. For production, you'd do a two-pass deploy: deploy orchestrator → deploy frontend → get frontend URL → update orchestrator CORS → redeploy orchestrator.

**Thinking**
**Date:**

2026-03-23

**Severity:**

High (blocks all API calls from deployed frontend)

**Affected:**

`orchestrator/src/config.py`, `deploy.ps1`

---

## 14. Cloud Run — DL-013 Cloud Run Container Fails to Start — Wrong Port

**Problem**
```
ERROR: The user-provided container failed to start and listen on the port
defined provided by the PORT=8080 environment variable within the allocated timeout.
```

**Root cause**
Cloud Run defaults to `PORT=8080` and expects containers to listen there. Our containers listen on custom ports (8002, 8001, 8000, 3000) as defined in their Dockerfiles. Without `--port`, Cloud Run sends traffic to 8080 where nothing is listening.

**Fix**
Added `--port` to every Cloud Run deploy command:
- Monitor: `--port=8002`
- Knowledge Engine: `--port=8001`
- Orchestrator: `--port=8000`
- Frontend: `--port=3000`

**Thinking**
**Date:**

2026-03-23

**Severity:**

High (blocks deployment)

**Affected:**

All Cloud Run service deployments

---

## 15. Cloud Run — DL-014 Cloud Run Health Checks Return 405 Method Not Allowed

**Problem**
All three backend health checks reported `405 Method Not Allowed` even though services were running correctly.

**Root cause**
The deploy script's health check used `Invoke-WebRequest -Method Head`, but FastAPI's `/health` endpoints only define `@app.get("/health")` — they don't accept `HEAD` requests.

**Fix**
Changed health check from `-Method Head` to `-Method Get`.

**Thinking**
**Date:**

2026-03-23

**Severity:**

Low (cosmetic — services work fine)

**Affected:**

`deploy.ps1` — health check section

---

## 16. Cloud Run — DL-015 Cloud Run Rejects `PORT` as Environment Variable

**Problem**
```
ERROR: spec.template.spec.containers[0].env: The following reserved env names
were provided: PORT. These values are automatically set by the system.
```

**Root cause**
Cloud Run reserves `PORT` as a system-managed environment variable. When `--port=3000` is specified, Cloud Run automatically sets `PORT=3000` in the container. Passing `PORT=3000` in `--set-env-vars` causes a conflict.

**Fix**
Removed `PORT=3000` from `--set-env-vars` in the frontend deploy command. Cloud Run sets it automatically from `--port`.

**Thinking**
**Date:**

2026-03-23

**Severity:**

Medium (blocks frontend deployment)

**Affected:**

`deploy.ps1` — frontend deploy command

---

## 17. Cloud Run — DL-016 Cloud Run Domain Mapping Unsupported in europe-west2

**Problem**
Cloud Run Console shows "Domain mappings are not available in the region of the selected service" when trying to map a custom domain in `europe-west2` (London).

**Root cause**
Cloud Run domain mapping is only supported in specific regions. `europe-west2` is not one of them.

**Fix**
Changed deployment region from `europe-west2` to `europe-west1` in:
- `deploy.ps1` — `$REGION` variable
- `deploy_gcp.ps1` — default parameter
- `cleanup_gcp.ps1` — default parameter

After changing regions, deleted old services in `europe-west2` and redeployed to `europe-west1`.

**Thinking**
**Date:**

2026-03-23

**Severity:**

Medium

**Affected:**

All Cloud Run services

**Supported European regions for domain mapping:**

- `europe-west1` (Belgium) — closest alternative

**Note on domain mapping timing:**

After adding DNS records, domain mapping verification can take 15-30 minutes. If it exceeds 1 hour, check:
1. DNS records are correct (`gcloud beta run domain-mappings describe --domain=yourdomain.com --region=europe-west1`)
2. Domain ownership is verified in [Google Search Console](https://search.google.com/search-console)
3. No CAA records blocking Google's certificate authority (`pki.goog`)
4. Alternative: use a Global Application Load Balancer or Firebase Hosting instead of native domain mapping

---

## 18. GCP Secrets — DL-017 Gemini API Key Invalid on Cloud Run

**Problem**
Assessment workflow returns:
```
Error calling model 'gemini-2.5-flash' (INVALID_ARGUMENT): 400 INVALID_ARGUMENT.
API key not valid. Please pass a valid API key.
```

**Root cause**
The `GEMINI_API_KEY` stored in GCP Secret Manager was stale or invalid. The secret was pushed from `orchestrator/.env` via `setup-secrets.ps1`, but the key may have been rotated or expired at Google AI Studio.

**Fix**
1. Verify the key works locally: `curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY"`
2. If invalid, generate a new key at [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Update `orchestrator/.env` with the new key
4. Re-push: `.\setup-secrets.ps1`
5. Redeploy orchestrator: `.\deploy.fast.ps1` (or update just the secret version and trigger a new revision)

**Thinking**
**Date:**

2026-03-23

**Severity:**

Critical (blocks all LLM operations)

**Affected:**

`orchestrator` Cloud Run service

**Lesson:**

Always test API keys independently before deploying. Secret Manager stores versions — an old version being "latest" doesn't mean the key is still valid.

---

## 19. GCP Secrets — DL-018 Secrets Corrupted by PowerShell BOM / CRLF When Pushing to GCP Secret Manager

**Problem**
OAuth login on deployed Cloud Run returns:
```
Error 401: invalid_client — The OAuth client was not found.
```
API keys may also show "invalid" errors despite being correct locally.

**Root cause**
`setup-secrets.ps1` piped secret values to gcloud via stdin:
```powershell
$value | & $GCLOUD secrets versions add $name --data-file=-
```

This has **two problems** on Windows PowerShell 5.1:
1. **Trailing CRLF** — PowerShell's pipe appends `\r\n` to every string sent to a native command. The secret `my-client-id.apps.googleusercontent.com` is stored as `my-client-id.apps.googleusercontent.com\r\n`.
2. **UTF-8 BOM** — The alternative fix using `[System.IO.File]::WriteAllText($path, $value, [System.Text.Encoding]::UTF8)` writes a 3-byte BOM (`\xEF\xBB\xBF`) prefix on .NET Framework (PowerShell 5.1).

Cloud Run injects secret values **byte-for-byte** as environment variables — it does NOT strip BOM or trailing whitespace. So `AUTH_GOOGLE_ID` becomes `\xEF\xBB\xBFmy-client-id.apps.googleusercontent.com` or `my-client-id.apps.googleusercontent.com\r\n`, neither of which Google recognizes.

Locally, `.env` files are read directly by the framework (no BOM, no CRLF injection), so credentials work fine.

**Fix**
Use `WriteAllBytes` with explicit UTF-8 encoding (no BOM, no trailing newline):
```powershell
$tmp = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllBytes($tmp, [System.Text.Encoding]::UTF8.GetBytes($value))
& $GCLOUD secrets versions add $name --data-file=$tmp --quiet
Remove-Item $tmp
```

**Thinking**
**Date:**

2026-03-25

**Severity:**

Critical (breaks OAuth and any secret containing exact-match values)

**Affected:**

`setup-secrets.ps1`, all Cloud Run services consuming secrets

**Lesson:**

Never pipe secrets to `gcloud --data-file=-` on Windows PowerShell. Always write to a temp file using `WriteAllBytes` to guarantee clean byte output. This applies to any tool that reads exact-match values from Secret Manager (OAuth client IDs, API keys, JWTs, etc.).

---

## 20. Gemini API — DL-019 Gemini Embedding Model `text-embedding-004` Returns 404 (Silent Empty Citations)

**Problem**
The scan UI shows findings, risk classification (PROHIBITED), narrative, and remediation, but **every expanded finding row has no "Legal citations" block**. `mapped_articles` badges still render because they come from the static rule YAML, masking the real failure.

Direct probe of the knowledge engine:

```
$ curl -X POST http://localhost:8001/api/v1/hybrid/reason \
    -H "Content-Type: application/json" \
    -d '{"question":"biometric identification"}'
Internal Server Error  (HTTP 500)
```

`/health` reports everything green (`vector_store: loaded`, `neo4j: connected`), so the failure is invisible from the dashboard.

**Fix**
```python
# knowledge_engine/src/config.py
- embedding_model: str = "text-embedding-004"
+ embedding_model: str = "gemini-embedding-001"
```

(The matching default in `engine.py:35` was also updated for parity.)

**Thinking**
**Date:**

2026-04-14

**Severity:**

High (legal_research agent silently produces zero citations)

**Affected:**

`knowledge_engine/src/config.py`, `knowledge_engine/src/retrieval/engine.py`

**Root Cause (two-layer bug):**

1. **Stale embedding model name.** `knowledge_engine/src/config.py` defaulted to `embedding_model = "text-embedding-004"`. As of 2026, Google removed this model from the `v1beta` endpoint that `google-genai >= 1.6x` calls. The Gemini SDK now returns:
   ```
   google.genai.errors.ClientError: 404 NOT_FOUND.
   models/text-embedding-004 is not found for API version v1beta,
   or is not supported for embedContent.
   ```
   This 404 propagates up through `RetrievalEngine.query()` → `vector_search` / `hybrid_search` / `hybrid_reason`, which all return HTTP 500 to the orchestrator.

2. **Legal Research agent swallows the failure.** [`legal_research.py:106-108`](orchestrator/src/agents/legal_research.py#L106-L108) catches `httpx.HTTPError`, logs a warning, and returns empty citations. The supervisor still completes the workflow — so the UI looks healthy, the documentation_generator runs on whatever it has, and the user has no on-screen signal that the KB lookup never produced a single article.

**Why this is safe without a re-embed:**

the existing JSON vector store (`knowledge_engine/chroma_data/*.json`) was already generated with `gemini-embedding-001` — embeddings are 3072-dim. Verified:

```python
import json
data = json.load(open("chroma_data/articles.json"))
len(data["embeddings"][0])  # -> 3072  (gemini-embedding-001 native dim)
```

So the deployed data and the new model name match. Switching the default is purely a config fix — no re-ingestion needed.

**Activation:**

restart the knowledge_engine process so Pydantic Settings re-reads the default:

```powershell
.\stop-all-modules.ps1 -SkipInfra
.\start-all-modules.ps1 -SkipInfra
```

After restart, expanded finding rows in the scan UI render the "Legal citations" block populated with article snippets and relevance scores.

**Lessons:**

- **Pin embedding model versions in `.env`, not as code defaults.** Google's habit of deprecating models on `v1beta` will break any service whose model name lives only in source. Putting `EMBEDDING_MODEL=` in the `.env` makes rotation a 30-second fix instead of a code edit + redeploy.
- **Fail-loud on KB lookup failure when there ARE findings to research.** `legal_research.py` catches HTTP errors per-rule and continues — that's correct for partial outages, but if **every** rule lookup fails the agent should surface a workflow-level warning so the dashboard can show "citations unavailable" rather than silently rendering an empty block. (Tracked as a follow-up; not fixed in this commit.)
- **`/health` is not enough for retrieval services.** A green health check that loads the store but never exercises the embedding path will hide a deprecated-model failure indefinitely. Add a synthetic-query smoke check to `/health` (embed a fixed string, do a 1-doc cosine lookup, return the result count) so this class of bug fails the health probe.
- **Cross-check stored embedding dimension against the configured model** before changing model names. A mismatch (e.g. switching to a 768-dim model against 3072-dim stored vectors) silently produces garbage rankings — worse than a 500.

**Files Changed:**

- `knowledge_engine/src/config.py` — `embedding_model` default updated
- `knowledge_engine/src/retrieval/engine.py` — matching default updated

---

## 21. Citations — DL-020 "Validated 0/0 Citations" — Brittle Regex Misses Common LLM Citation Phrasings

**Problem**
After fixing [DL-019](#dl-019--gemini-embedding-model-text-embedding-004-returns-404-silent-empty-citations), the `legal_research` agent's `reasoning_chain` shows the pipeline executing end-to-end:

```
step 1 retrieve   -> 10 entities (AIACT_ART_5, GDPR_ART_35, ...)
step 2 classify   -> intent: prohibition
step 3 build_context -> 10 entities
step 4 synthesize -> Gemini answer generated
step 5 validate   -> Validated 0/0 citations    <-- bug
step 6 score      -> Confidence: MEDIUM
```

Retrieval is finding the right articles, the LLM is writing a grounded answer, but **zero citations make it to the UI**. The "Legal citations" block in the scan UI stays empty even though the system has perfect grounding.

**Root cause**
`_extract_citations` (in `reasoning_engine.py`) uses regex to harvest article references **from the LLM's free-text answer**. The original four patterns only matched the regulation-suffix form:

```python
r"Article\s+(\d+)\s+(?:of\s+(?:the\s+)?)?GDPR"
r"Article\s+(\d+)\s+(?:of\s+(?:the\s+)?)?(?:EU\s+)?AI\s+Act"
r"Art(?:icle)?\.?\s*(\d+)\s+GDPR"
r"Art(?:icle)?\.?\s*(\d+)\s+AI\s+Act"
```

But Gemini routinely emits the regulation-**prefix** form ("AI Act Art 5(1)(c)", "GDPR Article 35") and inlines subsections like `5(1)(c)` between the article number and the regulation token. Neither was matched. So `_extract_citations` returned `[]`, the validator dutifully reported "0/0", and the agent's response shipped with no citations attached — even though `raw_results` already contained `AIACT_ART_5` from retrieval step 1.

This was a **silent quality regression**: the LLM-citation extractor was the single point of truth for what reached the UI, and its failure mode is invisible (the workflow completes, narrative renders, only the citation block goes empty).

**Fix**
Two complementary changes in `_extract_citations`:

1. **Broadened regex set.** Four patterns covering both orderings (regulation-prefix and regulation-suffix), with `Art./Article/Art` prefix tolerance and an optional subsection cluster `(?:\s*\([^)]*\))*` that swallows things like `5(1)(c)`:

   ```python
   _CITATION_PATTERNS = [
       r"(?:EU\s+)?AI\s+Act[\s,]+Art(?:icle)?\.?\s*(\d+)",
       r"GDPR[\s,]+Art(?:icle)?\.?\s*(\d+)",
       r"Art(?:icle)?\.?\s*(\d+)(?:\s*\([^)]*\))*\s+(?:of\s+(?:the\s+)?)?(?:EU\s+)?AI\s+Act",
       r"Art(?:icle)?\.?\s*(\d+)(?:\s*\([^)]*\))*\s+(?:of\s+(?:the\s+)?)?GDPR",
   ]
   ```

2. **Retrieval-based fallback.** When the regex still finds nothing, promote the top retrieved Article entities (entities whose `metadata.type == "Article"` or whose `entity_id` starts with `AIACT_ART_` / `GDPR_ART_`) — capped at 5. These were already validated against the graph by the retrieval step, so surfacing them is a strict quality improvement, not a hallucination risk:

   ```python
   if not citations:
       for r in results:
           # promote top retrieved Article entities
           ...
           if len(citations) >= 5:
               break
   ```

**Thinking**
**Date:**

2026-04-14

**Severity:**

Medium (legal_research returns empty citation list despite high-quality retrieval)

**Affected:**

`knowledge_engine/src/retrieval/reasoning_engine.py`

**Verification (offline, against the new logic):**

| Input answer text | Extracted citations |
|---|---|
| `AI Act Art 5 lists prohibited practices including social scoring (5(1)(c)).` | `['AIACT_ART_5']` |
| `See Article 5(1)(c) of the AI Act for prohibited practices.` | `['AIACT_ART_5']` |
| `Art. 35 GDPR requires a DPIA. Also Article 9 GDPR for special categories.` | `['GDPR_ART_35', 'GDPR_ART_9']` |
| `GDPR Art 9 covers special-category data; AI Act Article 27 covers FRIA.` | `['AIACT_ART_27', 'GDPR_ART_9']` |
| `No citations here, just plain text.` (with retrieval hits) | fallback -> `['AIACT_ART_5', 'GDPR_ART_35']` |

All five forms previously returned `[]`.

**Activation:**

restart the knowledge_engine so the new method is loaded:

```powershell
.\stop-all-modules.ps1 -SkipInfra
.\start-all-modules.ps1 -SkipInfra
```

After restart, the "Legal citations" block populates for every finding where retrieval returned at least one Article entity.

**Lessons:**

- **Don't make LLM phrasing the single source of truth for structured outputs.** If the retrieval step has already validated entities against a knowledge graph, surface those entities directly — treat the LLM's free-text citations as augmentation, not the authoritative list.
- **"0/0 validated" is a code smell, not a confidence signal.** It silently hides a broken extractor as a "the LLM didn't cite anything" non-event. A degraded-but-still-rendering response is much harder to debug than a hard failure.
- **Test extractors against the model's actual output style, not your assumed style.** Gemini's free-form citation phrasing varies by intent (prohibition prompts get prefix-form; obligation prompts often get suffix-form). Sample real outputs before writing the regex, not after.

**Files Changed:**

- `knowledge_engine/src/retrieval/reasoning_engine.py` — broadened `_CITATION_PATTERNS`, added retrieval fallback in `_extract_citations`

---

## 22. Vector Store — DL-021 Vector store consolidation: Weaviate + JSON → Neo4j native vector index

**Problem**
Two recurring failure modes converged on the same conclusion: two vector backends meant two failure surfaces.

**(1) Aura pause + stale driver.** A `retrieve: FAILED — ReadError:` symptom appeared in scan reports — superficially similar to [DL-019](#dl-019--gemini-embedding-model-text-embedding-004-returns-404-silent-empty-citations), but the embedding model was already correct. Investigation showed Aura free-tier had auto-paused after 3 days of inactivity. The knowledge_engine's cached Neo4j driver became stale. `/health` reported `degraded` but didn't 503 cleanly; individual `/api/v1/hybrid/search` calls returned 500 Internal Server Error mid-response, which httpx async surfaces as `ReadError:` with empty message because the connection was dropped before a complete response body arrived.

**(2) Weaviate not deployed.** `gcp.ps1` deploy was wired for Neo4j only. The deployed knowledge_engine read `WEAVIATE_HOST` from settings, defaulted to `localhost` (which doesn't exist on Cloud Run), and returned 0 vector hits even when otherwise healthy. Production scans would surface findings with empty citation blocks.

**Root cause**
The vector backend had migrated twice before this session: ChromaDB → JSON-backed `VectorStore` → Weaviate sidecar. Each migration solved one specific problem (Python compat, persistence, scale-out) but added fan-out — by the time Weaviate landed, knowledge_engine state spanned two databases, two Docker volumes, two Cloud Run secret families, two health probes, and two separate "is this thing alive?" debugging surfaces. Every operational incident had to be triaged across both backends.

Neo4j 5.13+ ships a native HNSW vector index over node properties. Aura runs 5.27 with `db.index.vector.queryNodes` available. So consolidating to one backend isn't a downgrade — it's an option that didn't exist when ChromaDB was originally chosen.

**Fix**
- **Single vector index** `entity_embedding` on `:Entity(embedding)`, dim=3072 (gemini-embedding-001), cosine similarity.
- **All 2,198 embeddings** loaded into Neo4j as `:Entity.embedding` properties via `09_load_vectors_to_neo4j.py` (UNWIND batch update, 250 nodes per transaction). Source was the existing `chroma_data/*.json` corpus — embeddings preserved without re-running Gemini.
- **Logical "collections"** (articles, recitals, obligations, etc.) preserved as `:Entity.collection` property; queries filter via `WHERE node.collection IN $collections` after `CALL db.index.vector.queryNodes(...)`. One index, seven logical groupings.
- **`RetrievalEngine`** rewritten to delegate vector search to `graph_store.vector_search(...)`; RRF fusion logic unchanged. Documents come back with `:Entity.document_text` baked in, so retrieval results are self-contained.
- **Weaviate Docker container, volume, and `weaviate-client` Python dep** all removed.
- **Aura keep-alive** added: `.github/workflows/keep-aura-alive.yml` runs every 2 days at 12:00 UTC, executes `MATCH (n) RETURN count(n)` against Aura via the Neo4j Python driver, and fails the workflow with an alert if node count drops below 1000 (catches accidental graph wipes). Required repo secrets: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`.

**Thinking**
**Date:**

2026-04-29

**Severity:**

High (architectural change, ops fragility driver)

**Affected:**

- `knowledge_engine/src/stores/graph_store.py` (added `vector_search`, `create_vector_index`, `vector_index_exists`, `vector_collection_counts`, plus `VECTOR_*` class constants)
- `knowledge_engine/src/retrieval/engine.py` (drops `vector_store`, delegates to `graph_store.vector_search`)
- `knowledge_engine/src/api/main.py` (removes `vector_store` global; simplifies `/health` and `/api/v1/vector/search`)
- `knowledge_engine/src/config.py` (removes `weaviate_*` settings)
- `knowledge_engine/pyproject.toml` (removes `weaviate-client` dep)
- `docker-compose.yml` (removes `weaviate` service + volume + dependent env vars)
- New: `knowledge_engine/scripts/09_load_vectors_to_neo4j.py`
- Deleted: `weaviate_store.py`, `vector_store.py` (JSON), `chroma_data/` directory, scripts `05a_fix_concept_rights_vectors.py` and `08_migrate_json_to_weaviate.py`
- New: `.github/workflows/keep-aura-alive.yml`

**Verification:**

End-to-end scan against `https://github.com/sahabajalam/euai_testing` completed in 27 seconds (16:14:14 → 16:14:41). 8 findings, every reasoning chain showed `1. retrieve: hybrid RRF search — N raw hits` (no `FAILED`, no `ReadError`, no `503`). Direct `/api/v1/hybrid/search` query for biometric identification returned the same Article 5 obligations as the previous Weaviate-era smoke test, with similarity 0.89 (Neo4j returns native cosine; Weaviate was returning `1 - distance` so the previous score was 0.78 — same ranking, different scale).

**Lesson:**

Operational fragility compounds across backends. When the same architecture spans two stateful systems (graph DB + vector DB), every incident has to be triaged twice and every deploy has to wire up two independent secret families. Consolidating into one backend is worth a meaningful migration cost if the destination supports the workload — and Neo4j's native vector index does, comfortably, for this corpus size (2,198 embeddings, 3072-dim, ~27 MB on Aura's 200 MB free tier). When evaluating future "should we add a specialized store?" questions, the cost isn't the new system in isolation; it's the second failure surface for everything you already have.

---

## 23. Cloud Run — DL-022 Cloud Run orchestrator deploy: port hardcoded + missing git binary

**Problem**
Two consecutive deploys to `aegis-orchestrator` failed with the same Cloud Run error:

```
ERROR: (gcloud.run.deploy) The user-provided container failed to start
and listen on the port defined provided by the PORT=8004 environment
variable within the allocated timeout.
```

Misleading message — suggests port misconfiguration. The actual cause was upstream of port binding in both cases.

**Root cause**
Two distinct bugs surfaced in sequence.

**(1) Hardcoded port in Dockerfile.**
`orchestrator/Dockerfile` shipped with `EXPOSE 8000` and `CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]`. The deploy script passes `--port=8004` to `gcloud run deploy`, which Cloud Run translates into `PORT=8004` injected into the container at runtime. The hardcoded uvicorn arg ignored `$PORT` entirely and bound to 8000. Cloud Run probed 8004, got nothing, declared the deploy failed.

**(2) Missing git binary.**
After fixing port to use `${PORT:-8004}`, deploy still failed with the same error. Pulling Cloud Run logs (`gcloud logging read`) on the failed revision revealed:

```
The git executable must be specified in one of the following ways:
    - be included in your $PATH
    - be set via $GIT_PYTHON_GIT_EXECUTABLE
    - explicitly set via git.refresh(<full-path-to-git-executable>)
All git commands will error until this is rectified.
Traceback (most recent call last):
  File "/app/.venv/bin/uvicorn", line 10, in <module>
    sys.exit(main())
```

The orchestrator imports `code_analyzer/`, which uses GitPython to `git clone --depth=1` repos for scanning. GitPython runs an import-time check that calls `exit(1)` if `git` is missing from PATH. The base image `python:3.11-slim` doesn't include git. Container exited with code 1 before uvicorn ever bound to a port. Cloud Run reported the symptom (port not listening) instead of the cause (process exit during import).

**Fix**
`orchestrator/Dockerfile` final stage:

```dockerfile
# Install git — required at runtime for code_analyzer.ingest, which
# uses GitPython to `git clone --depth=1` scanned repos. GitPython
# also runs an import-time check that exit(1)s if git is missing.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Expose port (matches PORT default below; Cloud Run overrides via env)
EXPOSE 8004

# Run the application — bind to $PORT if Cloud Run injected one,
# otherwise fall back to the local convention (8004). `exec` keeps
# uvicorn as PID 1 so SIGTERM is delivered cleanly on shutdown.
CMD ["sh", "-c", "exec uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8004}"]
```

The `sh -c "exec ..."` pattern is critical: shell form gets `$PORT` expansion, `exec` replaces the shell with uvicorn so uvicorn becomes PID 1 and receives SIGTERM directly during Cloud Run shutdown (otherwise sh ignores the signal and you get a 10-second termination delay).

`knowledge_engine/Dockerfile`: same `${PORT:-8001}` pattern applied preventively. The KE was working coincidentally because deploy `--port=8001` matched the hardcoded value, but a single change in either place would have broken it.

`HEALTHCHECK` directives removed from both Dockerfiles — Cloud Run uses its own startup probes; nothing in `docker-compose.yml` depended on the Dockerfile healthcheck.

**Thinking**
**Date:**

2026-04-29

**Severity:**

High (deploy blocked; misleading error message)

**Affected:**

- `orchestrator/Dockerfile` (port + git install)
- `knowledge_engine/Dockerfile` (preventive `$PORT` fix)
- Cloud Run service `aegis-orchestrator`

**Lesson:**

Cloud Run's "container failed to start and listen on PORT" error covers two distinct failure modes:

1. The process is alive but binding to the wrong port.
2. The process exited (any reason) before binding any port.

Both produce the same Cloud Run error. **Always pull `gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.revision_name="..."'` for the failed revision before assuming it's a port issue.** The application logs show the real failure — in this case, the GitPython import-time crash. Diagnosing from the deploy error alone wastes a build cycle.

Same lesson applies to any system-level dep: if the application imports a Python library that wraps a CLI tool (GitPython, pygit2, etc.), the CLI must be in the runtime image. Slim base images don't ship development tools.

---

## 24. PowerShell — DL-023 gcp.ps1 secret verification false-negative: PowerShell scope mismatch

**Problem**
Immediately after `./gcp.ps1 -Action secrets` reported all 6 secrets stored, `./gcp.ps1 -Action deploy-fast` reported every secret as MISSING:

```
[+] Verifying required secrets in Secret Manager
    [ERR] GEMINI_API_KEY -- MISSING
    [ERR] GOOGLE_API_KEY -- MISSING
    [ERR] DATABASE_URL_ORCHESTRATOR -- MISSING
    [ERR] NEO4J_URI -- MISSING
    [ERR] NEO4J_USER -- MISSING
    [ERR] NEO4J_PASSWORD -- MISSING
```

The secrets were genuinely present in Secret Manager — verifiable via `gcloud secrets list`. The deploy script just couldn't see them.

**Root cause**
PowerShell scope mismatch in the verification block:

```powershell
$existingSecrets = @()                                                # function-local
Invoke-Native "gcloud secrets list" {
    $script:existingSecrets = (& $gcloud secrets list ... 2>$null) -split "`n" |
        ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }      # writes script scope
}
foreach ($s in $requiredSecrets) {
    if ($existingSecrets -contains $s) { Write-OK $s }                # reads function-local (still empty!)
    else { Write-Fail "$s -- MISSING" }
}
```

When `Invoke-Native` calls `& $Command`, the scriptblock runs in a child scope. `$existingSecrets = ...` would be local to that child; `$script:existingSecrets = ...` writes to the script scope. But the outer `foreach` reads function-local `$existingSecrets` — never populated. The two "$existingSecrets" are different variables.

This sat as a latent bug because the deploy script had only been tested end-to-end on a fresh project where `setup` and `deploy` ran back-to-back without a working secret-list verification path. Re-running `deploy-fast` against an existing project surfaced the mismatch.

**Fix**
Use `Invoke-GcloudQuery` (already defined elsewhere in `gcp.ps1`) which returns the captured output through the function boundary cleanly:

```powershell
$rawList = Invoke-GcloudQuery { & $gcloud secrets list --format="value(name)" }
$existingSecrets = @()
if ($rawList) {
    $existingSecrets = ($rawList -split "`r?`n") |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ -ne "" }
}
foreach ($s in $requiredSecrets) {
    if ($existingSecrets -contains $s) { Write-OK $s }
    else { Write-Fail "$s -- MISSING"; $missing += $s }
}
```

**Thinking**
**Date:**

2026-04-29

**Severity:**

Low (workflow blocker, not a runtime bug)

**Affected:**

`gcp.ps1` `Invoke-Deploy` function

**Lesson:**

PowerShell scriptblock invocation via `& $Command` creates a new scope. If a result needs to escape, return it via the pipeline (which `Invoke-GcloudQuery` already does) rather than mutating an outer-scope variable from inside the scriptblock. Mixing `$script:` writes with function-local reads silently desyncs.

---

## 25. Cloud Run — DL-024 Live orchestrator reports `database: unavailable` (degraded health)

**Problem**
`/health` returns:

```json
{
  "status": "degraded",
  "components": {
    "supervisor": "ready",
    "control_plane": "ready",
    "database": "unavailable"
  }
}
```

Frontend (200 OK) and knowledge engine (`status: healthy`, Neo4j connected, vector index online with 2,198 docs) are unaffected. The orchestrator's supervisor + control plane initialised cleanly; the Postgres connection did not.

**Root cause**
Not yet diagnosed. Likely candidates (in order of probability):
1. Cloud SQL instance paused/stopped (free-tier idling) — verify with `gcloud sql instances describe`.
2. Secret rotation: the `DATABASE_URL_ORCHESTRATOR` secret in Secret Manager has drifted from the live Cloud SQL instance creds.
3. VPC/connector / Cloud SQL Auth Proxy misconfiguration after the last redeploy.
4. SQLAlchemy async pool exhaustion on a long-idle instance (less likely with `/health` returning at all).

**Fix**
Not applied yet. The investigation step is:

```bash
# Confirm Cloud SQL is running
gcloud sql instances list --project gdpreuai

# Pull live secret value and compare against expected shape
gcloud secrets versions access latest --secret=DATABASE_URL_ORCHESTRATOR --project gdpreuai

# Inspect orchestrator logs for the actual connection error
gcloud run services logs read aegis-orchestrator --region europe-west1 --limit 50 --project gdpreuai
```

Logged on [`NORTHSTAR.md`](NORTHSTAR.md) Part III as a follow-up; not blocking the live-URL win.

**Thinking**
**Date:**

2026-06-16

**Severity:**

Medium (degrades end-to-end scan flow but doesn't block the live demo)

**Affected:**

`aegis-orchestrator` Cloud Run service (URL: https://aegis-orchestrator-whfa7vg4ea-ew.a.run.app/)

**Discovery context:**

Surfaced 2026-06-16 while verifying the deploy state during the [`07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md)-driven portfolio cleanup pass. The audit had assumed the deploy was "pending" — it isn't, but this DB issue means the live demo can't persist a scan end-to-end yet.

**Notes:**

- A scan-flow end-to-end test via `POST /api/v1/scans` will fail at scan persistence — the supervisor will run, classify, retrieve, but the scan record won't survive. The KE / frontend halves of the demo (browse the KG, hit the health endpoints) are unaffected.
- This issue is *interview-relevant* — the honest answer to "show me a live demo" is "the frontend + KE are healthy; the orchestrator's Postgres connection degraded and the fix is investigation-pending." Pre-rehearsed in [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md) Q10 ("what's the worst part of this project").

---

## 26. Neo4j Aura — DL-025 Aura free-tier 30-day inactivity deletion — recovered via in-flight JSONL dump

**Problem**
User reported the original Aura instance had been auto-deleted by Neo4j after 30 days of inactivity, and they had created a new (empty) instance `e8097dda` on the same account. Strangely, the project's `knowledge_engine/.env` still pointed at the old `652f6242` URI, and connections to that URI **still succeeded** — returning a fully-populated 2,301-node / 4,423-rel graph with the 2,198-document vector index online.

**Root cause**
Aura free-tier deletion is two-stage: when the 30-day inactivity timer fires, the instance is removed from the user's account (freeing the 1-instance-per-account quota — which is why the user could create `e8097dda`), but the underlying database cluster goes through a **grace period** before hard-purge. During that window, bolt connections to the old URI continue to succeed because the certificate + auth are still loaded and the data is still resident on disk. The user sees an empty new instance in the console while the old (now-orphan) instance silently serves queries until purge.

Not documented in Aura's user-facing docs. Observed empirically.

**Fix**
**Recovery:**

1. **Backup the phantom.** Wrote [`knowledge_engine/scripts/10_backup_to_jsonl.py`](../knowledge_engine/scripts/10_backup_to_jsonl.py) — a streaming dump that writes each node + relationship as JSONL plus a separate `_indexes.json` for the vector + property indexes. Ran against the phantom URI: **2,301 nodes (97 MB nodes.jsonl), 4,423 rels (0.7 MB), 1 vector index, 23 total indexes, 1 constraint** — full bit-for-bit dump in ~30 seconds.
2. **Sync `.env` files.** User had updated root `.env` only; `knowledge_engine/.env` (the one `src/config/settings.py` actually reads) still pointed at the phantom. Synced via a PowerShell regex-substitution script.
3. **Restore.** Wrote [`knowledge_engine/scripts/11_restore_from_jsonl.py`](../knowledge_engine/scripts/11_restore_from_jsonl.py) — recreates the `:Entity(id)` unique constraint, CREATEs each node with its full label set, then MATCHes endpoints by `id` property (element IDs are not portable across instances) and CREATEs each relationship, then recreates the `entity_embedding` vector index (3072-dim cosine over `:Entity.embedding`). ~4 minutes against `e8097dda`. Verification: **2,301 / 2,301 nodes, 4,423 / 4,423 rels, 2,198 embeddings, 0 rels skipped.**
4. **Behavior verification.** Reran [`07_run_golden_tests.py --dry-run`](../knowledge_engine/scripts/07_run_golden_tests.py): citation recall@15 = **75%** (was 87.5% pre-restore — see [`METRICS.md`](METRICS.md) §5 for the HNSW non-determinism analysis; identical data, different graph build).

**Fix and prevention:**

- **`knowledge_engine/scripts/10_backup_to_jsonl.py`** is now in repo. Run before any planned maintenance, after any significant KB change, and on a schedule once the keep-alive cron is investigated. Backup dir (`knowledge_engine/backups/`) added to `.gitignore` — never commit ~100 MB JSONL dumps.
- **`knowledge_engine/scripts/11_restore_from_jsonl.py`** is now in repo. Idempotent against an empty target; uses property-based identity mapping so element IDs don't matter.
- **Open follow-up:** `keep-aura-alive.yml` workflow exists at `.github/workflows/` but did not prevent the deletion. Two possible reasons: (a) the workflow stopped running because GitHub disables scheduled workflows after 60 days of zero repo activity — but our last commit was 2026-05-20, only 30 days ago, so this shouldn't have fired; (b) Aura free-tier deletion is policy-based (30-day idle), not activity-based, and a `MATCH (n) RETURN count(n)` ping isn't counted as activity. Diagnose with `gh run list -w keep-aura-alive.yml --limit 10`. If (b), accept that free-tier needs a periodic backup-and-rebuild cycle, not a keep-alive ping.
- **Downstream:** Cloud Run services on GCP still hold the old `NEO4J_URI` secret pointing at `652f6242`. Will silently break when the phantom hard-purges. Push the new creds via `./gcp.ps1 -Action secrets` + `gcloud run services update` on both `aegis-knowledge-engine` and `aegis-orchestrator`. **Not done in this session.**

**Thinking**
**Date:**

2026-06-19

**Severity:**

Critical (data-loss event, recovered)

**Affected:**

Neo4j Aura instance `652f6242` (the production KG); replaced by `e8097dda`.

**Notes:**

- The build-A → build-B recall drop (87.5% → 75%) is a **clean HNSW non-determinism datapoint** that validates the audit's "n=6 is too small" note in [`METRICS.md`](METRICS.md) §4. Headline updated to 75% with the historical range published — honest is better than the higher number.
- The phantom-instance pattern is exploitable as a recovery tool: if you discover a paused/deleting Aura, dump it immediately before hard-purge. Window unknown — Neo4j doesn't publish it.

---
