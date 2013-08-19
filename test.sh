#! /usr/bin/env sh
TGT=./scenario/$1
if [ ! -f $TGT ]; then
    echo $TGT
    python schema_parse.py $1 > test/msg.proto
    cd test
    protoc -I=. --python_out=. ./msg.proto && touch ../msg_pb2.py && rm ../msg_pb2.py && cp msg_pb2.py ../
    cd ..
    python pb.py $1 > $TGT
fi
