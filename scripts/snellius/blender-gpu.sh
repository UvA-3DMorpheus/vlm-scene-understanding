#!/usr/bin/env bash
# Blender wrapper for the simulation pipeline on a GPU node.
#
# The 3D-Simulations Blender script selects Apple's METAL backend and falls back to the CPU
# elsewhere. Blender's Cycles add-on also reads `--cycles-device <backend>` from the script
# arguments (after `--`) and forces that device at the engine level, and the pipeline's script
# only reads the two arguments that precede it. Appending the flag here therefore moves the
# render to the GPU without changing the pipeline's code.
#
# BLENDER_REAL: the Blender executable; BLENDER_COMPUTE_DEVICE: CUDA, OPTIX, OPTIX+CPU, ... (default OPTIX).
set -euo pipefail
real="${BLENDER_REAL:?set BLENDER_REAL to the Blender executable}"
exec "${real}" "$@" --cycles-device "${BLENDER_COMPUTE_DEVICE:-OPTIX}"
