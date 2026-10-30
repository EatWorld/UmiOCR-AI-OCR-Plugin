#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AI OCR 插件 —— 模型列表获取与缓存模块
#
# 为全局设置的"模型下拉菜单"提供数据源：
#   1. MODEL_CURATED_LISTS：内置精选模型列表（仅在平台从未成功拉取时作为引导候选）
#   2. model_lists_cache.json：通过平台 API 拉取的在线模型列表缓存
#      （由"拉取模型列表"按钮、"应用修改"时的自动补拉或"刷新模型列表.bat"写入，
#       热刷新/重启后下拉菜单即以在线列表为准——强制平台实时列表，不与精选混排）
#   3. UmiOCR-data/.settings：用户已保存的模型值（合并进下拉列表，防止升级后枚举校验把旧值重置）
#
# 地址归一化规则（与实际调用时的归一化保持一致）：
#   - Gemini（地址含 generativelanguage.googleapis.com）：从完整 :generateContent 端点
#     自动归位到 models 列表端点（裸 base、/models、完整模型端点均可归一），
#     过滤出支持 generateContent 的模型；
#   - Ollama 本地（base 以 /api 结尾或含 :11434）：走 /api/tags 列出已安装模型，无需 Key；
#   - 其余按 OpenAI 兼容：GET {base}/models（Bearer 认证），base 支持带或不带
#     /chat/completions 后缀。
#
# 本模块既被插件导入使用，也可直接作为脚本运行：
#   python model_lists.py                # 拉取全部已配置平台
#   python model_lists.py --provider kimi openai
#   python model_lists.py --list         # 仅查看缓存

import json
import os
import re
import ssl
import sys
import threading
import urllib.request

# 模型下拉菜单中"自定义"选项的特殊值（选中后使用 {provider}_model_custom 手填值）
MODEL_CUSTOM_VALUE = "__custom__"

# 缓存读写锁：按钮拉取与多个自动补拉线程并发"读-合并-写"时防止互相覆盖
_CACHE_LOCK = threading.RLock()

# 插件目录（model_lists.py 所在目录）
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
# UmiOCR-data 目录（插件目录上两级：plugins/<插件名>/ → UmiOCR-data）；.settings 文件位于此
UMI_DATA_DIR = os.path.dirname(os.path.dirname(PLUGIN_DIR))
SETTINGS_PATH = os.path.join(UMI_DATA_DIR, ".settings")
CACHE_PATH = os.path.join(PLUGIN_DIR, "model_lists_cache.json")


# ============================================================
# =============== 内置精选模型列表（离线兜底） ===============
# ============================================================
# 只收录确定存在的模型 ID 作为默认候选；完整列表请用"拉取模型列表"功能在线获取。
# 列表为空的平台（如自定义 OpenAI 兼容）仅提供"自定义"入口。

MODEL_CURATED_LISTS = {
    "openai": ["gpt-5-mini", "gpt-4.1", "gpt-4.1-mini", "gpt-4o"],
    "custom_openai": [],
    "gemini": ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
    "xai": ["grok-4", "grok-3"],
    "openrouter": [
        "moonshotai/kimi-k2.6:free",
        "qwen/qwen3-vl-235b-a22b-instruct",
        "nvidia/nemotron-3.5-super-vl:free",
        "google/gemini-2.5-flash",
    ],
    "siliconflow": [
        "PaddlePaddle/PaddleOCR-VL-1.5",
        "Qwen/Qwen3-VL-32B-Instruct",
        "Qwen/Qwen3.5-122B-A10B",
    ],
    "doubao": ["doubao-seed-2-0-pro", "doubao-seed-2-1-pro-260628", "Doubao-1.5-vision-pro-32k"],
    "zhipu": ["glm-ocr", "glm-4.6v", "glm-4.5v", "glm-4v-plus", "glm-4v-flash"],
    "glm_ocr": ["glm-ocr"],
    "alibaba": [
        "qwen-vl-plus",
        "qwen-vl-max",
        "qwen-vl-ocr",
        "qwen3-vl-plus",
        "qwen3-vl-235b-a22b-instruct",
    ],
    "ollama": ["llava:latest", "qwen2.5vl:7b", "qwen3vl:8b"],
    "lmstudio": ["llava", "llava-1.5-7b-hf"],
    "llamacpp": [],
    "groq": [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "meta-llama/llama-4-maverick-17b-128e-instruct",
    ],
    "hunyuan": ["hy-vision-2.0-instruct", "hunyuan-t1-vision-20250916", "youtu-vita"],
    "mistral": ["mistral-ocr-latest", "pixtral-12b-2409"],
    "modelscope": ["Qwen/Qwen3-VL-235B-A22B-Instruct", "Qwen/Qwen-VL-Plus", "Qwen/QVQ-72B-Preview"],
    "mimo": ["mimo-v2.5"],
    "intern": ["intern-latest", "intern-s2-preview", "intern-s1-pro", "internvl3.5-241b-a28b"],
    "kimi": ["kimi-k2.6", "kimi-k2.5", "moonshot-v1-128k-vision-preview"],
    "nvidia_nim": ["moonshotai/kimi-k2.6"],
    "longcat": ["LongCat-Flash-Chat", "LongCat-Flash-Thinking", "LongCat-Flash-Lite"],
    "agnes": ["agnes-2.0-flash"],
    "xflyun": ["xoppaddleocrv16", "xophunyuanocr"],
    "opencode_go": ["grok-4.5", "glm-5.2", "kimi-k3", "kimi-k2.6", "deepseek-v4-pro", "mimo-v2.5", "hy3"],
    "opencode_zen": ["kimi-k3", "kimi-k2.6", "glm-5.2", "deepseek-v4-pro", "minimax-m3", "hy3-free"],
    "modelbest": ["MiniCPM-OCR-1.0"],
    "mineru": ["vlm", "pipeline", "MinerU-HTML"],
}

# 各服务商模型列表的获取方式
# kind: openai=GET {base}/models（Bearer）；gemini=GET {base}/models?key=（过滤 generateContent）；
#       ollama=GET {base}/tags（无需 Key）
PROVIDER_LIST_RULES = {
    "openai": {"kind": "openai"},
    "custom_openai": {"kind": "openai"},
    "gemini": {"kind": "gemini"},
    "xai": {"kind": "openai"},
    "openrouter": {"kind": "openai"},
    "siliconflow": {"kind": "openai"},
    "doubao": {"kind": "openai"},
    "zhipu": {"kind": "openai"},
    "glm_ocr": {"kind": "openai"},
    "alibaba": {"kind": "openai"},
    "ollama": {"kind": "ollama"},
    "lmstudio": {"kind": "openai"},
    "llamacpp": {"kind": "openai"},
    "groq": {"kind": "openai"},
    "hunyuan": {"kind": "openai"},
    "mistral": {"kind": "openai"},
    "modelscope": {"kind": "openai"},
    "mimo": {"kind": "openai"},
    "intern": {"kind": "openai"},
    "kimi": {"kind": "openai"},
    "nvidia_nim": {"kind": "openai"},
    "longcat": {"kind": "openai"},
    "agnes": {"kind": "openai"},
    "xflyun": {"kind": "openai"},
    "opencode_go": {"kind": "openai"},
    "opencode_zen": {"kind": "openai"},
    # 面壁智能：base 为裸域名，列表端点为 {base}/v1/models（_normalize_openai_base 会补 /v1）
    "modelbest": {"kind": "openai"},
    "mineru": None,  # MinerU 无模型列表端点（model_version 固定枚举）
    "paddle": None,
    "paddle_vl_16": None,
    "pp_structure_v3": None,
}

# 本地服务商：无需 API 密钥也尝试拉取
LOCAL_PROVIDERS = ("ollama", "lmstudio", "llamacpp")

# 各服务商默认 API 地址（与 ai_ocr_config.PROVIDER_CONFIGS 保持一致；此处冗余一份供脚本独立运行）
DEFAULT_API_BASES = {
    "openai": "https://api.openai.com/v1",
    "custom_openai": "https://api.openai.com/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta",
    "xai": "https://api.x.ai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "siliconflow": "https://api.siliconflow.cn/v1",
    "doubao": "https://ark.cn-beijing.volces.com/api/v3",
    "zhipu": "https://open.bigmodel.cn/api/paas/v4",
    "glm_ocr": "https://open.bigmodel.cn/api/paas/v4",
    "alibaba": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "ollama": "http://localhost:11434/api",
    "lmstudio": "http://localhost:1234/v1",
    "llamacpp": "http://localhost:8080/v1",
    "groq": "https://api.groq.com/openai/v1",
    "hunyuan": "https://tokenhub.tencentmaas.com/v1",
    "mistral": "https://api.mistral.ai/v1",
    "modelscope": "https://api-inference.modelscope.cn/v1",
    "mimo": "https://api.xiaomimimo.com/v1",
    "intern": "https://discovery-api.intern-ai.org.cn/v1",
    "kimi": "https://api.moonshot.cn/v1",
    "nvidia_nim": "https://integrate.api.nvidia.com/v1",
    "longcat": "https://api.longcat.chat/openai/v1",
    "agnes": "https://apihub.agnes-ai.com/v1",
    "xflyun": "https://maas-api.cn-huabei-1.xf-yun.com/v2",
    "opencode_go": "https://opencode.ai/zen/go/v1",
    "opencode_zen": "https://opencode.ai/zen/v1",
    "modelbest": "https://api.modelbest.ai",
}


# ============================================================
# =============== UmiOCR-data/.settings 读取 ===============
# ============================================================

def _unescape_ini_value(v):
    """按 QSettings INI 规则反转义值内容（Qt: \\n \\\\ 等；带引号则去除引号）。

    必须 Qt 侧读出什么，这里就解出什么 —— 合并进下拉列表的已存模型值要与
    Configs.qml 的 settings.value(key) 完全一致，否则枚举校验失败会被重置。
    """
    if v is None:
        return ""
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        v = v[1:-1]
    out = []
    i = 0
    n = len(v)
    while i < n:
        c = v[i]
        if c == "\\" and i + 1 < n:
            nxt = v[i + 1]
            simple = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", '"': '"', "'": "'", "s": " "}
            if nxt in simple:
                out.append(simple[nxt])
                i += 2
                continue
            if nxt in ("x", "X"):
                hex_part = v[i + 2:i + 6]
                if len(hex_part) == 4:
                    try:
                        out.append(chr(int(hex_part, 16)))
                        i += 6
                        continue
                    except ValueError:
                        pass
        out.append(c)
        i += 1
    return "".join(out)


def read_saved_ui_settings(settings_path=None):
    """读取 .settings 文件中 [Global] 段的配置，返回以短键名（如 "alibaba_model"）为键的字典。

    仅提取 "ocr.AIOCR." 前缀的本插件配置（其余插件/页面配置忽略）。
    读取失败返回 {}（不影响插件加载，下拉列表退化为 精选+缓存）。
    """
    path = settings_path or SETTINGS_PATH
    result = {}
    prefix = "ocr.AIOCR."
    try:
        if not os.path.isfile(path):
            return result
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            in_global = False
            for line in f:
                line = line.strip()
                if not line or line.startswith(";") or line.startswith("#"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_global = line[1:-1].strip() == "Global"
                    continue
                if not in_global or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key = key.strip()
                if not key.startswith(prefix):
                    continue
                result[key[len(prefix):]] = _unescape_ini_value(val)
    except Exception:
        return {}
    return result


# ============================================================
# =============== 缓存读写 ===============
# ============================================================

def load_model_list_cache(cache_path=None):
    """读取在线模型列表缓存。返回 {provider: [model_id, ...]}。"""
    path = cache_path or CACHE_PATH
    try:
        if not os.path.isfile(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        providers = data.get("providers", {})
        out = {}
        for p, info in providers.items():
            models = info.get("models") if isinstance(info, dict) else info
            if isinstance(models, list):
                out[p] = [str(m) for m in models if isinstance(m, (str, int, float)) and str(m).strip()]
        return out
    except Exception:
        return {}


def save_model_list_cache(results, cache_path=None):
    """写入缓存。results: {provider: {"models": [...], "ok": bool, "error": str}}

    线程安全：读-合并-写全程持锁。按钮拉取与多个自动补拉线程可能并发调用，
    无锁时并发读到大半写入的文件会 JSON 解析失败，进而以空表覆盖、清空全部缓存。
    """
    path = cache_path or CACHE_PATH
    import time as _time
    with _CACHE_LOCK:
        old = {}
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    old = json.load(f)
        except Exception:
            old = {}
        providers = old.get("providers", {}) if isinstance(old, dict) else {}
        for p, info in results.items():
            if isinstance(info, dict) and info.get("ok"):
                providers[p] = {
                    "models": info.get("models", []),
                    "fetched_at": _time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        payload = {
            "version": 1,
            "updated": _time.strftime("%Y-%m-%d %H:%M:%S"),
            "providers": providers,
        }
        try:
            tmp_path = path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, path)  # 原子替换，避免写一半被读到
            return True
        except Exception:
            return False


def build_model_options(provider, default_model="", saved_settings=None, cache=None):
    """构建某服务商模型下拉菜单的 optionsList。

    **在线列表强制优先**：
    - 已成功拉取过在线列表的平台：候选仅由"在线列表 + 已存值 + 自定义"组成，
      不混入任何内置精选项（以平台实时列表为准）；
    - 从未成功拉取的平台：以内置精选列表 + 默认值作为引导候选（首次"应用修改"
      会自动补拉，成功后热刷新替换为纯在线列表）。
    已存值（去首尾空白）始终追加，防止升级重置。
    """
    ids = []

    def _add(m):
        if m is None:
            return
        m = str(m)
        if m and m not in ids:
            ids.append(m)

    if cache is None:
        cache = load_model_list_cache()
    cached = cache.get(provider) or []
    if cached:
        for m in cached:
            _add(m)
    else:
        _add(default_model)
        for m in MODEL_CURATED_LISTS.get(provider, []):
            _add(m)
    if saved_settings is None:
        saved_settings = read_saved_ui_settings()
    saved = saved_settings.get(f"{provider}_model", "")
    if saved and saved != MODEL_CUSTOM_VALUE:
        saved = saved.strip()
        # 去首尾空白后入列（历史粘贴可能带换行，原样入列会把弹层撑破、控件重叠）。
        # 核心侧枚举匹配补丁会用"去空白后的值"再匹配一次，因此已存值不会因去空白而重置；
        # 含内部换行/制表的残值不入列，首枚举校验不通过时自动回退默认值（残值净化）。
        if saved and not any(c in saved for c in "\n\r\t"):
            _add(saved)
    options = [[m, m] for m in ids]
    options.append([MODEL_CUSTOM_VALUE, "自定义（手动输入）"])
    return options


# ============================================================
# =============== 地址归一化与在线拉取 ===============
# ============================================================

def _make_opener(proxy_url=None):
    """构建 urllib opener（忽略证书校验，与插件 HTTPClient 行为一致）"""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    handlers = [urllib.request.HTTPSHandler(context=ssl_context)]
    if proxy_url:
        handlers.append(urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url}))
    return urllib.request.build_opener(*handlers)


def _http_get(url, headers=None, timeout=15, proxy_url=None):
    opener = _make_opener(proxy_url)
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Umi-OCR-AIOCR"})
    with opener.open(req, timeout=timeout) as resp:
        return resp.getcode(), resp.read().decode("utf-8", errors="replace")


def _normalize_openai_base(base):
    """OpenAI 兼容：剥离 /chat/completions、/completions、/models 后缀得到列表 base。

    面壁智能等裸域名 base 会补全 /v1（列表端点为 {base}/v1/models）。
    """
    b = (base or "").strip().rstrip("/")
    for suffix in ("/chat/completions", "/completions", "/models"):
        if b.lower().endswith(suffix):
            b = b[: -len(suffix)]
            break
    m = re.match(r"^(https?://[^/]+)(/(.*))?$", b)
    if m:
        host, rest = m.group(1), (m.group(3) or "").strip("/")
        has_version = bool(re.search(r"(^|/)v\d", "/" + rest) if rest else False)
        if "modelbest.ai" in host and not has_version:
            b = host + "/v1"
    return b


def _normalize_gemini_base(base):
    """Gemini：裸 base、/models 结尾、完整 {base}/models/{model}:generateContent 均归一到列表 base。"""
    b = (base or "").strip().rstrip("/")
    m = re.match(r"^(https?://[^/]+/.+?)/models/[^/]+(?::[^/]+)?$", b)
    if m:
        b = m.group(1)
    if b.endswith("/models"):
        b = b[: -len("/models")]
    return b


def _normalize_ollama_base(base):
    """Ollama：以 /api 结尾（或裸 host:11434）统一归一到 {base}/api。"""
    b = (base or "").strip().rstrip("/")
    if not b.endswith("/api"):
        b = b + "/api"
    return b


def normalize_list_endpoint(provider, api_base, api_key=""):
    """按服务商类型归一化模型列表端点。返回 (url, headers)。"""
    rule = PROVIDER_LIST_RULES.get(provider) or {"kind": "openai"}
    kind = rule["kind"]
    if kind == "gemini":
        b = _normalize_gemini_base(api_base)
        url = f"{b}/models?key={api_key}" if api_key else f"{b}/models"
        return url, {"User-Agent": "Umi-OCR-AIOCR"}
    if kind == "ollama":
        b = _normalize_ollama_base(api_base)
        return f"{b}/tags", {"User-Agent": "Umi-OCR-AIOCR"}
    # OpenAI 兼容
    b = _normalize_openai_base(api_base)
    headers = {"User-Agent": "Umi-OCR-AIOCR"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return f"{b}/models", headers


def parse_model_list(provider, status_code, text):
    """解析模型列表响应，返回模型 ID 列表（失败抛异常）。"""
    if status_code == 401 or status_code == 403:
        raise Exception(f"鉴权失败（HTTP {status_code}），请检查 API 密钥")
    if status_code != 200:
        raise Exception(f"HTTP {status_code}: {text[:200]}")
    data = json.loads(text)
    models = []
    if isinstance(data, dict):
        if provider == "gemini":
            items = data.get("models", [])
            for it in items:
                if not isinstance(it, dict):
                    continue
                methods = it.get("supportedGenerationMethods") or []
                methods = [str(x).lower() for x in methods if x]
                if methods and "generatecontent" not in methods:
                    continue  # 仅保留支持 generateContent 的模型
                name = str(it.get("name", ""))
                if name.startswith("models/"):
                    name = name[len("models/"):]
                if name:
                    models.append(name)
        elif isinstance(data.get("data"), list):
            for it in data["data"]:
                mid = it.get("id") if isinstance(it, dict) else None
                if mid:
                    models.append(str(mid))
        elif isinstance(data.get("models"), list):
            for it in data["models"]:
                mid = it.get("name") or it.get("model") or it.get("id") if isinstance(it, dict) else None
                if mid:
                    models.append(str(mid))
    elif isinstance(data, list):
        for it in data:
            if isinstance(it, str):
                models.append(it)
            elif isinstance(it, dict):
                mid = it.get("id") or it.get("name") or it.get("model")
                if mid:
                    models.append(str(mid))
    # 去重，保持返回顺序
    seen, out = set(), []
    for m in models:
        if m and m not in seen:
            seen.add(m)
            out.append(m)
    if not out:
        raise Exception("响应中未找到模型列表")
    return out


def fetch_model_list(provider, api_base=None, api_key="", timeout=15, proxy_url=None):
    """拉取单个平台的模型列表。返回模型 ID 列表。"""
    rule = PROVIDER_LIST_RULES.get(provider)
    if rule is None:
        raise Exception(f"平台 {provider} 不支持在线获取模型列表")
    base = api_base or DEFAULT_API_BASES.get(provider, "")
    if not base:
        raise Exception("未配置 API 地址")
    url, headers = normalize_list_endpoint(provider, base, api_key)
    status, text = _http_get(url, headers=headers, timeout=timeout, proxy_url=proxy_url)
    return parse_model_list(provider, status, text)


def fetch_all_configured(providers=None, settings=None, timeout=15):
    """拉取全部已配置平台的模型列表并写入缓存。

    返回 {provider: {"models": [...], "ok": bool, "error": str, "name": str}}。
    - 云端平台：未填写 API 密钥时跳过；
    - 本地平台（Ollama/LM Studio/llama.cpp）：始终尝试（服务未启动则记为失败）。
    """
    if settings is None:
        settings = read_saved_ui_settings()
    proxy_url = settings.get("z_proxy_url", "") or None
    names = PROVIDER_DISPLAY_NAMES
    if providers is None:
        providers = [p for p, rule in PROVIDER_LIST_RULES.items() if rule]
    results = {}
    for p in providers:
        rule = PROVIDER_LIST_RULES.get(p)
        if not rule:
            continue
        api_key = settings.get(f"{p}_api_key", "") or ""
        default_base = DEFAULT_API_BASES.get(p, "")
        api_base = settings.get(f"{p}_api_base", "") or default_base
        # 用户改写过 API 地址（自建 / 反代 / 中转）或本地服务：无密钥也尝试拉取，
        # 否则自定义 OpenAI 兼容平台（本地反代通常不设密钥）会被误跳过
        base_is_custom = bool(default_base) and api_base.rstrip("/") != default_base.rstrip("/")
        if not api_key and p not in LOCAL_PROVIDERS and not base_is_custom:
            results[p] = {
                "models": [],
                "ok": False,
                "error": "未配置 API 密钥且未自定义 API 地址，已跳过",
                "name": names.get(p, p),
            }
            continue
        try:
            models = fetch_model_list(p, api_base, api_key, timeout=timeout, proxy_url=proxy_url)
            results[p] = {"models": models, "ok": True, "error": "", "name": names.get(p, p)}
        except Exception as e:
            results[p] = {"models": [], "ok": False, "error": str(e), "name": names.get(p, p)}
    save_model_list_cache(results)
    return results


# 服务商显示名（与 ai_ocr_config.optionsList 一致；冗余一份供脚本独立运行）
PROVIDER_DISPLAY_NAMES = {
    "openai": "OpenAI",
    "custom_openai": "自定义OpenAI兼容 (Custom)",
    "gemini": "Google Gemini",
    "xai": "xAI Grok",
    "openrouter": "OpenRouter",
    "siliconflow": "硅基流动 (SiliconFlow)",
    "doubao": "豆包 (Doubao)",
    "alibaba": "阿里云百炼 (Alibaba)",
    "zhipu": "智谱AI (Z.AI)",
    "glm_ocr": "GLM-OCR",
    "ollama": "Ollama (本地)",
    "lmstudio": "LM Studio (本地)",
    "llamacpp": "llama.cpp (本地)",
    "groq": "Groq",
    "hunyuan": "腾讯混元 (Hunyuan)",
    "mistral": "Mistral AI",
    "modelscope": "魔搭 (ModelScope)",
    "mimo": "小米MiMo",
    "intern": "浦源书生 (Intern)",
    "kimi": "Kimi (月之暗面)",
    "nvidia_nim": "NVIDIA NIM",
    "longcat": "Longcat AI",
    "agnes": "Agnes",
    "xflyun": "讯飞星辰 (MaaS)",
    "opencode_go": "OpenCode Go",
    "opencode_zen": "OpenCode Zen",
    "modelbest": "面壁智能 (ModelBest)",
}


# ============================================================
# =============== 命令行入口 ===============
# ============================================================

def _cli():
    args = sys.argv[1:]
    if "--list" in args:
        cache = load_model_list_cache()
        for p, models in cache.items():
            print(f"[{p}] {len(models)} 个模型")
            for m in models:
                print(f"  {m}")
        return 0
    providers = None
    if "--provider" in args:
        idx = args.index("--provider")
        providers = args[idx + 1:]
    print("正在读取 Umi-OCR 配置并拉取各平台模型列表...")
    results = fetch_all_configured(providers=providers)
    ok_num = 0
    for p, info in results.items():
        name = info.get("name", p)
        if info["ok"]:
            ok_num += 1
            print(f"[OK]   {name}: {len(info['models'])} 个模型")
        else:
            print(f"[SKIP] {name}: {info['error']}")
    print(f"\n完成：成功 {ok_num} / {len(results)}。缓存已写入：\n  {CACHE_PATH}\n请重启 Umi-OCR 使下拉菜单生效。")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
