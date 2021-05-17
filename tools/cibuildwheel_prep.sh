pip install lalsuite
cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/liblal-*so* /usr/lib
ln -s /usr/lib/liblal-*so* /usr/lib/liblal.so
