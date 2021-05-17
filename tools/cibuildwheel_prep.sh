pip install lalsuite
cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
ln -sf /usr/lib/liblal-*so* /usr/lib/liblal.so
