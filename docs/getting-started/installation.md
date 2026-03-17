# Installation Guide

This guide covers setting up the pyCircuit development environment.

## System Requirements

| Component | Minimum Version | Recommended Version |
|-----------|---------------|---------------------|
| Python | 3.9 | 3.10+ |
| LLVM | 17 | 19 |
| CMake | 3.20 | 3.28+ |
| Ninja | 1.10 | Latest |

## Install System Dependencies

### Ubuntu/Debian

```bash
# Update package lists
sudo apt-get update

# Install build tools and Python venv support
sudo apt-get install -y cmake ninja-build python3 python3-pip python3-venv clang

# Install LLVM/MLIR (Ubuntu 22.04+)
# Note: On Ubuntu, LLVM/MLIR packages use versioned names.
# Replace "18" below with the LLVM version available on your system
# (run `apt-cache search mlir-.*-tools` to discover available versions).
sudo apt-get install -y llvm-18-dev mlir-18-tools libmlir-18-dev

# Verify installation
llvm-config-18 --version
mlir-opt-18 --version
```

> **Note (Ubuntu 24.04+):** The unversioned packages `llvm-dev`, `mlir-tools`,
> and `libmlir-dev` may not be available. Always use the versioned package names
> (e.g. `llvm-18-dev`, `mlir-18-tools`, `libmlir-18-dev`). If your system
> provides `llvm-config` (unversioned symlink), you can use that instead of
> `llvm-config-18`.

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install build tools
brew install cmake ninja python@3

# Install LLVM with MLIR
brew install llvm
# Add LLVM to PATH
echo 'export PATH="$(brew --prefix llvm)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
llvm-config --version
```

## Clone and Build

```bash
# Clone the repository
git clone https://github.com/LinxISA/pyCircuit.git
cd pyCircuit

# Configure with CMake
LLVM_DIR="$(llvm-config --cmakedir)"
MLIR_DIR="$(dirname "$LLVM_DIR")/mlir"

cmake -G Ninja -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_DIR="$LLVM_DIR" \
  -DMLIR_DIR="$MLIR_DIR"

# Build the compiler (pycc only; pyc-opt is optional and may not build
# on all systems due to MLIRRegisterAllPasses availability)
ninja -C build pycc

# Verify the build
./build/bin/pycc --version
```

## Alternative: Use Build Script

```bash
# The project includes a build script that handles LLVM detection
bash flows/scripts/pyc build
```

## Install Python Package

```bash
# Create and activate a Python virtual environment
# (required on Ubuntu 24.04+ due to PEP 668 externally-managed environments)
python3 -m venv .venv
source .venv/bin/activate

# Install pycircuit in development mode
pip install -e .

# Verify installation
python -c "import pycircuit; print('pycircuit imported successfully')"
```

> **Note:** On Ubuntu 24.04+, running `pip install` outside of a virtual
> environment will fail with an `externally-managed-environment` error.
> Always create a venv first as shown above.

## Verify Your Setup

```bash
# Make sure the venv is activated
source .venv/bin/activate

# Quick compiler smoke test (emit + compile a single example)
PYTHONPATH="$(pwd)/compiler/frontend" \
  python3 -m pycircuit.cli emit designs/examples/counter/counter.py -o /tmp/counter.pyc
./build/bin/pycc /tmp/counter.pyc --emit=cpp -cpp /tmp/counter.cpp
# Should print stats and exit 0

# Full smoke test (runs all examples + API hygiene checks)
bash flows/scripts/run_examples.sh
```

## Troubleshooting

### LLVM Not Found

If CMake can't find LLVM, set the paths explicitly:

```bash
export LLVM_DIR=/path/to/llvm/lib/cmake/llvm
export MLIR_DIR=/path/to/mlir/lib/cmake/mlir
cmake -G Ninja -S . -B build ...
```

### Python Version Issues

pyCircuit requires Python 3.9+. Check your version:

```bash
python3 --version
```

If you need to install a newer Python version:

```bash
# Ubuntu
sudo apt-get install python3.11 python3.11-venv

# macOS
brew install python@3.11
```

### Build Errors

Clean and rebuild:

```bash
rm -rf build
cmake -G Ninja -S . -B build ...
ninja -C build pycc
```

### LLVM Duplicate CommandLine Option Crash

If `pycc` crashes at startup with `Option 'debug-counter' registered more than
once!`, the binary is linking both static LLVM component libraries and the
shared `libLLVM.so`, causing duplicate symbol registration.

The project's CMakeLists.txt automatically detects and links against the shared
`MLIR` / `LLVM` libraries when available (Ubuntu system packages). If you still
hit this issue, ensure `libmlir-<ver>-dev` is installed (it provides
`libMLIR.so`) and re-run the CMake configure step from a clean build directory.
