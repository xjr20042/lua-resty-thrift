local ThriftHandler = {}

function ThriftHandler:testVoid()
    print('testVoid 111')
end
function ThriftHandler:testString()
    return 'hello world!'
end

return ThriftHandler
