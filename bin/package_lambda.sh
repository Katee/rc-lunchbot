#! /bin/bash
PYTHON_VERSION="3.6"
PACKAGE='tmp-package'
OUTPUT='package.zip'

# remove files/folders we will use if they already exist
if [ -d $PACKAGE ]; then
  rm -r $PACKAGE
fi
if [ -f $OUTPUT ]; then
  rm -r $OUTPUT
fi

mkdir -p "$PACKAGE/code"
cd $PACKAGE

# set up virtualenv and install dependencies
virtualenv --python=python$PYTHON_VERSION .
source bin/activate
pip install -r ../requirements.txt

# copy files for this project
cp ../bot.py ../utils.py code

# copy in the site packages
cp -r lib/python$PYTHON_VERSION/site-packages/* code
cd code
zip -r -q ../../$OUTPUT *
cd ../../

# cleanup
rm -r $PACKAGE

echo "$PACKAGE created and ready to upload."
