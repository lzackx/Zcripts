#!/bin/bash

set -e
set -x

echo $*

PATH_OF_WORKING_DIRECTORY=$(
    cd "$(dirname "$0")/"
    pwd
)
PATH_OF_PROJECT_DIRECTORY=$(
    cd "$(dirname "$0")/../"
    pwd
)
PATH_OF_METRO_ENTRY_FILE="$PATH_OF_PROJECT_DIRECTORY/bundle.base.js"
PATH_OF_BUNDLE_OUTPUT_FILE="$PATH_OF_PROJECT_DIRECTORY/bundles/android/base/android.base.jsbundle"
PATH_OF_BUNDLE_ASSETS_DEST_DIRECTORY="$PATH_OF_PROJECT_DIRECTORY/bundles/android/base"
PATH_OF_METRO_CONFIG_FILE="$PATH_OF_PROJECT_DIRECTORY/metro.base.android.config.js"

BUNDLE_MODE_IS_DEV=false

cd $PATH_OF_PROJECT_DIRECTORY

while getopts ":i:d" opt; do
    case $opt in
    i)
        echo "install dependency forcely"
        yarn --force install
        ;;
    d)
        echo "bundle in dev mode"
        BUNDLE_MODE_IS_DEV=true
        ;;
    ?)
        print "Usage: $0 [-i] [-d]"
        print "-i:  install dependency forcely"
        print "-d:  bundle in dev mode"
        exit 1
        ;;
    esac
done

react-native bundle --platform android \
    --dev $BUNDLE_MODE_IS_DEV \
    --entry-file $PATH_OF_METRO_ENTRY_FILE \
    --bundle-output $PATH_OF_BUNDLE_OUTPUT_FILE \
    --assets-dest $PATH_OF_BUNDLE_ASSETS_DEST_DIRECTORY \
    --config $PATH_OF_METRO_CONFIG_FILE \
    --verbose
