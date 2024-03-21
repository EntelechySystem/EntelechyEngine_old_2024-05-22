"""
引擎文件
"""

"""
该文件是引擎的入口文件，用于运行引擎的主程序
"""


def engine(config: dict):
    """
    Python 版本引擎入口

    Args:
        config (dict): 配置项

    Returns:
        None

    """

    # global config, para

    # %% 首先导入相关包
    from Engine import os, platform, logging, Path, shutil, datetime, time, subprocess, pickle, base64, deepcopy
    from Engine.Tools.Tools import Tools
    from Engine.Tools.DataManageTools import DataManageTools

    # %% 初始化
    ## 获取项目路径、引擎工具路径
    config['folderpath_project'] = Tools.get_project_rootpath()
    config['folderpath_engine'] = Tools.get_project_rootpath(config['foldername_engine'], config['folderpath_relpath_engine'])

    # # %% 由本引擎复制一份完整的引擎工程文件夹到项目文件夹中使用 ！HACK 这个很危险，容易删除引擎工程文件夹！需要谨慎使用！
    # Tools._delete_and_recreate_folder(Path(config['folderpath_project'], r"Engine"), is_auto_confirmation=config['is_auto_confirmation'])
    # Tools._copy_files_from_other_folders(Path(config['folderpath_engine'], r"Engine"), Path(config['folderpath_project'], r"Engine"), is_auto_confirmation=config['is_auto_confirmation'])

    # %% 读写文件夹：如果 Library 之 Config 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    Tools._delete_and_recreate_folder(Path(config['folderpath_engine'], r"Engine/Library/Config").resolve(), is_auto_confirmation=config['is_auto_confirmation'])
    Tools._copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_engine'], "Engine/Library/Config").resolve(), is_auto_confirmation=config['is_auto_confirmation'])

    # %% 运行配置程序
    Tools.run_python_program_file(Path(config['folderpath_engine'], r"Engine/Library/Config/config.py").resolve(), [Path(config['folderpath_engine'], r"Engine/Library/Config").resolve()])

    ## 读取配置文件为字典
    with open(Path(config['folderpath_engine'], r"Engine/Library/Config/config.pkl").resolve(), 'rb') as f:
        config = pickle.load(f)

    ## config 赋值给全局变量 globals
    globals = dict()
    globals.update(config)

    ## 设置相关的实验文件夹名称
    # if globals['schedule_operation']['实验组模拟程序'] is True:
    # pass  # if
    globals['foldername_experiments'] = Tools.set_foldername_experiments(globals['foldername_prefix_experiments'], globals['foldername_set_manually'], globals['is_datetime'], globals['type_of_experiments_foldername'])

    ## 生成实验相关的文件夹用于本批次运作
    (
        globals['folderpath_project'],
        globals['folderpath_engine'],
        globals['folderpath_experiments'],
        globals['folderpath_experiments_output_data'],
        globals['folderpath_experiments_output_log'],
        globals['folderpath_experiments_output_config'],
        globals['folderpath_experiments_output_settings'],
        globals['folderpath_experiments_output_parameters'],
        globals['folderpath_experiments_output_agents'],
        globals['folderpath_experiments_output_models'],
        globals['folderpath_models'],
        globals['folderpath_config'],
        globals['folderpath_settings'],
        globals['folderpath_parameters'],
        globals['folderpath_agents'],
    ) = Tools.set_experiments_folders(
        foldername_experiments_output_data=globals['foldername_experiments_output_data'],
        foldername_experiments=globals['foldername_experiments'],
        str_folderpath_root_experiments=globals['folderpath_root_experiments'],
        str_foldername_engine=globals['foldername_engine'],
        str_folderpath_relpath_engine=globals['folderpath_relpath_engine'],
        str_foldername_outputData=globals['foldername_outputData'],
        str_folderpath_relpath_outputData=globals['folderpath_relpath_outputData'],
        str_folderpath_models=globals['folderpath_models'],
        str_folderpath_config=globals['folderpath_config'],
        str_folderpath_settings=globals['folderpath_settings'],
        str_folderpath_parameters=globals['folderpath_parameters'],
        str_folderpath_agents=globals['folderpath_agents'],
    )

    ## 如果 Library 之 Settings 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Settings").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])
    Tools._copy_files_from_other_folders(Path(globals['folderpath_project'], globals['folderpath_settings']), Path(globals['folderpath_engine'], "Engine/Library/Settings").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])

    # %% 运行设置程序
    Tools.run_python_program_file(Path(globals['folderpath_engine'], r"Engine/Library/Settings/settings.py").resolve(), [Path(globals['folderpath_engine'], r"Engine/Library/Settings").resolve()])

    ## 读取设置文件为字典
    settings = DataManageTools.load_PKLs_to_DataFrames(Path(globals['folderpath_engine'], r"Engine/Library/Settings"))

    globals.update(settings)  # 将 settings 字典中的内容更新到 globals 字典中

    Tools.flatten_dict(globals, 1)  # 将 globals 字典中的内容扁平化

    ## 导出全局变量 globals 字典为 PKL 文件
    globals_expert = deepcopy(globals)
    Tools.transform_all_Path_value_to_string(globals_expert)  # 转换字典里所有 Path 对象为字符串。
    Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Globals").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])
    with open(Path(globals['folderpath_engine'], r"Engine/Library/Globals/globals.pkl").resolve(), 'wb') as f:
        pickle.dump(globals_expert, f)

    # # 读取刚刚导出的文件 #DEBUG 专用
    # with open(Path(globals['folderpath_engine'], r"Engine/Library/Globals/globals.pkl").resolve(), 'rb') as f:
    #     data = pickle.load(f)

    # from Engine.core.operations.operator import Operator

    # # %% 是否运作模拟程序
    # if globals['schedule_operation']['实验组模拟程序']:
    #     ## 导入相关数据
    #     Tools._copy_files_from_other_folders(globals['folderpath_config'], globals['folderpath_experiments_output_config'], is_auto_confirmation=globals['is_auto_confirmation'])  # 导出一份到输出文件夹
    #
    #     Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Parameters"), is_auto_confirmation=globals['is_auto_confirmation'])
    #     Tools._copy_files_from_other_folders(globals['folderpath_parameters'], Path(globals['folderpath_engine'], r"Engine/Library/Parameters"), is_auto_confirmation=globals['is_auto_confirmation'])
    #     Tools._copy_files_from_other_folders(globals['folderpath_parameters'], globals['folderpath_experiments_output_parameters'], is_auto_confirmation=globals['is_auto_confirmation'])  # 导出一份到输出文件夹
    #     # shutil.copy(Path(globals['folderpath_parameters'], r"set_parameters_variables.py"), globals['folderpath_experiments_output_parameters'])  # 导出一份生成参数的代码文件到输出文件夹
    #     # from Core.define.define_parameterVariables import para
    #
    #     Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Agents"), is_auto_confirmation=globals['is_auto_confirmation'])
    #     Tools._copy_files_from_other_folders(globals['folderpath_agents'], Path(globals['folderpath_engine'], r"Engine/Library/Agents"), is_auto_confirmation=globals['is_auto_confirmation'])
    #     Tools._copy_files_from_other_folders(globals['folderpath_agents'], globals['folderpath_experiments_output_agents'], is_auto_confirmation=globals['is_auto_confirmation'])  # 导出一份到输出文件夹
    #     # from Engine.core.define.define_agentsVariables import dict_agent, dict_interagent
    #
    #     ## 获取一些系统信息
    #     globals['system_platform'] = platform.system()
    #
    #     ## 设置日志
    #     logger = logging.getLogger()
    #     logger.setLevel(globals['test_logging'])
    #     if Path(globals['folderpath_experiments_output_log'], "outputlog.txt").exists():
    #         os.remove(Path(globals['folderpath_experiments_output_log'], "outputlog.txt"))  # 如果原来的日志存在，那么就删除重建
    #         pass  # if
    #     log_file_handler = logging.FileHandler(Path(globals['folderpath_experiments_output_log'], "outputlog.txt"))
    #     logger.addHandler(log_file_handler)
    #     log_console_handler = logging.StreamHandler()
    #     logger.addHandler(log_console_handler)
    #
    #     if globals['is_develope_model']:
    #         logging.info("\n------------ 开发与调试模式！ ---------------\n")
    #         pass  # if
    #
    #     logging.info("\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    #     logging.info("\n实验组名称：" + globals['foldername_experiments'] + "\n")
    #     logging.info("\n引擎 engine 版本：" + globals['engine_version'] + "\n")
    #     logging.info("\n相关实验配置项 globals 文件夹：" + globals['folderpath_config'].name + "\n")
    #     logging.info("\n相关实验 models 文件夹：" + globals['folderpath_models'].name + "\n")
    #     logging.info("\n相关实验 agents 数据文件夹：" + globals['folderpath_agents'].name + "\n")
    #     logging.info("\n相关实验数据 experiments output data 文件夹：" + globals['folderpath_experiments'].name + "\n")
    #     logging.info("\n相关实验参数 parameters 文件夹：" + globals['folderpath_parameters'].name + "\n")
    #
    #     ## 运行实验组模拟程序
    #     from Programs.experiments_program import experiments_program
    #     experiments_program(globals, para)
    #
    #     ## 关闭日志
    #     logger.removeHandler(log_file_handler)
    #     pass  # if
    #
    # # %% 是否可视化结果程序
    # if globals['schedule_operation']['可视化结果程序']:
    #     sgv_pkl = pickle.dumps(globals)
    #     sgv_base64 = base64.b64encode(sgv_pkl).decode('utf-8')
    #     start_time = time.time()
    #     subprocess.run(["python", str(Path(globals['folderpath_engine'], 'Data/programs/visualize_data_program.py')), sgv_base64])
    #     end_time = time.time()
    #     print(f"\n可视化数据运行总时长：{end_time - start_time} 秒。\n")
    #     pass  # if
    #
    # # %% 清理
    # ## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Config"), is_auto_confirmation=globals['is_auto_confirmation'])
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Parameters"), is_auto_confirmation=globals['is_auto_confirmation'])
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Agents"), is_auto_confirmation=globals['is_auto_confirmation'])
    # if not globals['is_develope_model']:
    #     Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/Library/Models"), is_auto_confirmation=globals['is_auto_confirmation'])
    #     pass  # if

