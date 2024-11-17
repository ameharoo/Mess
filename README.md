![example workflow](https://github.com/ameharoo/Mess/actions/workflows/release.yml/badge.svg)
# Mess 
are extensible and language-neutral Mess(-ages Embedded Style Serialization).  
Supported backends:
- C++
- Python
- C# (in progress)
- PHP (in progress)
- ImHex Pattern Language

Although this project is developed for a smart home project, it can be used anywhere.

### Motivation
This project was created for a language-independent protocol description, with an emphasis on an alloc-free, copy-free implementation for c++, since the generated files are used on microcontrollers, where performance and every byte of data are important.

### Pros
- **Language-independent protocol description**
- **Alloc-free and zero-copy** on C++ Backend
-   An architecture that allows you to **quickly implement a new backend**
-   **Support for protocol versioning** <br>hashing the protocol version and embedding it in the message
- [Add new](https://github.com/ameharoo/Mess/issues)

### Cons  
- **Few backends implemented.** <br>You can help with this :3 Just [create a PR](https://github.com/ameharoo/Mess/pulls ) and I will gladly consider it
- **No Map message (VarDictionary).** <br>Still in development, non-trivial task: need to save alloc-free zero-copy for c++. If you have any ideas, please describe in Issues
- [Add new](https://github.com/ameharoo/Mess/issues)

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

## Usage
### By CMakeLists.txt:
Define variables `${MESS_DIRECTORY}`, `${MESS_SOURCE}` and `${MESS_TARGET}`, then include CMakeLists.txt.
Full usage you can see in [this example](examples/cpp).

#### More information:
1. Define variables:
- `${MESS_DIRECTORY}` Path to Mess folder (ex. `./Mess`)
- `${MESS_SOURCE}` Path to Mess source file (ex. `./messages/messages.ini`)
- `${MESS_TARGET}` Path to output (generated) file (`./headers/messages.h`)
- All paths can be relative.
2. Include Mess CMakeLists.txt

All of the above in your CMakeLists.txt:
```
set(MESS_DIRECTORY "${CMAKE_SOURCE_DIR}/Mess")
set(MESS_SOURCE "./messages/messages.ini")
set(MESS_TARGET "./headers/messages.h")

include(${MESS_DIRECTORY}/CMakeLists.txt)
```

### Manually
```bash
cd Mess

# Create VirtualEnv
python -m venv .venv

# Activate VirtualEnv
# Or on windows: venv\Scripts\activate.bat or venv\Scripts\Activate.ps1
source .venv/bin/activate

# Update pip
python -m pip install --upgrade pip

# Install some required modules
pip install -r requirements

# Finally usage
python mess.py cpp ./output.cpp ./source.ini
```

## Examples
[Example on c++ and cmake](examples/cpp)

