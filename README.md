# Mess 
are extensible and language-neutral Mess(-ages Embedded Style Serialization).  
Supported backends:
- C++
- Python (in progress)
- C# (in progress)
- PHP (in progress)
- ImHex Pattern Language (in progress)

## Message declaration
Message is described using ini-like format like this:
```ini
[.Protocol]
name = TestProto
hash_bytes_count = 1

[Color]
r = Int8
g = Int8
b = Int8

# My awesome message <3
[MessageName]
field_char = Int8
field2_long = Int64
field_float_array = VarArray<Float>
field_string = VarArray<Int8>
field_color = Color
# You can provide doc information for
# specified field and mess will take that into account!
field_color_array = VarArray<Color>
```

Supported types:
- Int8
- Int16
- Int32
- Int64
- Float
- Fixed16 (possible rename later)
- Fixed32 (possible rename later)

And generic types:
- VarArray\<Type\>
- VarDictionary\<Type, Type\> (in progress)


## Examples
[Example on c++ and cmake](examples/cpp)

