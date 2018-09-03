local GenericObjectPool = require "resty.thrift.GenericObjectPool"
local TestServiceClient = require "resty.thrift.thrift-idl.taskmgr_TaskMgr" [1]
local ngx = ngx
local client = GenericObjectPool:connection(TestServiceClient,'10.100.14.251',2998)
local cmd = "{\"dev_ids\":[\"V200V200V200V20\"]}"
--local res = client:queryDev(cmd)
local res = client:notify(1)
GenericObjectPool:returnConnection(client)
--GenericObjectPool:closeConnection(client)
ngx.say(res)
