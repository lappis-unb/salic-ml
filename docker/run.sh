#!/bin/bash

if [[ -n $1 ]]; then
	PORT=$1
else
	PORT='8888'
fi

echo "RUN sudo docker run --rm -it -v \"$PWD\":/salic-ml -p $PORT:$PORT salic-ml bash"
sudo docker run --rm -it -v "$PWD":/salic-ml -p $PORT:$PORT salic-ml bash
