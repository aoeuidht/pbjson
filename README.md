pbjson
======

About
-----

pbjson is a util for json - protocol buffers converting written in python.

This repo is part of my work when I was asked to compare data-size and
cpu usage during decoding/unserializing(for no reason). It's kind of strange to compare
between schema based protocol and self-explained protocol. Anyway, I write
two scripts. One to pasrse json source file and generate .proto file and convert json(dict)
to pb msg using another.

Usage
-----

There are two python source files in this repo:

1.  schema_parse.py
2.  msg_pb2.py

### generate .proto file
The first schema_parse can parse json string(saved in a file) and generate a .proto file automatically.
Just put your .json file as the first commandline parameter like this:

>    python schema_parse.py PATH_TO_JSON_FILE

The .proto file will printed out to STDOUT(whit out formating). You may want to save it to disk using redirect.

### convert .proto file to python class definition

When you got the .proto file(let's say msg.proto), you can generate a python source file using protoc
by this command

>   protoc -I=. --python_out=. ./msg.proto 

The default generated python sourec is msg_pb2.py, you can see how the msg class defined.

### Assign python dict to pb msg