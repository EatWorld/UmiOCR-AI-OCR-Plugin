@echo off
rem ============================================================
rem  AI OCR 插件 - 刷新各平台模型列表（离线拉取）
rem  通过各平台 API 在线获取模型列表，写入 model_lists_cache.json。
rem  拉取完成后请重启 Umi-OCR，全局设置的"模型"下拉菜单即会更新。
rem  （若 Umi-OCR 全局设置中已有"获取模型列表"按钮，可直接在软件内拉取，无需本脚本）
rem ============================================================
chcp 65001 >nul
cd /d "%~dp0"

set "PY=..\..\runtime\python.exe"
if not exist "%PY%" (
    echo 未找到 Umi-OCR 自带 Python（..\..\runtime\python.exe），尝试使用系统 Python...
    set "PY=python"
)

echo 正在拉取各平台模型列表，请稍候...
"%PY%" model_lists.py %*
echo.
pause
