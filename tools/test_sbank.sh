set -e
# Run sbank to generate XML and HDF banks
./sbank --approximant IMRPhenomD --aligned-spin --mass1-min 15.0 --mass1-max 25.0 --spin1-min 0.0 --spin1-max 0.5 --match-min 0.97 --flow 20.0 --noise-model aLIGOZeroDetHighPower --output-filename BBH-IMRPhenomD-aLIGOZeroDetHighPower.xml --convergence-threshold 45

./sbank --approximant IMRPhenomD --aligned-spin --mass1-min 15.0 --mass1-max 25.0 --spin1-min 0.0 --spin1-max 0.5 --match-min 0.97 --flow 20.0 --noise-model aLIGOZeroDetHighPower --output-filename BBH-IMRPhenomD-aLIGOZeroDetHighPower.hdf --convergence-threshold 25

XML_SIZE=`ligolw_print BBH-IMRPhenomD-aLIGOZeroDetHighPower.xml -t sngl_inspiral | wc -l`
HDF_SIZE=`h5ls BBH-IMRPhenomD-aLIGOZeroDetHighPower.hdf | grep "spin1z" | awk '{print $3}'`
HDF_SIZE="${HDF_SIZE:1:3}"

if ((XML_SIZE >= 140 && XML_SIZE <= 160)); then
  exit 1
fi

if ((HDF_SIZE >= 240 && HDF_SIZE <= 260)); then
  exit 1
fi

