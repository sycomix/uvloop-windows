@echo off
REM Windows build script for uvloop

setlocal

REM Check if we're running in the right directory
if not exist "setup.py" (
    echo Error: setup.py not found. Please run this script from the uvloop root directory.
    exit /b 1
)

REM Parse command line arguments
if "%1" == "" goto help
if "%1" == "help" goto help
if "%1" == "clean" goto clean
if "%1" == "compile" goto compile
if "%1" == "debug" goto debug
if "%1" == "test" goto test

echo Unknown command: %1
goto help

:help
echo Usage: Makefile.bat [clean^|compile^|debug^|test]
echo.
echo Commands:
echo   clean    - Clean build artifacts
echo   compile  - Build the extension
echo   debug    - Build with debug symbols
echo   test     - Run tests
exit /b 0

:clean
echo Cleaning build artifacts...
del /q "dist\*" 2>nul
del /q "uvloop\loop.*.pyd" 2>nul
del /q "uvloop\loop_d.*.pyd" 2>nul
del /q "uvloop\*.c" 2>nul
del /q "uvloop\*.html" 2>nul
del /q "uvloop\*.so" 2>nul
for /d %%i in ("uvloop\handles\*") do (
    if exist "%%i\*.html" del /q "%%i\*.html"
)
for /d %%i in ("uvloop\includes\*") do (
    if exist "%%i\*.html" del /q "%%i\*.html"
)
for /d %%i in ("build\*") do (
    if exist "%%i" rd /s /q "%%i"
)
echo Done.
exit /b 0

:compile
echo Building uvloop...
python setup.py build_ext --inplace --cython-always
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)
echo Build completed successfully.
exit /b 0

:debug
echo Building uvloop with debug symbols...
python setup.py build_ext --inplace --debug --cython-always --cython-annotate --cython-directives="linetrace=True" --define UVLOOP_DEBUG,CYTHON_TRACE,CYTHON_TRACE_NOGIL
if errorlevel 1 (
    echo Debug build failed.
    exit /b 1
)
echo Debug build completed successfully.
exit /b 0

:test
echo Running tests...
set PYTHONASYNCIODEBUG=1
python -m unittest discover -v tests
if errorlevel 1 (
    echo Tests failed.
    exit /b 1
)
python -m unittest discover -v tests
if errorlevel 1 (
    echo Tests failed.
    exit /b 1
)
echo All tests passed.
exit /b 0