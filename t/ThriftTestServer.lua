local TSocket = require "resty.thrift.thrift-lua.TSocket"
local TSocket, TServerSocket = TSocket[1],TSocket[2]
local TBuffered = require "resty.thrift.thrift-lua.TBufferedTransport"
local TBufferedTransport, TBufferedTransportFactory = TBuffered[1], TBuffered[2]
local TBinary = require "resty.thrift.thrift-lua.TBinaryProtocol"
local TBinaryProtocol, TBinaryProtocolFactory = TBinary[1], TBinary[2]
local TSimpleServer = require "resty.thrift.thrift-lua.TServer"

local ThriftService  = require "resty.thrift.thrift-idl.ThriftTest_ThriftTest"
local ThriftServiceClient, ThriftServiceIface, ThriftServiceProcessor = ThriftService[1], ThriftService[2],ThriftService[3]
local myhandler = require "ThriftTestHandler"
-- Handler
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

run()
