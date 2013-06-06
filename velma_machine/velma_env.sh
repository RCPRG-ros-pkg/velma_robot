#!/usr/bin/env bash

source /opt/ros/groovy/setup.bash

export ROS_PACKAGE_PATH=/home/konradb3/ros-groovy:/opt/ros-local/groovy/stacks:$ROS_PACKAGE_PATH

source `rosstack find orocos_toolchain`/env.sh

RTTLUA_MODULES=`rospack find ocl`/lua/modules/?.lua
if [ "x$LUA_PATH" == "x" ]; then
    LUA_PATH=";;"
fi

export LUA_PATH="$LUA_PATH;$RTTLUA_MODULES"
exec "$@"
