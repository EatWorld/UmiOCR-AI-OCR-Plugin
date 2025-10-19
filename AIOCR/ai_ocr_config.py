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
    },
    "zhipu": {
        "api_base": "https://open.bigmodel.cn/api/paas/v4",
        "model": "",  # 用户自定义
    },
    "alibaba": {
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "",  # 用户自定义
    },
    "ollama": {
        "api_base": "http://localhost:11434/api",
        "model": "",  # 用户自定义
    },
    "groq": {
        "api_base": "https://api.groq.com/openai/v1",
        "model": "",  # 用户自定义
    },
    "infinigence": {  # 无问芯穷
        "api_base": "https://cloud.infini-ai.com/maas/v1",
        "model": "",
    },
    "mistral": {
        "api_base": "https://api.mistral.ai/v1",
        "model": "",
    },
    # 新增：魔搭配置
    "modelscope": {
        "api_base": "https://api-inference.modelscope.cn/v1",
        "model": "",  # 用户自定义
    },
    "intern": {  # 浦源书生
        "api_base": "https://chat.intern-ai.org.cn/api/v1",
        "model": "",
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

# 全局配置项 - 新的配置结构，为每个服务商单独设置API密钥和模型

globalOptions = {
    "title": tr("AI OCR 设置"),
    "type": "group",

    # 使用 a_ 前缀确保基础设置排在最前面
    "a_provider": {
        "title": tr("当前AI服务商"),
        "default": "openai",
        "optionsList": [
            ["openai", "OpenAI"],
            ["gemini", "Google Gemini"],
            ["xai", "xAI Grok"],
            ["openrouter", "OpenRouter"],
            ["siliconflow", "硅基流动 (SiliconFlow)"],
            ["doubao", "豆包 (Doubao)"],
            ["alibaba", "阿里云百炼 (Alibaba)"],
            ["zhipu", "智谱AI (Z.AI)"],
            ["ollama", "Ollama (本地)"],
            ["groq", "Groq"],
            ["infinigence", "无问芯穷 (Infinigence)"],
            ["mistral", "Mistral AI"],
            ["modelscope", "魔搭 (ModelScope)"],  # 新增：魔搭选项
            ["intern", "浦源书生 (Intern)"],

        ],
        "toolTip": tr("选择当前要使用的AI服务商。所有服务商的配置都会保存，切换时无需重新输入。"),
    },
    "a_timeout": {
        "title": tr("请求超时"),
        "default": 30,
        "min": 5,
        "max": 120,
        "unit": tr("秒"),
        "isInt": True,
        "toolTip": tr("API请求的超时时间。"),
    },

    # 阿里云百炼配置
    "alibaba_api_key": {
        "title": tr("阿里云百炼 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入阿里云百炼的API密钥"),
    },
    "alibaba_model": {
        "title": tr("阿里云百炼 模型"),
        "default": "qwen-vl-plus-2025-08-15",
        "type": "text",
        "toolTip": tr("阿里云百炼模型名称，如：qwen-vl-plus-2025-08-15"),
    },

    # 豆包配置
    "doubao_api_key": {
        "title": tr("豆包 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入豆包的API密钥"),
    },
    "doubao_model": {
        "title": tr("豆包 模型"),
        "default": "Doubao-1.5-vision-pro-32k",
        "type": "text",
        "toolTip": tr("豆包模型名称，如：Doubao-1.5-vision-pro-32k"),
    },

    # Google Gemini配置
    "gemini_api_key": {
        "title": tr("Gemini API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入Google Gemini的API密钥"),
    },
    "gemini_model": {
        "title": tr("Gemini 模型"),
        "default": "gemini-2.5-flash",
        "type": "text",
        "toolTip": tr("Gemini模型名称，如：gemini-2.5-flash, gemini-1.5-pro"),
    },

    # OpenAI配置
    "openai_api_key": {
        "title": tr("OpenAI API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入OpenAI的API密钥"),
    },
    "openai_model": {
        "title": tr("OpenAI 模型"),
        "default": "gpt-5-mini",
        "type": "text",
        "toolTip": tr("OpenAI模型名称，如：gpt-5-mini, gpt-4o"),
    },

    # OpenRouter配置
    "openrouter_api_key": {
        "title": tr("OpenRouter API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入OpenRouter的API密钥"),
    },
    "openrouter_model": {
        "title": tr("OpenRouter 模型"),
        "default": "anthropic/claude-3.5-sonnet",
        "type": "text",
        "toolTip": tr("OpenRouter模型名称，如：anthropic/claude-3.5-sonnet, google/gemini-pro-vision"),
    },

    # 硅基流动配置
    "siliconflow_api_key": {
        "title": tr("硅基流动 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入硅基流动的API密钥"),
    },
    "siliconflow_model": {
        "title": tr("硅基流动 模型"),
        "default": "Qwen/Qwen2.5-VL-32B-Instruct",
        "type": "text",
        "toolTip": tr("硅基流动模型名称，如：Qwen/Qwen2.5-VL-32B-Instruct, Qwen/Qwen2.5-VL-72B-Instruct"),
    },

    # xAI配置
    "xai_api_key": {
        "title": tr("xAI API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入xAI的API密钥"),
    },
    "xai_model": {
        "title": tr("xAI 模型"),
        "default": "grok-4",
        "type": "text",
        "toolTip": tr("xAI模型名称，如：grok-4"),
    },

    # 智谱AI配置
    "zhipu_api_key": {
        "title": tr("智谱AI API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入智谱AI的API密钥"),
    },
    "zhipu_model": {
        "title": tr("智谱AI 模型"),
        "default": "glm-4v-flash",
        "type": "text",
        "toolTip": tr("智谱AI模型名称，如：glm-4v-flash, glm-4v"),
    },

    # Ollama配置（本地）
    "ollama_api_key": {
        "title": tr("Ollama API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("可留空。用于兼容一些需要密钥的本地服务设置。"),
    },
    "ollama_model": {
        "title": tr("Ollama 模型"),
        "default": "llava:latest",
        "type": "text",
        "toolTip": tr("Ollama本地视觉模型，如：llava:latest"),
    },

    # LM Studio配置（本地）
    "lmstudio_api_key": {
        "title": tr("LM Studio API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("可留空。用于兼容一些需要密钥的本地服务设置。"),
    },
    "lmstudio_model": {
        "title": tr("LM Studio 模型"),
        "default": "llava:latest",
        "type": "text",
        "toolTip": tr("LM Studio本地视觉模型，如：llava:latest"),
    },

    # Groq配置
    "groq_api_key": {
        "title": tr("Groq API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入Groq的API密钥"),
    },
    "groq_model": {
        "title": tr("Groq 模型"),
        "default": "meta-llama/llama-4-scout-17b-16e-instruct",
        "type": "text",
        "toolTip": tr("Groq视觉模型名称，如：meta-llama/llama-4-scout-17b-16e-instruct"),
    },

    # 无问芯穷配置
    "infinigence_api_key": {
        "title": tr("无问芯穷 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入无问芯穷的API密钥"),
    },
    "infinigence_model": {
        "title": tr("无问芯穷 模型"),
        "default": "MiniCPM-V-2.6",
        "type": "text",
        "toolTip": tr("无问芯穷视觉模型名称，如：MiniCPM-V-2.6"),
    },

    # Mistral配置
    "mistral_api_key": {
        "title": tr("Mistral API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入Mistral的API密钥"),
    },
    "mistral_model": {
        "title": tr("Mistral 模型"),
        "default": "pixtral-12b-2409",
        "type": "text",
        "toolTip": tr("Mistral视觉模型名称，如：pixtral-12b-2409, mistral-large-latest"),
    },

    # 新增：魔搭配置
    "modelscope_api_key": {
        "title": tr("魔搭 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入魔搭的访问令牌 (Access Token)"),
    },
    "modelscope_model": {
        "title": tr("魔搭 模型"),
        "default": "Qwen/Qwen-VL-Plus",
        "type": "text",
        "toolTip": tr("魔搭模型ID，如：Qwen/Qwen-VL-Plus, Qwen/QVQ-72B-Preview"),
    },
    # 新增：浦源书生配置
    "intern_api_key": {
        "title": tr("浦源书生 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入浦源书生的API密钥"),
    },
    "intern_model": {
        "title": tr("浦源书生 模型"),
        "default": "internvl3.5-241b-a28b",
        "type": "text",
        "toolTip": tr("浦源书生多模态模型，如：internvl3.5-241b-a28b"),
    },

    # 使用 z_ 前缀确保高级设置排在最后
    "z_proxy_url": {
        "title": tr("代理URL"),
        "default": "",
        "type": "text",
        "toolTip": tr("可选。格式：http://proxy:port 或 socks5://proxy:port"),
        "advanced": True,
    },
    "z_max_concurrent": {
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
        "toolTip": tr("当需要重编码时，选择JPEG质量等级。"),
    },
    
    "max_image_size": {
        "title": tr("最大图像边长"),
        "default": 1536,
        "min": 256,
        "max": 4096,
        "unit": "px",
        "isInt": True,
        "toolTip": tr("超过该边长将缩放图片以适配模型输入。"),
    },

    # 新增：检测-识别双通道开关
    "enable_dual_channel": {
        "title": tr("启用检测-识别双通道"),
        "default": False,
        "type": "boolean",
        "toolTip": tr("先用本地PaddleOCR检测获得真实坐标，再用所选AI模型识别文本。对齐显著更精准。"),
    },
    # 新增：双通道性能优化选项
    "dual_max_boxes": {
        "title": tr("双通道最大识别框数"),
        "default": 30,
        "min": 1,
        "max": 200,
        "unit": tr("个"),
        "isInt": True,
        "toolTip": tr("限制需要送到AI识别的裁剪框数量，超过将截断。"),
    },
    "dual_min_area": {
        "title": tr("双通道最小框面积"),
        "default": 0,
        "min": 0,
        "max": 50000,
        "unit": "px^2",
        "isInt": True,
        "toolTip": tr("过滤过小的检测框以提升速度，单位为像素面积。"),
    },
    "dual_max_workers": {
        "title": tr("双通道并发识别数"),
        "default": 3,
        "min": 1,
        "max": 10,
        "unit": tr("个"),
        "isInt": True,
        "toolTip": tr("并发向AI发送裁剪识别请求，提升总体速度。"),
    },
    "dual_local_score_threshold": {
        "title": tr("本地高置信度直接采用"),
        "default": 0.92,
        "min": 0.0,
        "max": 1.0,
        "toolTip": tr("当Paddle本地识别置信度高于该阈值时直接采用，跳过AI识别。"),
    },
    "dual_crop_padding": {
        "title": tr("裁剪边缘补白"),
        "default": 2,
        "min": 0,
        "max": 20,
        "unit": "px",
        "isInt": True,
        "toolTip": tr("对检测框四周增加少量像素，避免裁剪过紧影响识别。"),
    },
}
