# $1 is file name
#echo "file name is "$1
cd build
make install -j20
cd ../install/bin
./lightGuide -m run1.mac -o $1
#./plothisto $1
cd ../../
