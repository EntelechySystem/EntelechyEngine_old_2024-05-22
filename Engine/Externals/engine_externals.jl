## 导入包
using Logging
using StaticArrays
using SparseArrays
using DataFrames
using InteractiveDynamics
using CSV
# using GLMakie
# GLMakie.activate!()
# using CairoMakie
# CairoMakie.activate!()
using Colors
# using HDF5
using Random
using Agents
using FileIO
using Dates
# using Distances
using LinearAlgebra

## 临时修改默认的环境变量
ENV["JULIA_CONDAPKG_BACKEND"] = "Null"
ENV["JULIA_PYTHONCALL_EXE"] = "venv/bin/python"
# ENV["PYTHON"] = "venv/bin/python"

using PythonCall