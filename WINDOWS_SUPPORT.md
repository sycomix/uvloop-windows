# Windows Support for uvloop

Starting with version X.X.X, uvloop now officially supports Windows platforms.

## Overview

uvloop is built on top of libuv, which has excellent cross-platform support including Windows. The main changes to enable Windows support in uvloop involve:

1. Removing platform restrictions in the build system
2. Adapting the build process to use CMake on Windows (libuv's preferred build system on Windows)
3. Handling platform-specific differences in system headers and libraries

## Building on Windows

### Prerequisites

To build uvloop on Windows, you need:

1. Python 3.8 or greater
2. A C compiler (Visual Studio Build Tools or Visual Studio)
3. CMake 3.9 or greater
4. Cython 3.0 or greater

### Build Process

On Windows, uvloop uses CMake to build the bundled libuv library:

1. Clone the repository with submodules:
   ```
   git clone --recursive https://github.com/MagicStack/uvloop.git
   cd uvloop
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv uvloop-dev
   uvloop-dev\Scripts\activate
   ```

3. Install development dependencies:
   ```
   pip install -e .[dev]
   ```

4. Build the extension:
   ```
   Makefile.bat compile
   ```

### Platform-Specific Notes

#### Limitations

- Unix domain sockets are not supported on Windows (they will raise NotImplementedError)
- Some low-level system calls may behave differently on Windows

#### Libraries

On Windows, uvloop links against the following system libraries that libuv requires:
- psapi
- user32
- advapi32
- iphlpapi
- userenv
- ws2_32
- dbghelp
- ole32
- shell32

## Testing

Run the Windows-specific tests with:
```
python test_windows.py
```

Or run the full test suite:
```
Makefile.bat test
```

## Known Issues

1. Some tests may fail on Windows due to platform differences
2. Unix domain socket tests are skipped on Windows
3. File system event tests may behave differently on Windows

## Troubleshooting

If you encounter build issues:

1. Make sure you have all prerequisites installed
2. Ensure CMake is in your PATH
3. Check that you're using a compatible version of Visual Studio
4. Clean previous builds with `Makefile.bat clean`

## Contributing

If you encounter any Windows-specific issues, please report them on the GitHub issue tracker with the `windows` label.