#!/usr/bin/env bash
# ArticleTrace — build and deploy to Cloud Run.
#
# Replaces gcp.ps1 for macOS/Linux (there is no pwsh on the current machine,
# which is part of why the deployed images sat at 2026-04-29 for four months).
# Builds happen in Cloud Build, not locally: Cloud Run needs linux/amd64 and
# the dev machine is Apple silicon, so a local `docker build` would produce an
# image that will not start.
#
#   ./deploy.sh              # build + deploy all three services
#   ./deploy.sh orchestrator # just one (orchestrator|knowledge-engine|frontend)
#   ./deploy.sh --verify     # skip building; just report live health
#
# Secrets are NOT managed here. They live in Secret Manager and are wired to
# the services already; see "Rotating a secret" at the bottom of this file.

set -euo pipefail

PROJECT=gdpreuai
REGION=europe-west1
REG="${REGION}-docker.pkg.dev/${PROJECT}/aegis-images"
TAG="deploy-$(date +%Y%m%d-%H%M%S)"

# Service names are the original "aegis-*" ones. Renaming them would mint new
# URLs and break every inbound link for no architectural gain — deliberately
# deferred, see NORTHSTAR Part IV.
ORCH_URL=https://aegis-orchestrator-whfa7vg4ea-ew.a.run.app
KE_URL=https://aegis-knowledge-engine-whfa7vg4ea-ew.a.run.app
FE_URL=https://aegis-frontend-whfa7vg4ea-ew.a.run.app

verify() {
  echo
  echo "Live health:"
  printf '  %-24s ' knowledge-engine; curl -fsS --max-time 30 "$KE_URL/health"   || echo unreachable; echo
  printf '  %-24s ' orchestrator;     curl -fsS --max-time 30 "$ORCH_URL/health" || echo unreachable; echo
  printf '  %-24s ' frontend;         curl -fsS -o /dev/null -w 'HTTP %{http_code}\n' --max-time 30 "$FE_URL/"
  echo
  echo "A 'degraded' backend is usually a secret pointing at a resource that no"
  echo "longer exists — check the service logs before assuming it is the code."
}

if [[ "${1:-}" == "--verify" ]]; then verify; exit 0; fi

TARGET="${1:-all}"

build_and_deploy() {
  local name="$1" dir="$2"; shift 2
  echo "==> $name: building $TAG"
  case "$name" in
    frontend)
      # NEXT_PUBLIC_API_URL is compiled into the bundle at build time, so the
      # orchestrator URL must be correct here — it cannot be fixed by an env
      # var on the running service.
      ( cd "$dir" && gcloud builds submit --config cloudbuild.yaml \
          --substitutions="_NEXT_PUBLIC_API_URL=${ORCH_URL},_IMAGE_TAG=${REG}/frontend:${TAG}" \
          --project "$PROJECT" --region "$REGION" >/dev/null )
      ;;
    *)
      ( cd "$dir" && gcloud builds submit --tag "${REG}/${name}:${TAG}" \
          --project "$PROJECT" --region "$REGION" >/dev/null )
      ;;
  esac
  echo "==> $name: deploying"
  gcloud run deploy "aegis-${name}" --image "${REG}/${name}:${TAG}" \
    --region "$REGION" --project "$PROJECT" --quiet "$@" >/dev/null
  echo "==> $name: done"
}

# --no-cpu-throttling is load-bearing on the orchestrator, not a tuning knob.
# Scans run in a FastAPI BackgroundTask after the 202 response is sent, and
# Cloud Run's default throttles CPU to near-zero once a response completes — a
# scan would sit at "running" forever with no error anywhere. min-instances
# stays 0 so an idle deployment costs nothing; the frontend's 3s poll during a
# scan is what keeps the instance warm while the task runs.
case "$TARGET" in
  all)
    build_and_deploy knowledge-engine knowledge_engine
    build_and_deploy orchestrator     orchestrator     --no-cpu-throttling --min-instances=0
    build_and_deploy frontend         frontend
    ;;
  knowledge-engine) build_and_deploy knowledge-engine knowledge_engine ;;
  orchestrator)     build_and_deploy orchestrator orchestrator --no-cpu-throttling --min-instances=0 ;;
  frontend)         build_and_deploy frontend frontend ;;
  *) echo "unknown target: $TARGET (want: all|orchestrator|knowledge-engine|frontend)" >&2; exit 2 ;;
esac

verify

# ── Rotating a secret ────────────────────────────────────────────────────────
# Services read version "latest", so adding a version and redeploying is enough.
# Pipe the value in; never pass it as an argument, where it lands in shell
# history and the process table:
#
#   printf '%s' 'VALUE' | gcloud secrets versions add NEO4J_PASSWORD \
#       --project gdpreuai --data-file=-
#
# Then re-run this script for the affected service so it picks the version up.
# Secrets in use: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD (knowledge-engine +
# orchestrator), GOOGLE_API_KEY (knowledge-engine), GEMINI_API_KEY and
# DATABASE_URL_ORCHESTRATOR (orchestrator).
