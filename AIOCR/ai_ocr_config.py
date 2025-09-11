#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AI OCR Plugin Configuration

from plugin_i18n import Translator

tr = Translator(__file__, "i18n.csv")

# 服务商配置映射
PROVIDER_CONFIGS = {
    "openai": {
        "api_base": "https://api.openai.com/v1",
        "model": "",  # 用户自定义
    },
    "gemini": {
        "api_base": "https://generativelanguage.googleapis.com/v1beta",
        "model": "",  # 用户自定义
    },
    "xai": {
        "api_base": "https://api.x.ai/v1",
        "model": "",  # 用户自定义
    },
    "openrouter": {
        "api_base": "https://openrouter.ai/api/v1",
        "model": "",  # 用户自定义
    },
    "siliconflow": {
        "api_base": "https://api.siliconflow.cn/v1",
        "model": "",  # 用户自定义
    },

    "doubao": {
        "api_base": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "",  # 用户自定义

    "Z.AI": {
        "api_base": "https://open.bigmodel.cn/api/paas/v4",
        "model": "",  # 用户自定义
    },

    "Qwen": {
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "",  # 用户自定义
    },
}

# 获取服务商默认配置的辅助函数
def get_provider_default_api_base(provider):
    """获取指定服务商的默认API基础URL"""
    return PROVIDER_CONFIGS.get(provider, {}).get("api_base", "")

def get_provider_default_model(provider):
    """获取指定服务商的默认模型（现在返回空字符串，让用户自己填写）"""
    return ""

def update_provider_config(provider):
    """当服务商切换时，更新相关配置项的默认值"""
    try:
        # 获取新服务商的默认配置
        default_api_base = get_provider_default_api_base(provider)
        default_model = get_provider_default_model(provider)
        
        # 这里需要通过Umi-OCR的配置系统来更新其他配置项
        # 由于QML配置系统的限制，我们通过返回值来提示用户
        import sys
        if hasattr(sys.modules.get('__main__'), 'qmlapp'):
            qmlapp = sys.modules['__main__'].qmlapp
            if hasattr(qmlapp, 'popup'):
                message = f"已切换到 {provider}\n\n建议配置：\nAPI基础URL: {default_api_base}\n模型: {default_model}"
                qmlapp.popup.simple("服务商已切换", message)
        
        return None  # 不阻止配置变更
    except Exception as e:
        print(f"更新服务商配置时出错: {e}")
        return None

# 全局配置项
# 存储每个服务商的配置状态
_provider_configs = {
    "openai": {"model": "", "api_key": ""},
    "gemini": {"model": "", "api_key": ""},
    "xai": {"model": "", "api_key": ""},
    "openrouter": {"model": "", "api_key": ""},
    "siliconflow": {"model": "", "api_key": ""},
    "doubao": {"model": "", "api_key": ""},
    "Qwen": {"model": "", "api_key": ""},
    "Z.AI": {"model": "", "api_key": ""},
}

def switch_provider_config(new_provider, old_provider, configs):
    """切换服务商时保存当前配置并加载新配置"""
    try:
        # 保存当前服务商的配置
        if old_provider and old_provider in _provider_configs:
            _provider_configs[old_provider]["model"] = configs.get("model", "")
            _provider_configs[old_provider]["api_key"] = configs.get("api_key", "")
        
        # 加载新服务商的配置
        if new_provider in _provider_configs:
            return {
                "model": _provider_configs[new_provider]["model"],
                "api_key": _provider_configs[new_provider]["api_key"]
            }
    except Exception as e:
        print(f"切换服务商配置时出错: {e}")
    
    return None

globalOptions = {
    "title": tr("AI OCR 设置"),
    "type": "group",
    
    "provider": {
        "title": tr("AI 服务商"),
        "default": "openai",
        "optionsList": [
            ["openai", "OpenAI"],
            ["gemini", "Google Gemini"],
            ["xai", "xAI Grok"],
            ["openrouter", "OpenRouter (Claude)"],
            ["siliconflow", "硅基流动 (SiliconFlow)"],
            ["doubao", "豆包 (Doubao)"],
            ["Qwen", "千问 (Qwen)"],
            ["Z.AI", "智谱 (Z.AI)"],
        ],
        ],
        "toolTip": tr("选择要使用的AI服务提供商。切换时会自动保存和恢复对应的配置。"),
    },
    
    "model": {
        "title": tr("模型"),
        "default": "",
        "type": "text",
        "toolTip": tr("输入要使用的模型名称。请根据所选服务商填写对应的模型名称。"),
    },
    
    "api_key": {
        "title": tr("API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入对应服务商的API密钥。"),
    },
    
    "max_retries": {
        "title": tr("最大重试次数"),
        "default": 3,
        "min": 0,
        "max": 10,
        "unit": tr("次"),
        "isInt": True,
        "toolTip": tr("请求失败时的最大重试次数。"),
    },
    
    "timeout": {
        "title": tr("请求超时"),
        "default": 30,
        "min": 5,
        "max": 120,
        "unit": tr("秒"),
        "isInt": True,
        "toolTip": tr("API请求的超时时间。"),
    },
    
    "proxy_url": {
        "title": tr("代理URL"),
        "default": "",
        "type": "text",
        "toolTip": tr("可选。格式：http://proxy:port 或 socks5://proxy:port"),
        "advanced": True,
    },
    
    "max_concurrent": {
        "title": tr("最大并发数"),
        "default": 3,
        "min": 1,
        "max": 10,
        "unit": tr("个"),
        "isInt": True,
        "toolTip": tr("批量处理时的最大并发请求数。"),
        "advanced": True,
    },
}

# 局部配置项
localOptions = {
    "title": tr("文字识别（AI OCR）"),
    "type": "group",
    
    "language": {
        "title": tr("识别语言"),
        "default": "auto",
        "optionsList": [
            ["auto", tr("自动检测")],
            ["zh", tr("中文")],
            ["en", tr("英文")],
            ["ja", tr("日文")],
            ["ko", tr("韩文")],
            ["fr", tr("法文")],
            ["de", tr("德文")],
            ["es", tr("西班牙文")],
            ["ru", tr("俄文")],
            ["ar", tr("阿拉伯文")],
        ],
        "toolTip": tr("指定要识别的文字语言。自动检测适用于大多数情况。"),
    },
    
    "output_format": {
        "title": tr("输出格式"),
        "default": "text_only",
        "optionsList": [
            ["text_only", tr("仅文字")],
            ["with_coordinates", tr("文字+坐标")],
        ],
        "toolTip": tr("选择OCR结果的输出格式。坐标信息可用于定位文字位置。"),
    },
    
    "image_quality": {
        "title": tr("图像质量"),
        "default": "auto",
        "optionsList": [
            ["auto", tr("自动")],
            ["high", tr("高质量")],
            ["medium", tr("中等质量")],
            ["low", tr("低质量")],
        ],
        "toolTip": tr("图像压缩质量。高质量可能提高识别精度但增加传输时间。"),
    },
    
    "max_image_size": {
        "title": tr("最大图像尺寸"),
        "default": 1536,
        "optionsList": [
            [2048, "2048px"],
            [1536, "1536px " + tr("（推荐）")],
            [1024, "1024px"],
            [512, "512px"],
        ],
        "toolTip": tr("图像的最大边长。过大的图像会被压缩以节省API调用成本。"),
    },
}
