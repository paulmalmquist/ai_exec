#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
API_BASE=${API_BASE:-http://localhost:8000}
ORCH_URL="$API_BASE/orchestrator"

PERSONA_PAYLOAD='{"name":"Avery","style_guidelines":"Confident, analytical, willing to argue","argumentation_level":"high","risk_posture":"medium"}'
VOICE_PAYLOAD='{"name":"AveryVoice","description":"Sample executive timbre"}'
SCRIPT_PAYLOAD='{"persona_id":"local-persona","text":"<p>The economic outlook remains resilient...</p>","tone":"confident"}'

printf "Creating persona...\n"
PERSONA=$(curl -sS -X POST "$ORCH_URL/persona" -H 'Content-Type: application/json' -d "$PERSONA_PAYLOAD")
echo "$PERSONA"
PERSONA_ID=$(echo "$PERSONA" | jq -r '.id')

echo "Registering voice..."
VOICE=$(curl -sS -X POST "$ORCH_URL/voice" -H 'Content-Type: application/json' -d "$VOICE_PAYLOAD")
echo "$VOICE"
VOICE_ID=$(echo "$VOICE" | jq -r '.id')

echo "Saving script..."
SCRIPT=$(curl -sS -X POST "$ORCH_URL/script" -H 'Content-Type: application/json' -d "{\"persona_id\":\"$PERSONA_ID\",\"text\":\"Executive outlook remains positive.\",\"tone\":\"confident\"}")
echo "$SCRIPT"
SCRIPT_ID=$(echo "$SCRIPT" | jq -r '.id')

echo "Triggering render job..."
RENDER=$(curl -sS -X POST "$ORCH_URL/render" -H 'Content-Type: application/json' -d "{\"persona_id\":\"$PERSONA_ID\",\"voice_id\":\"$VOICE_ID\",\"script_id\":\"$SCRIPT_ID\",\"avatar_id\":\"default-avatar\",\"layout\":{\"background\":\"studio\"}}")
echo "$RENDER"
JOB_ID=$(echo "$RENDER" | jq -r '.id')

echo "Polling render status..."
for i in {1..10}; do
  STATUS=$(curl -sS "$ORCH_URL/render/$JOB_ID")
  echo "$STATUS"
  DONE=$(echo "$STATUS" | jq -r '.status')
  if [ "$DONE" = "complete" ]; then
    break
  fi
  sleep 2

done

echo "Signed URL:"
SIGNED=$(curl -sS "$ORCH_URL/render/$JOB_ID" | jq -r '.artifacts.final_video')
echo "$SIGNED"
