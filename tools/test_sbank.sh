set -e

PREFIX=$(python -c "import sys; print(sys.prefix)")
PYTHON="python -m coverage run --append"

# Run sbank to generate XML and HDF banks
${PYTHON} ${PREFIX}/bin/sbank --approximant IMRPhenomD --aligned-spin --mass1-min 15.0 --mass1-max 25.0 --spin1-min 0.0 --spin1-max 0.5 --match-min 0.97 --flow 20.0 --noise-model aLIGOZeroDetHighPower --output-filename BBH-IMRPhenomD-aLIGOZeroDetHighPower.xml --convergence-threshold 25

${PYTHON} ${PREFIX}/bin/sbank --approximant IMRPhenomD --aligned-spin --mass1-min 15.0 --mass1-max 25.0 --spin1-min 0.0 --spin1-max 0.5 --match-min 0.97 --flow 20.0 --noise-model aLIGOZeroDetHighPower --output-filename BBH-IMRPhenomD-aLIGOZeroDetHighPower.hdf --convergence-threshold 25

XML_SIZE=`ligolw_print BBH-IMRPhenomD-aLIGOZeroDetHighPower.xml -t sngl_inspiral | wc -l`
HDF_SIZE=`h5ls BBH-IMRPhenomD-aLIGOZeroDetHighPower.hdf | grep "spin1z" | awk '{print $3}'`
HDF_SIZE="${HDF_SIZE:1:3}"

if ((XML_SIZE < 140 || XML_SIZE > 160)); then
  echo "The XML bank is not the expected size " ${XML_SIZE}
  exit 1
fi

if ((HDF_SIZE < 140 || HDF_SIZE > 160)); then
  echo "The HDF bank is not the expected size " ${HDF_SIZE}
  exit 1
fi


## We can check ecc bank but currently, waveform approx is not openly available.
## Bank works only in hdf form.
# sbank --approximant IMRPhenomXE --aligned-spin --mass1-min 20.0 --mass1-max 24.0 --spin1-min 0.0 --spin1-max 0.25 --mass2-min 15.0 --mass2-max 18.0 --spin2-min 0.0 --spin2-max 0.5 --ecc-min 0.1 --ecc-max 0.2 --f-ref 10.0 --match-min 0.97 --flow 20.0 --noise-model aLIGOZeroDetHighPower --output-filename BBH-IMRPhenomXE-aLIGOZeroDetHighPower.hdf --verbose --use-eccentric

