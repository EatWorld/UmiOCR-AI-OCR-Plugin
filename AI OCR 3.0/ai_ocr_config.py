#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AI OCR Plugin Configuration

import os

from plugin_i18n import Translator

from .model_lists import (
    MODEL_CUSTOM_VALUE,
    MODEL_CURATED_LISTS,
    PROVIDER_DISPLAY_NAMES,
    build_model_options,
)

tr = Translator(__file__, "i18n.csv")

# 服务商配置映射
PROVIDER_CONFIGS = {
    "openai": {
        "api_base": "https://api.openai.com/v1",
        "model": "",  # 用户自定义
    },
    "custom_openai": {  # 自定义OpenAI兼容服务商
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
    "hunyuan": {  # 腾讯混元
        "api_base": "https://tokenhub.tencentmaas.com/v1",
        "model": "hy-vision-2.0-instruct",
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
    "intern": {  # 浦源书生（书生平台 2026-10 起启用 discovery-api 域名）
        "api_base": "https://discovery-api.intern-ai.org.cn/v1",
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
    "agnes": {
        "api_base": "https://apihub.agnes-ai.com/v1",
        "model": "agnes-2.0-flash",
    },
    "xflyun": {
        "api_base": "https://maas-api.cn-huabei-1.xf-yun.com/v2",
        "model": "xoppaddleocrv16",
    },
    # OpenCode Go / Zen：OpenAI 兼容网关（请求发送至 {api_base}/chat/completions）
    "opencode_go": {
        "api_base": "https://opencode.ai/zen/go/v1",
        "model": "grok-4.5",  # 默认视觉模型，可在设置中修改
    },
    "opencode_zen": {
        "api_base": "https://opencode.ai/zen/v1",
        "model": "kimi-k3",  # 默认视觉模型，可在设置中修改
    },
    # 面壁智能（ModelBest）：文档解析模型（MiniCPM-OCR），同步/异步双模式
    "modelbest": {
        "api_base": "https://api.modelbest.ai",
        "model": "MiniCPM-OCR-1.0",
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
            ["custom_openai", tr("自定义OpenAI兼容 (Custom)")],
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
            ["hunyuan", "腾讯混元 (Hunyuan)"],
            ["mistral", "Mistral AI"],
            ["modelscope", "魔搭 (ModelScope)"],
            ["mimo", "小米MiMo"],
            ["intern", "浦源书生 (Intern)"],
            ["kimi", "Kimi (月之暗面)"],
            ["nvidia_nim", "NVIDIA NIM"],
            ["mineru", "MinerU"],
            ["modelbest", tr("面壁智能 (ModelBest)")],
            ["paddle", "PaddleOCR (在线)"],
            ["paddle_vl_16", "PaddleOCR-VL-1.6 (在线)"],
            ["pp_structure_v3", "PP-StructureV3 (在线)"],
            ["longcat", "Longcat AI"],
            ["agnes", "Agnes"],
            ["xflyun", "讯飞星辰 (MaaS)"],
            ["opencode_go", "OpenCode Go"],
            ["opencode_zen", "OpenCode Zen"],

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

    # 文本检测器配置（双通道模式）
    "a_v6_detector_version": {
        "title": tr("检测器版本"),
        "default": "v6_onnx",
        "optionsList": [
            ["v6_onnx", tr("PP-OCRv6 ONNX（推荐，更快更准）")],
            ["v3_legacy", tr("PP-OCRv3 旧版（兼容回退）")],
        ],
        "toolTip": tr("双通道模式的文本检测器版本。v6 基于 ONNX 推理，速度更快、精度更高；v3 为旧版 C++ 实现，仅作兼容回退。"),
    },
    "a_v6_model_size": {
        "title": tr("v6检测模型"),
        "default": "small",
        "optionsList": [
            ["small", tr("Small（7.7MB，推荐，速度快）")],
            ["medium", tr("Medium（34.5MB，精度高，较慢）")],
            ["tiny", tr("Tiny（1.5MB，最快，精度较低）")],
        ],
        "toolTip": tr("PP-OCRv6 ONNX 检测模型大小。检测仅用于文字分块定位，small 已足够；追求极致速度可选 tiny，复杂版面可选 medium。需下载对应模型文件。"),
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
        "default": "doubao-seed-2-0-pro",
        "type": "text",
        "toolTip": tr("豆包模型名称，如：doubao-seed-2-0-pro, doubao-seed-2-1-pro-260628, Doubao-1.5-vision-pro-32k"),
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

    # 自定义OpenAI兼容服务商配置
    "custom_openai_api_key": {
        "title": tr("自定义OpenAI兼容 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入自定义OpenAI兼容平台的API密钥"),
    },
    "custom_openai_model": {
        "title": tr("自定义OpenAI兼容 模型"),
        "default": "",
        "type": "text",
        "toolTip": tr("OpenAI兼容模型名称，如：gpt-4o, qwen-vl-plus, deepseek-vl2 等"),
    },
    "custom_openai_api_base": {
        "title": tr("自定义OpenAI兼容 API地址"),
        "default": "https://api.openai.com/v1",
        "type": "text",
        "toolTip": tr("OpenAI兼容API地址。默认：https://api.openai.com/v1 ；可填写任意兼容平台（如 vLLM、One API、new-api 中转、自建服务等）的地址，请求将发送到 {地址}/chat/completions"),
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
        "default": "PaddlePaddle/PaddleOCR-VL-1.5",
        "type": "text",
        "toolTip": tr("硅基流动模型名称，如：PaddlePaddle/PaddleOCR-VL-1.5（免费）、Qwen/Qwen3-VL-32B-Instruct、Qwen/Qwen3.5-122B-A10B（Qwen2.5-VL 系列与 Qwen3-VL-235B 已于 2026-04 下线）"),
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

    # 腾讯混元配置
    "hunyuan_api_key": {
        "title": tr("腾讯混元 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入腾讯混元的API密钥"),
    },
    "hunyuan_model": {
        "title": tr("腾讯混元 模型"),
        "default": "hy-vision-2.0-instruct",
        "type": "text",
        "toolTip": tr("腾讯混元视觉模型名称，如：hy-vision-2.0-instruct, hunyuan-t1-vision-20250916, youtu-vita"),
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
        "default": "mistral-ocr-latest",
        "type": "text",
        "toolTip": tr("Mistral OCR模型名称，推荐：mistral-ocr-latest（即mistral-ocr-4-0）；也可使用视觉模型如pixtral-12b-2409"),
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
        "toolTip": tr("MiMo视觉模型名称，如：mimo-v2.5"),
    },
    "mimo_api_base": {
        "title": tr("小米MiMo API地址"),
        "default": "https://api.xiaomimimo.com/v1",
        "type": "text",
        "toolTip": tr("小米MiMo平台的API地址。默认：https://api.xiaomimimo.com/v1 ；如购买了Code套餐，请使用专属地址：https://token-plan-cn.xiaomimimo.com/v1"),
    },
    # 浦源书生配置（书生平台 2026-10 起启用 discovery-api 新域名）
    "intern_api_key": {
        "title": tr("浦源书生 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入浦源书生的API密钥。注意：生成模型限速 50 次/分钟、决策模型 200 次/分钟（所有 API Key 共享额度），建议在高级设置中将\"每分钟最大请求数\"设为 40 左右"),
    },
    "intern_model": {
        "title": tr("浦源书生 模型"),
        "default": "intern-latest",
        "type": "text",
        "toolTip": tr("浦源书生多模态模型，如：intern-latest、intern-s2-preview、intern-s1-pro、internvl3.5-241b-a28b"),
    },
    "intern_api_base": {
        "title": tr("浦源书生 API地址"),
        "default": "https://discovery-api.intern-ai.org.cn/v1",
        "type": "text",
        "toolTip": tr("书生平台API地址，默认：https://discovery-api.intern-ai.org.cn/v1（2026年10月起启用的新域名；旧地址 chat.intern-ai.org.cn/api/v1 已停用）"),
        "advanced": True,
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

    # Agnes配置
    "agnes_api_key": {
        "title": tr("Agnes API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入Agnes平台的API Key"),
    },
    "agnes_model": {
        "title": tr("Agnes 模型"),
        "default": "agnes-2.0-flash",
        "type": "text",
        "toolTip": tr("Agnes模型名称，如：agnes-2.0-flash"),
    },
    "agnes_api_base": {
        "title": tr("Agnes API地址"),
        "default": "https://apihub.agnes-ai.com/v1",
        "type": "text",
        "toolTip": tr("Agnes的API地址，默认：https://apihub.agnes-ai.com/v1"),
        "advanced": True,
    },

    # 讯飞星辰 MaaS 配置
    "xflyun_api_key": {
        "title": tr("讯飞星辰 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入讯飞星辰MaaS平台的APIKey（从服务管控页面获取）"),
    },
    "xflyun_model": {
        "title": tr("讯飞星辰 模型"),
        "default": "xoppaddleocrv16",
        "type": "text",
        "toolTip": tr("讯飞星辰模型ID（从服务管控页面获取）。注意讯飞平台模型名与其他平台不同：xoppaddleocrv16（PaddleOCR-VL-1.6）、xophunyuanocr（HunyuanOCR）；DeepSeek-OCR暂不支持API调用"),
    },
    "xflyun_api_base": {
        "title": tr("讯飞星辰 API地址"),
        "default": "https://maas-api.cn-huabei-1.xf-yun.com/v2",
        "type": "text",
        "toolTip": tr("讯飞星辰MaaS API地址，默认：https://maas-api.cn-huabei-1.xf-yun.com/v2（2026年1月10日后发布服务的用户）；存量用户可使用 http://maas-api.cn-huabei-1.xf-yun.com/v1"),
        "advanced": True,
    },

    # OpenCode Go 配置
    "opencode_go_api_key": {
        "title": tr("OpenCode Go API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入OpenCode Go的API密钥（在 https://opencode.ai/auth 订阅 Go 后获取）"),
    },
    "opencode_go_model": {
        "title": tr("OpenCode Go 模型"),
        "default": "grok-4.5",
        "type": "text",
        "toolTip": tr("OpenCode Go模型名称（需支持图像输入的视觉模型），如：grok-4.5、glm-5.2、kimi-k3、kimi-k2.6、deepseek-v4-pro、mimo-v2.5、hy3。完整列表见 https://opencode.ai/zen/go/v1/models"),
    },
    "opencode_go_api_base": {
        "title": tr("OpenCode Go API地址"),
        "default": "https://opencode.ai/zen/go/v1",
        "type": "text",
        "toolTip": tr("OpenCode Go的OpenAI兼容API地址，默认：https://opencode.ai/zen/go/v1 （请求将发送到 {地址}/chat/completions）"),
        "advanced": True,
    },

    # OpenCode Zen 配置
    "opencode_zen_api_key": {
        "title": tr("OpenCode Zen API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入OpenCode Zen的API密钥（在 https://opencode.ai/auth 登录 Zen 后获取）"),
    },
    "opencode_zen_model": {
        "title": tr("OpenCode Zen 模型"),
        "default": "kimi-k3",
        "type": "text",
        "toolTip": tr("OpenCode Zen模型名称（需支持图像输入的视觉模型），如：kimi-k3、kimi-k2.6、glm-5.2、deepseek-v4-pro、minimax-m3、hy3-free。注意：仅 chat/completions 接口的模型可用于OCR；GPT/Claude/Gemini 等走 responses/messages 接口的模型暂不支持。完整列表见 https://opencode.ai/zen/v1/models"),
    },
    "opencode_zen_api_base": {
        "title": tr("OpenCode Zen API地址"),
        "default": "https://opencode.ai/zen/v1",
        "type": "text",
        "toolTip": tr("OpenCode Zen的OpenAI兼容API地址，默认：https://opencode.ai/zen/v1 （请求将发送到 {地址}/chat/completions）"),
        "advanced": True,
    },

    # 面壁智能（ModelBest）文档解析配置
    "modelbest_api_key": {
        "title": tr("面壁智能 API密钥"),
        "default": "",
        "type": "text",
        "toolTip": tr("请输入面壁智能（ModelBest）的 MAP API Key（登录 https://platform.modelbest.ai → 控制台 → API Keys 获取）"),
    },
    "modelbest_model": {
        "title": tr("面壁智能 模型"),
        "default": "MiniCPM-OCR-1.0",
        "type": "text",
        "toolTip": tr('面壁智能文档解析模型，默认 MiniCPM-OCR-1.0。可从下拉菜单选择（可通过"获取模型列表"按钮在线更新）；选择"自定义（手动输入）"后可在高级设置中填写任意模型名。'),
    },
    "modelbest_api_base": {
        "title": tr("面壁智能 API地址"),
        "default": "https://api.modelbest.ai",
        "type": "text",
        "toolTip": tr("面壁智能开放平台API基础地址，默认：https://api.modelbest.ai （文档解析请求发送到 {地址}/v1/document-parse）"),
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
    "z_rate_limit": {
        "title": tr("每分钟最大请求数"),
        "default": 0,
        "min": 0,
        "max": 600,
        "unit": tr("次/分钟"),
        "isInt": True,
        "toolTip": tr("API请求速率限制（令牌桶算法，主动避免429限流）。0表示不限制。建议设为服务商限额的80%左右。密钥池：在任意服务商的API密钥框中填写多个密钥（用逗号、分号或换行分隔），插件将自动轮询使用，分摊请求压力。"),
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
            ["custom_openai", tr("自定义OpenAI兼容 (Custom)")],
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
            ["hunyuan", "腾讯混元 (Hunyuan)"],
            ["mistral", "Mistral AI"],
            ["modelscope", "魔搭 (ModelScope)"],
            ["mimo", "小米MiMo"],
            ["intern", "浦源书生 (Intern)"],
            ["kimi", "Kimi (月之暗面)"],
            ["nvidia_nim", "NVIDIA NIM"],
            ["mineru", "MinerU"],
            ["modelbest", tr("面壁智能 (ModelBest)")],
            ["paddle", "PaddleOCR (在线)"],
            ["paddle_vl_16", "PaddleOCR-VL-1.6 (在线)"],
            ["pp_structure_v3", "PP-StructureV3 (在线)"],
            ["longcat", "Longcat AI"],
            ["agnes", "Agnes"],
            ["xflyun", "讯飞星辰 (MaaS)"],
            ["opencode_go", "OpenCode Go"],
            ["opencode_zen", "OpenCode Zen"],
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
    "dual_limit_side_len": {
        "title": tr("检测分辨率"),
        "default": 1440,
        "min": 320,
        "max": 4096,
        "unit": "px",
        "isInt": True,
        "toolTip": tr("检测器输入图像的长边限制。值越大检测越精细但越慢；值越小检测越快但可能漏检小字。推荐 1440，小字密集文档可提高到 1920。"),
        "advanced": True,
    },
    "paddle_timeout": {
        "title": tr("检测超时"),
        "default": 20,
        "min": 5,
        "max": 120,
        "unit": tr("秒"),
        "isInt": True,
        "toolTip": tr("文本检测的超时时间。超时后跳过检测，直接使用AI识别。"),
        "advanced": True,
    },
    "dual_max_boxes": {
        "title": tr("最大识别框数"),
        "default": 100,
        "min": 1,
        "max": 500,
        "unit": tr("个"),
        "isInt": True,
        "toolTip": tr("限制需要送到AI识别的裁剪框数量，超过将截断。值越小AI识别越快，但可能漏掉部分文字。文档识别建议 100 以上。"),
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


# ============================================================
# =============== 模型下拉菜单与在线列表获取 ===============
# ============================================================
# 全局设置中各平台的"模型"字段由手填文本框升级为下拉菜单：
#   候选 = 内置精选列表 + 在线拉取缓存(model_lists_cache.json) + 已保存的当前值 + "自定义"
# - 已保存的旧值（含历史手填的自定义模型）会合并进候选列表，升级后不会被枚举校验重置；
# - 选择"自定义（手动输入）"时，实际调用改用下方自动生成的"{平台} 自定义模型"手填框，
#   与旧版纯手填行为完全兼容（本地模型、未收录模型、中转站模型均可手填）；
# - 可通过"获取模型列表"按钮（或"刷新模型列表.bat"脚本）在线更新候选列表。

# 检测 Umi-OCR 核心是否支持"按钮 onClicked 为字符串 → callPy"分发
# （Configs.qml compBtns 中的字符串分支；原版核心仅有函数分支）。
def _detect_btn_call_support():
    try:
        qml_path = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "qt_res", "qml", "Configs", "Configs.qml",
        ))
        if os.path.isfile(qml_path):
            with open(qml_path, "r", encoding="utf-8", errors="replace") as f:
                return 'callPy("ocr"' in f.read() or "callPy('ocr'" in f.read()
    except Exception:
        pass
    return False


def _check_fetch_hooks_installed():
    """检测 ai_ocr.py 是否已成功把 aioFetchModels 挂载到 MissionOCR。"""
    try:
        from py_src.mission.mission_ocr import MissionOCR
        return getattr(MissionOCR, "_aio_fetch_hooks", False)
    except Exception:
        return False


CORE_SUPPORTS_BTN_CALL = _detect_btn_call_support() and _check_fetch_hooks_installed()

# 已追加过"自定义手填指引"的服务商（rebuild_model_options 可重入，防重复追加）
_HINT_APPENDED_PROVIDERS = set()


def rebuild_model_options():
    """(重)构建各平台模型下拉候选，并补 {provider}_model_custom 手填框。

    候选策略（见 model_lists.build_model_options）：**在线列表强制优先**——已成功
    拉取过在线列表的平台仅用"在线列表 + 已存值 + 自定义"；未拉取过的平台以内置
    精选列表作引导。本函数可重复调用：在线拉取成功后由 ai_ocr.py 的刷新钩子再次
    执行，使下拉菜单即时反映最新平台列表（无需重启）。
    """
    from .model_lists import read_saved_ui_settings, load_model_list_cache
    saved_settings = read_saved_ui_settings()
    cache = load_model_list_cache()
    for provider in MODEL_CURATED_LISTS:
        key = f"{provider}_model"
        item = globalOptions.get(key)
        if not isinstance(item, dict) or "title" not in item:
            continue  # paddle 系列等未导出模型项的平台保持原样
        old_default = item.get("default", "")
        # 显式 type:"text" 会阻止 QML 将 optionsList 推断为枚举，必须移除
        item.pop("type", None)
        item["optionsList"] = build_model_options(
            provider, default_model=old_default, saved_settings=saved_settings, cache=cache
        )
        # 旧默认值可能为空或不在候选内（如 custom_openai/llamacpp/默认值被在线列表替换），避免枚举校验重置
        option_keys = [o[0] for o in item["optionsList"]]
        if item.get("default", "") not in option_keys:
            item["default"] = option_keys[0]
        # 平台显示名（悬停指引与自定义框标题共用）
        name = PROVIDER_DISPLAY_NAMES.get(provider, provider)
        # 在下拉框悬停提示中追加自定义模型填写指引（自定义输入框默认随"高级"隐藏，需显式指路）
        # 仅追加一次（用进程内标记而非文本匹配——tr 译文随语言变化，文本匹配会在
        # 非中文语言下失效导致每次刷新重复追加）：本函数会被热刷新反复调用
        if provider not in _HINT_APPENDED_PROVIDERS:
            _HINT_APPENDED_PROVIDERS.add(provider)
            item["toolTip"] = (item.get("toolTip") or "") + tr(
                '【自定义模型】如需手填：先在上方下拉菜单选择"自定义（手动输入）"，然后开启页面右上角的「高级」开关，在下方带 * 号的"{0} 自定义模型"框中输入模型名（需支持图像输入；留空则回退默认模型）。'
            ).format(name)
        # 追加"自定义"手填框（QVariantMap 按键名字母序渲染，自动紧跟在 model 字段之后）
        globalOptions[f"{provider}_model_custom"] = {
            "title": tr("{0} 自定义模型").format(name),
            "default": old_default or "",
            "type": "text",
            "toolTip": tr('当"{0} 模型"选择"自定义（手动输入）"时生效。直接填写任意模型名（需支持图像输入），与旧版手填行为一致。').format(name),
            "advanced": True,
        }


rebuild_model_options()

# "获取模型列表"按钮：仅在核心 QML 支持字符串分发且钩子挂载成功时渲染
if CORE_SUPPORTS_BTN_CALL:
    globalOptions["a_fetch_models_btns"] = {
        "title": tr("获取模型列表"),
        "btnsList": [
            {"text": tr("🔄 拉取当前服务商"), "onClicked": "aioFetchModels", "textColorKey": "yesColor"},
            {"text": tr("🔄 拉取全部已配置平台"), "onClicked": "aioFetchAllModels", "textColorKey": "noColor"},
        ],
        "toolTip": tr("通过各平台API在线获取模型列表并更新上方下拉菜单。未配置API密钥的平台自动跳过；本地服务（Ollama等）需处于运行状态。结果缓存于插件目录 model_lists_cache.json，重启 Umi-OCR 后同样生效。"),
    }

# 面壁智能（ModelBest）局部配置项
localOptions["modelbest_upright"] = {
    "title": tr("文档自适应旋转"),
    "default": True,
    "toolTip": tr("【仅面壁智能】开启后自动旋转倾斜/倒置的文档图片再识别。注意：旋转后返回的坐标以矫正后页面为基准，如需精确坐标建议关闭。"),
}
localOptions["modelbest_recognize_seal"] = {
    "title": tr("印章内容识别"),
    "default": True,
    "toolTip": tr("【仅面壁智能】识别文档中的印章并输出其文字内容。关闭时印章区域保留布局但内容为空。"),
}
