set -e
# This is used in github actions when building the wheels for distribution.
# DO NOT RUN THIS SCRIPT OUTSIDE OF THAT!!!
pip install lalsuite
# DEBUG COMMAND BELOW. THIS MUST BE REMOVED
#pip install --upgrade git+https://github.com/spxiwh/delocate.git

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Needed for linux
    cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
    ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.*libs/liblal-*so* /usr/lib/liblal.so
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac names are quite different
    #sudo conda install -c conda-forge liblal
    #conda init
    #source ~/.bashrc
    #conda activate root
    #echo "conda activate root" >> ~/.bashrc
    #echo `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/
    #sudo echo `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/
    #sudo ls `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/
    #export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:`python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/
    #echo "export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:`python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/" >> ~/.bashrc 
    sudo cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/lib*dylib /usr/local/lib
    sudo cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.dylibs/liblal.*.dylib /usr/local/lib/liblal.dylib

fi # Don't consider anything else at present
