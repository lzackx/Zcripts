#!/bin/bash

set -e
set -x

# Template Variables
# product

#获取当前脚本的目录
PATH_OF_WORKING_DIRECTORY=$(cd "$(dirname "$0")";pwd)
PATH_OF_OUTPUT="${PATH_OF_WORKING_DIRECTORY}/$1"
APP_PATH="${PATH_OF_OUTPUT}/Release"

#更新依赖库
flutter packages upgrade
flutter packages get

#生成产物
flutter build ios-framework --output=$PATH_OF_OUTPUT --no-debug --no-profile -v

#删除部分sdk
function getdir(){
    echo $1
    local dir=$1
    for file in $1/*; do
    	var=$file
    	name=${var##*/}
    	if [[ $name == "Flutter.xcframework" ]]; then
    		#statements
            echo "removing ${name}"
    		rm -rf $file
    	fi
    done
}
getdir "${APP_PATH}"

#更新产物版本号
BUNDLE_PATH="${PATH_OF_WORKING_DIRECTORY}/flutter_build.bundle"

if [[ -d "${BUNDLE_PATH}" ]]; then
    #statements
    echo "update version"
    version=`date '+%Y%m%d%H%M'`
    echo -n "$version" > ${BUNDLE_PATH}/version.txt
    cp -r  ${BUNDLE_PATH} ${APP_PATH}
else
    echo "不存在flutter_build.bundle文件，请先创建"
fi

echo "Done"
