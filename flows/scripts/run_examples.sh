#!/usr/bin/env bash
set -euo pipefail

# Run all folderized examples through emit + pycc (cpp) to sanity-check the
# compiler/codegen pipeline.

source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
pyc_find_pycc

PYTHONPATH_VAL="$(pyc_pythonpath)"
EX_DIR="${PYC_ROOT_DIR}/designs/examples"
DISCOVER="${PYC_ROOT_DIR}/flows/tools/discover_examples.py"
EXAMPLE_TIER="${PYC_EXAMPLE_TIER:-normal}"
API_HYGIENE_TARGETS=(
  "compiler/frontend/pycircuit"
  "designs/examples"
)
CPP_SKIP_EXAMPLES=(
  "calculator"
)
PROJECT_BUILD_SMOKE_EXAMPLES=(
  "counter"
)

if [[ -n "${PYC_API_HYGIENE_TARGETS:-}" ]]; then
  # Allow callers/CI to widen or narrow the scan scope without editing the script.
  # The default excludes docs so setup verification is not blocked by stale prose.
  # shellcheck disable=SC2206
  API_HYGIENE_TARGETS=(${PYC_API_HYGIENE_TARGETS})
fi

if [[ -n "${PYC_CPP_SKIP_EXAMPLES:-}" ]]; then
  # shellcheck disable=SC2206
  CPP_SKIP_EXAMPLES=(${PYC_CPP_SKIP_EXAMPLES})
fi

if [[ -n "${PYC_PROJECT_BUILD_SMOKE_EXAMPLES:-}" ]]; then
  # shellcheck disable=SC2206
  PROJECT_BUILD_SMOKE_EXAMPLES=(${PYC_PROJECT_BUILD_SMOKE_EXAMPLES})
fi

if [[ ! -d "${EX_DIR}" ]]; then
  pyc_die "examples dir not found: ${EX_DIR}"
fi

pyc_log "using pycc: ${PYCC}"

pyc_log "running strict API hygiene gate"
python3 "${PYC_ROOT_DIR}/flows/tools/check_api_hygiene.py" \
  "${API_HYGIENE_TARGETS[@]}"

fail=0
count=0
skip_example() {
  local name="$1"
  local item
  for item in "${CPP_SKIP_EXAMPLES[@]}"; do
    if [[ "${item}" == "${name}" ]]; then
      return 0
    fi
  done
  return 1
}

while IFS=$'\t' read -r bn design _tb _cfg _tier; do
  [[ -n "${bn}" ]] || continue
  if skip_example "${bn}"; then
    pyc_log "skip ${bn} (excluded from default cpp smoke)"
    continue
  fi

  count=$((count+1))
  out_root="$(pyc_out_root)/example-smoke/${bn}"
  rm -rf "${out_root}" >/dev/null 2>&1 || true
  mkdir -p "${out_root}"
  pyc_file="${out_root}/${bn}.pyc"
  cpp_dir="${out_root}/cpp"

  pyc_log "[${count}] emit ${bn}"
  if ! PYTHONPATH="${PYTHONPATH_VAL}" python3 -m pycircuit.cli emit "${design}" -o "${pyc_file}"; then
    pyc_warn "emit failed: ${bn}"
    fail=1
    continue
  fi

  pyc_log "[${count}] compile(cpp) ${bn}"
  if ! "${PYCC}" "${pyc_file}" \
      --emit=cpp \
      --cpp-split=module \
      --out-dir="${cpp_dir}" \
      --logic-depth=64; then
    pyc_warn "pycc failed: ${bn}"
    fail=1
    continue
  fi

  # Basic artifact check.
  if [[ ! -f "${cpp_dir}/cpp_compile_manifest.json" ]]; then
    pyc_warn "missing cpp_compile_manifest.json: ${bn}"
    fail=1
  fi

done < <(python3 "${DISCOVER}" --root "${EX_DIR}" --tier "${EXAMPLE_TIER}" --format tsv)

# Project build flow smoke checks (multi-.pyc + parallel pycc + CMake/Ninja).
for bex in "${PROJECT_BUILD_SMOKE_EXAMPLES[@]}"; do
  ex="${EX_DIR}/${bex}/tb_${bex}.py"
  [[ -f "${ex}" ]] || continue
  count=$((count+1))
  out_root="$(pyc_out_root)/example-build-smoke/${bex}"
  rm -rf "${out_root}" >/dev/null 2>&1 || true
  mkdir -p "${out_root}"
  pyc_log "[${count}] build ${bex}"
  if ! PYTHONPATH="${PYTHONPATH_VAL}" python3 -m pycircuit.cli build \
      "${ex}" \
      --out-dir "${out_root}" \
      --target cpp \
      --jobs "${PYC_EXAMPLE_JOBS:-4}" \
      --logic-depth 64; then
    pyc_warn "build failed: ${bex}"
    fail=1
    continue
  fi
  if [[ ! -f "${out_root}/project_manifest.json" ]]; then
    pyc_warn "missing project_manifest.json: ${bex}"
    fail=1
  fi
done

if [[ "${fail}" -ne 0 ]]; then
  pyc_die "one or more examples failed"
fi

pyc_log "all examples passed"
