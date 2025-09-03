#!/usr/bin/env bash
set -euo pipefail

EXIT_FILE="bandit_exit_code.txt"
CODE=0

if [[ -f "${EXIT_FILE}" ]]; then
  CODE=$(cat "${EXIT_FILE}" || echo 0)
fi

echo "[bandit] Enforcing failure policy. Exit code from scan: ${CODE}"

if [[ "${CODE}" -ne 0 ]]; then
  echo "Bandit found issues (exit ${CODE}). Failing the job."
  exit "${CODE}"
else
  echo "No Bandit issues detected."
fi

