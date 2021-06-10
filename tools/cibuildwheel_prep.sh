set -e
# This is used in github actions when building the wheels for distribution.
# DO NOT RUN THIS SCRIPT OUTSIDE OF THAT!!!
pip install lalsuite
# DEBUG COMMAND BELOW. THIS MUST BE REMOVED
pip install --upgrade git+https://github.com/spxiwh/delocate.git

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Needed for linux
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
    ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.*libs/liblal-*so* /usr/lib/liblal.so
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac names are quite different
    mkdir -p ~/lib
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/lib*dylib ~/lib
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/liblal.*.dylib ~/lib/liblal.dylib
    sudo cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/lib*dylib /usr/local/lib
    sudo cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/liblal.*.dylib /usr/local/lib/liblal.dylib

fi # Don't consider anything else at present
