#!/usr/bin/env bash
set -euo pipefail

# Security scan using Bandit. Produces:
# - bandit-report.txt
# - bandit_exit_code.txt
# Also appends a human-readable summary to GitHub Step Summary if available.

TARGETS=${1:-"mcp_tools scripts tests"}
REPORT_FILE="bandit-report.txt"
EXIT_FILE="bandit_exit_code.txt"

echo "[bandit] Scanning targets: ${TARGETS}"

# Run bandit recursively; do not fail the script immediately so we can capture and report
set +e
bandit -r ${TARGETS} -f txt -o "${REPORT_FILE}"
CODE=$?
set -e

echo "${CODE}" > "${EXIT_FILE}"
echo "[bandit] Exit code: ${CODE} (0 means no issues)"

# Append to GitHub Step Summary if available
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  {
    echo "## Bandit Security Scan"
    echo "Targets: ${TARGETS}"
    echo "Exit code: ${CODE}"
    echo
    if [[ -f "${REPORT_FILE}" ]]; then
      echo '```text'
      sed -e 's/\r$//' "${REPORT_FILE}"
      echo '```'
    else
      echo "No bandit report generated"
    fi
  } >> "$GITHUB_STEP_SUMMARY"
fi

echo "[bandit] Report: ${REPORT_FILE}"
echo "[bandit] Exit code saved to: ${EXIT_FILE}"
