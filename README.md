Name
===
lua-resty-thrift - Lua thrift client driver for the ngx_lua based on the cosocket API

Synopsis
===

*nginx.conf:*  
```lua

   server {
       location /test{
            content_by_lua '
                local GenericObjectPool = require "resty.thrift.GenericObjectPool"
                local TestServiceClient = require "resty.thrift.thrift-idl.lua_test_TestService"
                local ngx = ngx
                local client = GenericObjectPool:connection(TestServiceClient,'127.0.0.1',9090)
                local res = client:say('thrift')
                GenericObjectPool:returnConnection(client)
                ngx.say(res)
            ';
       }
   
   }
   
```

*thrift:*
```thrift
   namespace java com.test.thrift
   namespace lua lua_test

   service TestService {
      string say(1:string request)
   }
```
	
	1. 将本项目lib目录下的resty目录拷贝到openresty的安装目录
	   :> cp lib/resty /${openresty.path}/lualib/
	2. 使用generate_resty.py自动生成代码
	以ThriftTest.thrift为例
	1) .使用generate_resty.py ThriftTest.thrift 生成server和client依赖的代码。
		ThriftTest_ThriftTest.lua 是thrift生成的代码，server和client都依赖，请放到 resty/thrift/thrift-idl/目录
		server：
			ThriftTestServer.lua 是自动生成的代码，server端使用，在nginx.conf 配置content_by_lua_file ThriftTestServer.lua 来启动server服务。
			ThriftTestHandler.lua 是使用者需要创建并编辑的文件，由ThriftTestServer.lua 调用, 请在里面实现thrift文件定义的rpc方法。
		client:
			请参考test_rpc.lua
