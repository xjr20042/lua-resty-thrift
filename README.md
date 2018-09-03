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
	2. create thrift lua client (thrift 0.9.3) 
	   用thrift命令生成thrift客户端
	   :> thrift gen -lua tets.thrift
	3. 将生成的文件拷贝openresty安装目录下的lualib/resty/thrift/thrift-idl/目录
	   :>cp gen-lua/*_Service.lua /${openresty.path}/lualib/resty/thrift/thrift-idl/
	4. :> cp gen-lua/*_ttypes.lua /${openresty.path}/lualib/resty/thrift/thrift-idl/
	5. Replace *_Service.lua *_Service.lua `require`
	   由于thrift生成的文件都是全局变量，而openresty建议使用的是local变量，因此需要把生成的文件变量改掉。
	   *_ttypes.lua:
	   local Thrift = require 'resty.thrift.thrift-lua.Thrift' -- local 方式引入变量
       local TType = Thrift[1] -- TType 变量被存放在Thrift数组里，下面变量同理
       local TMessageType = Thrift[2]
       local __TObject = Thrift[3]
       local TException = Thrift[4]
       local TApplicationException = Thrift[5]
       local __TClient = Thrift[6]
       
       *_Service.lua:
       local Thrift = require 'resty.thrift.thrift-lua.Thrift'
       local TType = Thrift[1]
       local TMessageType = Thrift[2]
       local __TObject = Thrift[3]
       local TException = Thrift[4]
       local TApplicationException = Thrift[5]
       local __TClient = Thrift[6]
	6. 拷贝本项目下的所有so包到/usr/local/lib/ 如果该目录不在系统加载so包的默认设置里，可以手动一下，或者将so包放到/usr/lib/里
	   :> cp lua-resty-thrift/lib/*.so /usr/local/lib/
	7. 添加so包后需要让so包被加载
	   :> ldconfig	   
	
       
使用generate_resty.py自动生成服代码
以ThriftTest.thrift为例
1.使用generate_resty.py ThriftTest.thrift 生成server和client依赖的代码。
	ThriftTest_ThriftTest.lua 是thrift生成的代码，server和client都依赖，请放到 resty/thrift/thrift-idl/目录
	server：
		ThriftTestServer.lua 是自动生成的代码，server端使用，在nginx.conf 配置content_by_lua_file ThriftTestServer.lua 来启动server服务。
		ThriftTestHandler.lua 是使用者需要创建并编辑的文件，由ThriftTestServer.lua 调用, 请在里面实现thrift文件定义的rpc方法。
	client:
		请参考test_rpc.lua
