###工具说明
本工具用于检测ELF格式文件(动态、静态库等)中全局变量信息；
注意：不支持windows平台静态、动态库（非ELF格式文件）。


###使用方法
运行平台：linux
命令行： GlobalVarCheck argv[1]
argv[1]: 待检测库文件


###输出
当前目录下生成global_var_check.log，追加方式写入。
