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
    "glm_ocr": {
        "api_base": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-ocr",
    },
    "alibaba": {
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-vl-plus",
    },
    "ollama": {
        "api_base": "http://localhost:11434/api",
        "model": "",  # 用户自定义
    },
    "lmstudio": {
        "api_base": "http://localhost:1234/v1",
        "model": "",  # 用户自定义
    },
    "llamacpp": {
        "api_base": "http://localhost:8080/v1",
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
        "model": "",
    },
    "mimo": {
        "api_base": "https://api.xiaomimimo.com/v1",
        "model": "mimo-v2.5",
    },
    "intern": {  # 浦源书生
        "api_base": "https://chat.intern-ai.org.cn/api/v1",
        "model": "",
    },
    "kimi": {
        "api_base": "https://api.moonshot.cn/v1",
        "model": "kimi-k2.6",
    },
    "nvidia_nim": {
        "api_base": "https://integrate.api.nvidia.com/v1",
        "model": "moonshotai/kimi-k2.6",
    },
    "paddle": {
        "api_base": "https://paddleocr.aistudio-app.com",
        "model": "PP-OCRv6",
    },
    "paddle_vl_16": {
        "api_base": "https://paddleocr.aistudio-app.com",
        "model": "PaddleOCR-VL-1.6",
    },
    "pp_structure_v3": {
        "api_base": "https://paddleocr.aistudio-app.com",
        "model": "PP-StructureV3",
    },
    "mineru": {
        "api_base": "https://mineru.net/api/v4",
        "model": "vlm",
    },
    "longcat": {
        "api_base": "https://api.longcat.chat/openai/v1",
        "model": "LongCat-Flash-Chat",
    },
}

# 获取服务商默认配置的辅助函数
def get_provider_default_api_base(provider):
    """获取指定服务商的默认API基础URL"""
    return PROVIDER_CONFIGS.get(provider, {}).get("api_base", "")

def get_provider_default_model(provider):
    """获取指定服务商的默认模型"""
    cfg = PROVIDER_CONFIGS.get(provider, {})
    model = cfg.get("model", "")
    if model:
        return model
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

    "a_prompt_text_only": {
        "title": tr("纯文字识别 Prompt"),
        "default": "识别图片中的文字，语言：{language}。保持原有格式，直接返回文字内容。",
        "type": "text",
        "toolTip": tr("纯文字识别模式的提示词模板，{language}会被替换为当前识别语言。留空则使用默认模板。"),
    },
    "a_prompt_with_coordinates": {
        "title": tr("含坐标识别 Prompt"),
        "default": '识别图片文字并返回坐标，语言：{language}\n输出JSON格式：{{"texts": [{{"text": "文字内容", "box": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]}}]}}\n坐标为像素位置，左上角为原点。直接返回JSON，无其他内容。',
        "type": "text",
        "toolTip": tr("含坐标识别模式的提示词模板，{language}会被替换为当前识别语言。留空则使用默认模板。"),
    },
    "a_prompt_markdown": {
        "title": tr("Markdown识别 Prompt"),
        "default": "识别图片中的文字，语言：{language}。以Markdown格式输出，保留标题、列表、表格、加粗、斜体等结构。直接返回Markdown内容，无其他说明。",
        "type": "text",
        "toolTip": tr("Markdown识别模式的提示词模板，{language}会被替换为当前识别语言。留空则使用默认模板。"),
    },

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
            ["glm_ocr", "GLM-OCR"],
            ["ollama", "Ollama (本地)"],
            ["lmstudio", "LM Studio (本地)"],
            ["llamacpp", "llama.cpp (本地)"],
            ["groq", "Groq"],
            ["infinigence", "无问芯穷 (Infinigence)"],
            ["mistral", "Mistral AI"],
            ["modelscope", "魔搭 (ModelScope)"],
            ["mimo", "小米MiMo"],
            ["intern", "浦源书生 (Intern)"],
            ["kimi", "Kimi (月之暗面)"],
            ["nvidia_nim", "NVIDIA NIM"],
            ["mineru", "MinerU"],
            ["paddle", "PaddleOCR (在线)"],
            ["paddle_vl_16", "PaddleOCR-VL-1.6 (在线)"],
            ["pp_structure_v3", "PP-StructureV3 (在线)"],
            ["longcat", "Longcat AI"],

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
        "default": "qwen-vl-plus",
        "type": "text",
        "toolTip": tr("阿里云百炼模型名称，如：qwen-vl-plus, qwen-vl-max, qwen-vl-ocr"),
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
    "glm_ocr_api_key": {
        "title": tr("GLM-OCR API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入GLM-OCR的API密钥"),
    },
    "glm_ocr_model": {
        "title": tr("GLM-OCR 模型"),
        "default": "glm-ocr",
        "type": "text",
        "toolTip": tr("GLM-OCR模型名称，如：glm-ocr"),
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
    "ollama_api_base": {
        "title": tr("Ollama API地址"),
        "default": "http://localhost:11434/api",
        "type": "text",
        "toolTip": tr("Ollama本地服务的API地址，默认为 http://localhost:11434/api"),
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
    "lmstudio_api_base": {
        "title": tr("LM Studio API地址"),
        "default": "http://localhost:1234/v1",
        "type": "text",
        "toolTip": tr("LM Studio本地服务的API地址，默认为 http://localhost:1234/v1"),
    },

    # llama.cpp配置（本地）
    "llamacpp_api_key": {
        "title": tr("llama.cpp API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("可留空。如启动llama.cpp服务时设置了 --api-key，请在此填写对应密钥。"),
    },
    "llamacpp_model": {
        "title": tr("llama.cpp 模型"),
        "default": "",
        "type": "text",
        "toolTip": tr("llama.cpp加载的模型名称，可通过 /v1/models 端点查询。"),
    },
    "llamacpp_api_base": {
        "title": tr("llama.cpp API地址"),
        "default": "http://localhost:8080/v1",
        "type": "text",
        "toolTip": tr("llama.cpp本地服务的API地址，默认为 http://localhost:8080/v1"),
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
    # 小米MiMo配置
    "mimo_api_key": {
        "title": tr("小米MiMo API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入小米MiMo平台的API密钥"),
    },
    "mimo_model": {
        "title": tr("小米MiMo 模型"),
        "default": "mimo-v2.5",
        "type": "text",
        "toolTip": tr("MiMo视觉模型名称，如：mimo-v2.5, mimo-v2-omni"),
    },
    "mimo_api_base": {
        "title": tr("小米MiMo API地址"),
        "default": "https://api.xiaomimimo.com/v1",
        "type": "text",
        "toolTip": tr("小米MiMo平台的API地址。默认：https://api.xiaomimimo.com/v1 ；如购买了Code套餐，请使用专属地址：https://token-plan-cn.xiaomimimo.com/v1"),
    },
    # 浦源书生配置
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
    # Kimi (月之暗面) 配置
    "kimi_api_key": {
        "title": tr("Kimi API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入Kimi平台的API Key（从 https://platform.moonshot.cn 获取）"),
    },
    "kimi_model": {
        "title": tr("Kimi 模型"),
        "default": "kimi-k2.6",
        "type": "text",
        "toolTip": tr("Kimi视觉模型名称，如：kimi-k2.6, kimi-k2.5, moonshot-v1-128k-vision-preview"),
    },
    "kimi_api_base": {
        "title": tr("Kimi API地址"),
        "default": "https://api.moonshot.cn/v1",
        "type": "text",
        "toolTip": tr("Kimi平台的API地址，默认：https://api.moonshot.cn/v1"),
        "advanced": True,
    },
    # NVIDIA NIM 配置
    "nvidia_nim_api_key": {
        "title": tr("NVIDIA NIM API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入NVIDIA NIM的API Key（从 https://build.nvidia.com 获取）"),
    },
    "nvidia_nim_model": {
        "title": tr("NVIDIA NIM 模型"),
        "default": "moonshotai/kimi-k2.6",
        "type": "text",
        "toolTip": tr("NVIDIA NIM模型名称，如：moonshotai/kimi-k2.6"),
    },
    "nvidia_nim_api_base": {
        "title": tr("NVIDIA NIM API地址"),
        "default": "https://integrate.api.nvidia.com/v1",
        "type": "text",
        "toolTip": tr("NVIDIA NIM的API地址，默认：https://integrate.api.nvidia.com/v1"),
        "advanced": True,
    },

    "mineru_api_key": {
        "title": tr("MinerU API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入MinerU平台的API Token（请求头 Authorization: Bearer <token>）"),
    },
    "mineru_model": {
        "title": tr("MinerU 模型版本"),
        "default": "vlm",
        "type": "text",
        "toolTip": tr("MinerU 的 model_version，如：vlm、pipeline、MinerU-HTML"),
    },
    "mineru_user_token": {
        "title": tr("MinerU 用户标识 (可选)"),
        "default": "",
        "type": "text",
        "toolTip": tr("部分 PRO 接口要求请求头额外携带 token 字段，用于额度管理"),
        "advanced": True,
    },

    # Longcat AI配置
    "longcat_api_key": {
        "title": tr("Longcat AI API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入Longcat AI平台的API Key（从 https://longcat.chat/platform/api_keys 获取）"),
    },
    "longcat_model": {
        "title": tr("Longcat AI 模型"),
        "default": "LongCat-Flash-Chat",
        "type": "text",
        "toolTip": tr("Longcat AI模型名称，如：LongCat-Flash-Chat, LongCat-Flash-Thinking, LongCat-Flash-Lite"),
    },
    "longcat_api_base": {
        "title": tr("Longcat AI API地址"),
        "default": "https://api.longcat.chat/openai/v1",
        "type": "text",
        "toolTip": tr("Longcat AI的API地址，默认：https://api.longcat.chat/openai/v1"),
        "advanced": True,
    },

    # PaddleOCR 在线配置（异步解析模式）
    "paddle_api_key": {
        "title": tr("PaddleOCR Token"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入AI Studio的Access Token（从 https://aistudio.baidu.com/account/accessToken 获取）"),
    },
    "paddle_model": {
        "title": tr("PaddleOCR 模型"),
        "default": "PP-OCRv6",
        "type": "text",
        "toolTip": tr("PaddleOCR模型名称，如：PP-OCRv6"),
        "advanced": True,
    },
    "paddle_api_base": {
        "title": tr("PaddleOCR API地址"),
        "default": "https://paddleocr.aistudio-app.com",
        "type": "text",
        "toolTip": tr("PaddleOCR异步API基础地址，默认：https://paddleocr.aistudio-app.com"),
        "advanced": True,
    },
    # PaddleOCR-VL-1.6 在线配置（异步解析模式）
    "paddle_vl_16_api_key": {
        "title": tr("PaddleOCR-VL-1.6 Token"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入AI Studio的Access Token（从 https://aistudio.baidu.com/account/accessToken 获取）"),
    },
    "paddle_vl_16_model": {
        "title": tr("PaddleOCR-VL-1.6 模型"),
        "default": "PaddleOCR-VL-1.6",
        "type": "text",
        "toolTip": tr("PaddleOCR-VL-1.6模型名称，如：PaddleOCR-VL-1.6"),
        "advanced": True,
    },
    "paddle_vl_16_api_base": {
        "title": tr("PaddleOCR-VL-1.6 API地址"),
        "default": "https://paddleocr.aistudio-app.com",
        "type": "text",
        "toolTip": tr("PaddleOCR-VL-1.6异步API基础地址，默认：https://paddleocr.aistudio-app.com"),
        "advanced": True,
    },
    # PP-StructureV3 在线配置（异步解析模式）
    "pp_structure_v3_api_key": {
        "title": tr("PP-StructureV3 Token"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入AI Studio的Access Token（从 https://aistudio.baidu.com/account/accessToken 获取）"),
    },
    "pp_structure_v3_model": {
        "title": tr("PP-StructureV3 模型"),
        "default": "PP-StructureV3",
        "type": "text",
        "toolTip": tr("PP-StructureV3模型名称，如：PP-StructureV3"),
        "advanced": True,
    },
    "pp_structure_v3_api_base": {
        "title": tr("PP-StructureV3 API地址"),
        "default": "https://paddleocr.aistudio-app.com",
        "type": "text",
        "toolTip": tr("PP-StructureV3异步API基础地址，默认：https://paddleocr.aistudio-app.com"),
        "advanced": True,
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

    # 当前AI服务商（可覆盖全局设置，a_前缀确保排在设置面板最顶部）
    "a_l_provider": {
        "title": tr("当前AI服务商"),
        "default": "",
        "optionsList": [
            ["", tr("跟随全局设置")],
            ["openai", "OpenAI"],
            ["gemini", "Google Gemini"],
            ["xai", "xAI Grok"],
            ["openrouter", "OpenRouter"],
            ["siliconflow", "硅基流动 (SiliconFlow)"],
            ["doubao", "豆包 (Doubao)"],
            ["alibaba", "阿里云百炼 (Alibaba)"],
            ["zhipu", "智谱AI (Z.AI)"],
            ["glm_ocr", "GLM-OCR"],
            ["ollama", "Ollama (本地)"],
            ["lmstudio", "LM Studio (本地)"],
            ["llamacpp", "llama.cpp (本地)"],
            ["groq", "Groq"],
            ["infinigence", "无问芯穷 (Infinigence)"],
            ["mistral", "Mistral AI"],
            ["modelscope", "魔搭 (ModelScope)"],
            ["mimo", "小米MiMo"],
            ["intern", "浦源书生 (Intern)"],
            ["kimi", "Kimi (月之暗面)"],
            ["nvidia_nim", "NVIDIA NIM"],
            ["mineru", "MinerU"],
            ["paddle", "PaddleOCR (在线)"],
            ["paddle_vl_16", "PaddleOCR-VL-1.6 (在线)"],
            ["pp_structure_v3", "PP-StructureV3 (在线)"],
            ["longcat", "Longcat AI"],
        ],
        "toolTip": tr("选择当前AI服务商。默认跟随全局设置，也可在此直接切换（切换后全局设置同步更新）。"),
    },

    "dual_strategy": {
        "title": tr("识别策略"),
        "default": "ai_high_precision_with_coordinates",
        "optionsList": [
            ["ai_high_precision_with_coordinates", tr("双通道：AI高精度识别（含位置版）")],
            ["ai_high_precision_text_only", tr("仅AI高精度识别")],
        ],
        "toolTip": tr("选择识别策略：含位置高精度或纯文本高精度。"),
    },
    
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
            ["markdown", tr("Markdown格式")],
        ],
        "toolTip": tr("选择OCR结果的输出格式。坐标信息可用于定位文字位置。Markdown格式将直接输出AI返回的Markdown内容。"),
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
    # 新增：双通道性能优化选项
    "dual_max_boxes": {
        "title": tr("最大识别框数"),
        "default": 30,
        "min": 1,
        "max": 200,
        "unit": tr("个"),
        "isInt": True,
        "toolTip": tr("限制需要送到AI识别的裁剪框数量，超过将截断。"),
    },
    "dual_min_area": {
        "title": tr("最小框面积"),
        "default": 0,
        "min": 0,
        "max": 50000,
        "unit": "px^2",
        "isInt": True,
        "toolTip": tr("过滤过小的检测框以提升速度，单位为像素面积。"),
    },
    "dual_max_workers": {
        "title": tr("并发识别数"),
        "default": 3,
        "min": 1,
        "max": 20,
        "unit": tr("个"),
        "isInt": True,
        "toolTip": tr("并发向AI发送识别请求，提升总体速度。PaddleOCR异步模式下建议设为5-10。"),
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
    
    "mineru_enable_table": {
        "title": tr("MinerU 表格识别"),
        "default": True,
        "toolTip": tr("【仅MinerU平台】启用表格识别功能。"),
    },
    "mineru_enable_formula": {
        "title": tr("MinerU 公式识别"),
        "default": True,
        "toolTip": tr("【仅MinerU平台】启用公式识别功能。"),
    },
    
    "paddle_use_doc_unwarping": {
        "title": tr("文档扭曲矫正"),
        "default": False,
        "toolTip": tr("【PP-OCRv6/VL-1.6/V3通用】自动矫正扭曲图片（褶皱、倾斜等）。"),
    },
    "paddle_use_doc_orientation_classify": {
        "title": tr("文档方向分类"),
        "default": False,
        "toolTip": tr("【PP-OCRv6/VL-1.6/V3通用】自动识别并矫正0°/90°/180°/270°的图片方向。"),
    },
    "paddle_use_textline_orientation": {
        "title": tr("文本行方向矫正"),
        "default": False,
        "toolTip": tr("【仅PP-OCRv6/V3】自动识别和矫正0°/180°的文本行方向。"),
    },
    "paddle_use_layout_detection": {
        "title": tr("版面区域检测"),
        "default": False,
        "toolTip": tr("【仅VL-1.6】自动检测文档中不同区域并排序。"),
    },
    "paddle_use_chart_recognition": {
        "title": tr("图表识别"),
        "default": False,
        "toolTip": tr("【VL-1.6/V3】自动解析图表（柱状图、饼图等）并转换为表格。"),
    },
    "paddle_use_formula_recognition": {
        "title": tr("公式识别"),
        "default": False,
        "toolTip": tr("【仅V3】自动识别文档中的公式并转换为LaTeX格式。"),
    },
    "paddle_use_seal_recognition": {
        "title": tr("印章识别"),
        "default": False,
        "toolTip": tr("【仅VL-1.6/V3】自动识别文档中的印章内容。"),
    },
    "paddle_prettify_markdown": {
        "title": tr("Markdown美化"),
        "default": True,
        "toolTip": tr("【仅VL-1.6】启用Markdown格式美化输出。"),
    },
    "paddle_repetition_penalty": {
        "title": tr("重复惩罚参数"),
        "default": 1.0,
        "min": 1.0,
        "max": 2.0,
        "toolTip": tr("【仅VL-1.6】重复惩罚参数(1.0-2.0)，用于减少重复输出。"),
    },
    "paddle_temperature": {
        "title": tr("温度参数"),
        "default": 0.1,
        "min": 0.0,
        "max": 1.0,
        "toolTip": tr("【仅VL-1.6】温度参数(0.0-1.0)，控制输出的随机性。"),
    },
    "paddle_relevel_titles": {
        "title": tr("标题重分级"),
        "default": False,
        "toolTip": tr("【仅VL-1.6】启用标题重分级功能，自动调整标题层级。"),
    },
    "paddle_merge_tables": {
        "title": tr("表格合并"),
        "default": False,
        "toolTip": tr("【仅VL-1.6】启用表格合并功能，合并跨页或分割的表格。"),
    },
}
