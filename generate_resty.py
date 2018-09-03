#

#python generate_resty_client.py *.thrift

import os
import sys

os.system("mkdir -p gen-resty")
os.system("thrift --gen lua -out gen-resty " + sys.argv[1])
os.system("rm gen-resty/*_constants.lua -f")
os.system("rm gen-resty/*_ttypes.lua -f")

def get_service_name(thrift_file):
    with open(thrift_file, "r") as f:
        while True:
            line = f.readline()
            if len(line) == 0:break
            if line.startswith("service "):
                if line[len(line)-1] == '\n':
                    line = line[:len(line)-1]
                pos = line.find(' ')
                if pos >= 0:
                    return line[pos:].strip()
                pos = line.find('\t')
                if pos >= 0:
                    return line[pos:].strip()
            #elif line.startswith("service\t"):
                #return

def get_file_name(fpath):
    if fpath.endswith(".thrift"):
        return fpath[:-7]
    return fpath

def get_var_name(line):
    pos = line.find(" =")
    return line[:pos].strip()
service_name = get_service_name(sys.argv[1])
#print get_file_name(sys.argv[1])

service_file = get_file_name(sys.argv[1]) + "_" + service_name+".lua"

file_head = """local Thrift = require 'resty.thrift.thrift-lua.Thrift'
local TType = Thrift[1]
local TMessageType = Thrift[2]
local __TObject = Thrift[3]
local TException = Thrift[4]
local TApplicationException = Thrift[5]
local __TClient = Thrift[6]
local __TProcessor = Thrift[7]
local ttype = Thrift[8]
local terror = Thrift[9]"""

tmp_file = "/tmp/" + service_file
head = ""
body = ""
var = []
dealing_body = False
with open("gen-resty/" + service_file, "r") as f:
    while True:
        line = f.readline()
        if len(line) == 0: break
        if line.startswith("require "):
            line = '--' + line
        if line.find("__TObject") > 0:
            dealing_body = True
            var.append(get_var_name(line))
        if not dealing_body:
            head += line
        else:
            body += line
head = head + file_head + "\n\n"
for v in var:
    head += "local " + v + "\n"
txt = head + "\n" + body
with open(tmp_file, "w+") as f:
    f.write(txt)
    f.write("\nreturn {" + service_name +"Client,"+service_name+"Iface,"+service_name+"Processor}\n")
os.system("mv " + tmp_file + " gen-resty/")

#write server.lua

server_file = service_name + "Server.lua"
with open("gen-resty/" + server_file, "w") as f:
    head = """-- auto generated code, do not edit please.
local TSocket = require "resty.thrift.thrift-lua.TSocket"
local TSocket, TServerSocket = TSocket[1],TSocket[2]
local TBuffered = require "resty.thrift.thrift-lua.TBufferedTransport"
local TBufferedTransport, TBufferedTransportFactory = TBuffered[1], TBuffered[2]
local TBinary = require "resty.thrift.thrift-lua.TBinaryProtocol"
local TBinaryProtocol, TBinaryProtocolFactory = TBinary[1], TBinary[2]
local TSimpleServer = require "resty.thrift.thrift-lua.TServer"

local ThriftService  = require "resty.thrift.thrift-idl."""
    tail = """-- Handler
local ThriftHandler = ThriftServiceIface:new(myhandler)

--------------------------------------------------------------------------------
local function run()
  -- Handler & Processor
  local handler = ThriftHandler:new{}
  local processor = ThriftServiceProcessor:new{
    handler = handler
  }
  -- Server Socket
  local socket = TServerSocket:new{}

  -- Transport & Factory
  local trans_factory = TBufferedTransportFactory:new{}
  local prot_factory = TBinaryProtocolFactory:new{}

  -- Simple Server
  local server = TSimpleServer:new{
    processor = processor,
    serverTransport = socket,
    transportFactory = trans_factory,
    protocolFactory = prot_factory
  }
  -- Serve
  server:serve()
  server = nil
end

run()"""
    body = head + get_file_name(sys.argv[1]) + "_" + service_name + "\"\n"
    body += "local ThriftServiceClient, ThriftServiceIface, ThriftServiceProcessor = ThriftService[1], ThriftService[2],ThriftService[3]\n"
    body += "local myhandler = require \""+ service_name + "Handler\"\n"
    body += tail + "\n"
    f.write(body)


