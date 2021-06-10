set -e
# This is used in github actions when building the wheels for distribution.
# Do not run this outside of that!
python -m pip install --upgrade pip
echo `python --version`
echo `pip --version`
python -m pip install lalsuite
cp `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/lib*so* /usr/lib
ln -sf `python -c 'import sys; print (sys.path[-1])'`/lalsuite.libs/liblal-*so* /usr/lib/liblal.so
