set -e
# This is used in github actions when building the wheels for distribution.
# Do not run this outside of that!
pip install lalsuite

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Needed for linux
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
    ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.*libs/liblal-*so* /usr/lib/liblal.so
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac names are quite different
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/lib*dylib /usr/lib
    ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/liblal.*.dylib /usr/lib/liblal.dylib
fi # Don't consider anything else at present
