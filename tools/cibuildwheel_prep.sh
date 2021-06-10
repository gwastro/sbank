set -e
# This is used in github actions when building the wheels for distribution.
# DO NOT RUN THIS SCRIPT OUTSIDE OF THAT!!!
#pip install lalsuite
# DEBUG COMMAND BELOW. THIS MUST BE REMOVED
pip install --upgrade git+https://github.com/spxiwh/delocate.git

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Needed for linux
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
    ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.*libs/liblal-*so* /usr/lib/liblal.so
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac names are quite different
    conda install -c conda-forge lalsuite
    #sudo echo "export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:`python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/" >> /etc/bashrc
    #sudo cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/lib*dylib /usr/local/lib
    #sudo cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/liblal.*.dylib /usr/local/lib/liblal.dylib

fi # Don't consider anything else at present
