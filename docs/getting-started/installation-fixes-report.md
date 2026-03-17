# Installation Documentation Fixes Report

**Date:** 2026-03-17
**Environment:** Ubuntu 24.04 LTS (Noble Numbat), LLVM 18.1.3, Python 3.12.3

This report summarizes all errors encountered while following `docs/getting-started/installation.md` and the corresponding fixes applied.

---

## Files Edited

### 1. `docs/getting-started/installation.md` (documentation)

| Section | Original (Incorrect) | Fix Applied | Reason |
|---------|---------------------|-------------|--------|
| Install System Dependencies | `sudo apt-get install -y llvm-dev mlir-tools libmlir-dev` | Changed to versioned packages: `llvm-18-dev mlir-18-tools libmlir-18-dev` | On Ubuntu 24.04, unversioned MLIR packages (`mlir-tools`, `libmlir-dev`) do not exist. Only versioned packages (e.g. `mlir-18-tools`, `libmlir-18-dev`) are available. |
| Install System Dependencies | Missing `python3-venv` package | Added `python3-venv` to apt install command | Required for creating virtual environments on Ubuntu 24.04+. |
| Clone and Build | `ninja -C build pycc pyc-opt` | Changed to `ninja -C build pycc` with note that pyc-opt is optional | `pyc-opt` target is only available when `MLIRRegisterAllPasses` is found. With system LLVM 18 packages, this target does not exist, causing `ninja: error: unknown target 'pyc-opt'`. |
| Install Python Package | `pip install -e .` (bare pip) | Added virtual environment creation step: `python3 -m venv .venv && source .venv/bin/activate` before `pip install -e .` | Ubuntu 24.04 enforces PEP 668 (externally-managed-environment). Running `pip install` outside a venv fails with `error: externally-managed-environment`. |
| Install Python Package | `python -c "import pycircuit; print(pycircuit.__version__)"` | Changed to `python -c "import pycircuit; print('pycircuit imported successfully')"` | The `pycircuit` module does not expose a `__version__` attribute, causing `AttributeError`. |
| Verify Your Setup | Expected output: `Compiling counter... OK` etc. | Replaced with a direct quick smoke test command and noted the full suite separately | The actual `run_examples.sh` script output format differs from what was documented. It also runs an API hygiene check first. |
| Troubleshooting | (new section) | Added "LLVM Duplicate CommandLine Option Crash" section | When linking static LLVM component libraries alongside the shared `libLLVM.so`, duplicate CommandLine option registration causes a crash. This is a common pitfall on Ubuntu with system LLVM packages. |

### 2. `compiler/mlir/CMakeLists.txt` (build system)

**Change:** Added automatic detection of shared `MLIR` and `LLVM` library targets. When both shared targets are available (typical for Ubuntu system packages), the build links against them instead of individual static component libraries.

**Reason:** The original CMakeLists.txt linked against static MLIR component libraries (e.g. `MLIRArithDialect`, `MLIRFuncDialect`) and `LLVMSupport`. On Ubuntu, these static libraries coexist with the shared `libLLVM.so.18.1`, causing duplicate symbol registration at runtime — specifically, the `debug-counter` CommandLine option is registered twice, leading to an immediate crash on any invocation of `pycc`.

### 3. `compiler/mlir/lib/Transforms/CombCanonicalizePass.cpp` (source code)

**Change:** Added `#include "llvm/Config/llvm-config.h"` and wrapped LLVM 19+ API calls with version guards:
- `cfg.enableFolding()` → guarded with `#if LLVM_VERSION_MAJOR >= 19`
- `applyPatternsGreedily(...)` → falls back to `applyPatternsAndFoldGreedily(...)` for LLVM 18

**Reason:** The code used `applyPatternsGreedily` and `GreedyRewriteConfig::enableFolding()`, which are LLVM 19+ APIs. With LLVM 18, `applyPatternsGreedily` was named `applyPatternsAndFoldGreedily`, and `enableFolding()` did not exist on `GreedyRewriteConfig`. Build failed with: `error: 'enableFolding' is not a member of 'mlir::GreedyRewriteConfig'` and `error: 'applyPatternsGreedily' was not declared in this scope`.

### 4. `compiler/mlir/lib/Transforms/InlineFunctionsPass.cpp` (source code)

**Change:** Added `#include "mlir/IR/BuiltinOps.h"`.

**Reason:** The file uses `mlir::ModuleOp` but did not include the header that defines it. With LLVM 18 system headers, `ModuleOp` is not transitively included, causing: `error: 'ModuleOp' was not declared in this scope`.

### 5. `compiler/mlir/tools/pycc.cpp` (source code)

**Change:** Replaced `outputFilename = directCppOut` and `outputFilename = directVerilogOut` with `outputFilename.setValue(directCppOut)` and `outputFilename.setValue(directVerilogOut)`. Same for `emitKind`.

**Reason:** `llvm::cl::opt<std::string>` has a deleted copy-assignment operator in LLVM 18. The `.setValue()` method is the correct way to update the value. Build failed with: `error: use of deleted function 'llvm::cl::opt<...>::operator=(const llvm::cl::opt<...>&)'`.

---

## Summary of Error Categories

1. **Package naming (doc):** Ubuntu versioned LLVM/MLIR package names differ from the unversioned names in the docs.
2. **PEP 668 compliance (doc):** Ubuntu 24.04 requires a virtual environment for pip installs.
3. **LLVM API version incompatibility (source):** Three source files used LLVM 19+ APIs not available in LLVM 18.
4. **Shared/static library linking conflict (build system):** Mixing static LLVM component libraries with the shared `libLLVM.so` caused duplicate symbol crashes.
5. **Incorrect verification commands (doc):** `__version__` attribute doesn't exist; `pyc-opt` build target may not exist; expected output format was inaccurate.
