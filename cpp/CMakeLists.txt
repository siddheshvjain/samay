cmake_minimum_required(VERSION 3.12)
project(samay_cpp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

# Source files
set(SOURCES
    src/backtest_engine.cpp
    src/bindings.cpp
)

# Create Python module
pybind11_add_module(samay_backtest_cpp ${SOURCES})

# Optimization flags for production
if(MSVC)
    target_compile_options(samay_backtest_cpp PRIVATE /O2 /arch:AVX2)
else()
    target_compile_options(samay_backtest_cpp PRIVATE -O3 -march=native -ffast-math)
endif()

# Link math library
target_link_libraries(samay_backtest_cpp PRIVATE m)
