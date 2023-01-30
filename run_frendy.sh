#!/bin/bash

EXE=./frendy.exe
INP_DIR=./inp_frendy
LIB_DIR=./lib
ACE_DIR=./ace

mkdir -p "${ACE_DIR}"

for CASE in H1 H2 O16 U235 U238 Zr90 Er166 Er167 Mo98 C0 Cr50 Cr52 Cr53 Cr54 Fe54 Fe56 Fe57 Fe58 Ni58 Ni60 \
            Ni61 Ni62 Ni64 Mn55 Si28 Si29 Si30 N14 N15 P31 S32 S33 S34 S36 B10 B11 Zr91 Zr92 Zr94 Zr96 \
            Mg24 Al27 Cu63 Cu65 Zn64 Pb207 HinH2O ZrinZrH HinZrH
do
  echo "${CASE}"

  INP="${INP_DIR}/inp_JENDL-4_${CASE}.dat"
  LIB="${LIB_DIR}/${CASE}.dat"

  cp -p "${LIB}" ./tape20
  if [ "${CASE}" == "HinH2O" ] || [ "${CASE}" == "HinZrH" ]; then
    cp -p "${LIB_DIR}/H001.dat"  ./tape20
    cp -p "${LIB}"               ./tape23
  elif [ "${CASE}" == "ZrinZrH" ]; then
    cp -p "${LIB_DIR}/Zr001.dat" ./tape20
    cp -p "${LIB}"               ./tape23
  fi

  "${EXE}"  "${INP}"

  mv ./tape30 "${ACE_DIR}/${CASE}.ace"
  mv ./tape31 "${ACE_DIR}/${CASE}.xsdir"
done

rm -rf ./tape*
