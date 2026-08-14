#!/bin/sh
set -e

ARCHC_PATH="${ARCHC_PATH:-/Volumes/External/Code/ArchC}"
SYSTEMC_PATH="${SYSTEMC_PATH:-/opt/homebrew/opt/systemc}"
ACSIM_BIN="${ARCHC_PATH}/src/acsim/acsim"

echo "=== Running ArchC Simulator Generator (acsim -nw -nci) ==="
mkdir -p ~/.archc
cp -f "${ARCHC_PATH}/archc.conf" ~/.archc/archc.conf 2>/dev/null || true
"${ACSIM_BIN}" "parsed_archc_isa.ac" -nw -nci

# Setup syscall stubs if missing
if [ ! -f parsed_archc_isa_syscall.H ] && [ -f parsed_archc_isa_syscall.H.tmpl ]; then
    cp parsed_archc_isa_syscall.H.tmpl parsed_archc_isa_syscall.H
fi
if [ ! -f parsed_archc_isa_syscall.cpp ] && [ -f parsed_archc_isa_syscall.cpp.tmpl ]; then
    cp parsed_archc_isa_syscall.cpp.tmpl parsed_archc_isa_syscall.cpp
fi

echo "=== Compiling SystemC Simulator with Clang++ (-O3 -march=native) ==="
clang++ -std=c++17 -O3 -march=native -DAC_MATCH_ENDIANNESS -Wno-deprecated \
  -Dstat64=stat -Dlstat64=lstat -Dfstat64=fstat \
  -I. \
  -I"${ARCHC_PATH}/src/aclib/ac_core" \
  -I"${ARCHC_PATH}/src/aclib/ac_decoder" \
  -I"${ARCHC_PATH}/src/aclib/ac_storage" \
  -I"${ARCHC_PATH}/src/aclib/ac_syscall" \
  -I"${ARCHC_PATH}/src/aclib/ac_utils" \
  -I"${ARCHC_PATH}/src/aclib/ac_stats" \
  -I"${ARCHC_PATH}/src/aclib/ac_gdb" \
  -I"${ARCHC_PATH}/src/aclib/ac_tlm" \
  -I"${ARCHC_PATH}/src/aclib/ac_rtld" \
  -I"${ARCHC_PATH}/src/aclib/ac_cache" \
  -I"${ARCHC_PATH}/src/aclib" \
  -I"${SYSTEMC_PATH}/include" \
  main.cpp parsed_archc_isa_arch.cpp parsed_archc_isa_arch_ref.cpp parsed_archc_isa.cpp parsed_archc_isa_syscall.cpp \
  "${ARCHC_PATH}/src/aclib/.libs/libarchc.a" \
  -L"${SYSTEMC_PATH}/lib" -lsystemc -lm \
  -o parsed_archc_isa.x

echo "=== Successfully built SystemC simulator: parsed_archc_isa.x ==="