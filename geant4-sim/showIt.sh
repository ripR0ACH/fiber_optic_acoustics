#!/bin/bash
cd build
make install -j20
cd ../install/bin/
`./lightGuide`
cd ../../
