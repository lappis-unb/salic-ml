#!/bin/bash

echo "RUN sudo docker run --rm -it -v "$PWD":/salic-ml salic-ml bash"

sudo docker run --rm -it -v "$PWD":/salic-ml salic-ml bash
