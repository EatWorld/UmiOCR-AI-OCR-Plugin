# -*- coding: utf-8 -*-
# AI OCR Plugin for Umi-OCR
# Author: Assistant
# Description: Multi-vendor AI OCR plugin supporting various AI providers

from .ai_ocr import Api
from .ai_ocr_config import globalOptions, localOptions

# 插件信息
PluginInfo = {
    "group": "ocr",  # 插件组别
    "global_options": globalOptions,  # 全局配置项
    "local_options": localOptions,   # 局部配置项
    "api_class": Api,  # API类
}