set -e
# This is used in github actions when building the wheels for distribution.
# Do not run this outside of that!
pip install lalsuite
ls `python -c 'import sys; print (sys.path[-1])'`
ls `python -c 'import sys; print (sys.path[-1])'`/lalsimulation/_lalsimulation*.so
otool -L `python -c 'import sys; print (sys.path[-1])'`/lalsimulation/_lalsimulation*.so
ls `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/
cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/liblal-*so* /usr/lib/liblal.so
