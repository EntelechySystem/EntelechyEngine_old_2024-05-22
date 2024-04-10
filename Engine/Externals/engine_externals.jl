function get_conda_env_path(env_name)  #HACK 这个似乎无用
    cmd = `conda info --envs`
    result = String(run(cmd, stdout=Base.Pipe))
    lines = split(result, '\n')
    for line in lines[2:end-1]
        parts = split(line)
        if length(parts) >= 2 && parts[1] == env_name
            return parts[2]
        end
    end
    return ""
end



## 添加自定义的路径环境变量
ENV["ENGINE_PATH"] = abspath(joinpath(@__DIR__, "../../", "Engine"))

## 临时修改默认的环境变量
ENV["JULIA_NUM_THREADS"] = 1


## 导入包
using Logging
import Logging: AbstractLogger, LogLevel, LogRecord
using StaticArrays
using SparseArrays
using DataFrames
using CSV
using GLMakie
GLMakie.activate!()
# using CairoMakie
# CairoMakie.activate!()
using Colors
using Random
using Agents
using FileIO
using Dates
using LinearAlgebra
using CellListMap.PeriodicSystems
using Distributed

if Sys.iswindows()
    println("当前操作系统是Windows")
    # 在Windows上执行特定的操作
    ENV["JULIA_PYTHONCALL_EXE"] = joinpath(homedir(), "anaconda3", "envs", conda_virtual_environment, "python.exe")  # `conda_virtual_environment` 之默认值是 "Engine"
    ENV["JULIA_CONDAPKG_BACKEND"] = "Current"
elseif Sys.isapple()
    println("当前操作系统是Mac")
    ## 临时修改默认的环境变量
    ENV["JULIA_CONDAPKG_BACKEND"] = "Null"
    ENV["JULIA_PYTHONCALL_EXE"] = "venv/bin/python"
    # ENV["PYTHON"] = "venv/bin/python"
elseif Sys.islinux()
    println("当前操作系统是Linux")
    # 在Linux上执行特定的操作
else
    println("未知操作系统")
    # 在其他操作系统上执行默认操作
end


using PythonCall