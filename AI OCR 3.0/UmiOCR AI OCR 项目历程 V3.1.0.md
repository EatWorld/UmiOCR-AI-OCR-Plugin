# Umi-OCR AI OCR 插件 说明文档

> **插件目录**：`AIOCR 2/AI OCR 3.0/`
> **适用平台**：Umi-OCR v2.0+
> **当前版本**：v3.1.0
> **作者**：EatWorld
> **文档生成日期**：2026-07-03
> **最近更新**：2026-10-31

---

## 一、项目概览

本插件是 Umi-OCR 的扩展插件，将 **21+ 主流 AI 服务商** 的视觉模型接入 Umi-OCR 的 OCR 流程，作为离线 PaddleOCR 的强力补充。核心特色：

1. **多服务商统一接入**：内置 OpenAI、Gemini、阿里云百炼、智谱、豆包、Kimi、MinerU、PaddleOCR 在线等 25+ 服务商的适配器。
2. **双通道识别策略**：本地 PP-OCRv6 ONNX 检测器负责精确定位，云端 AI 负责高精度文字识别，二者结合实现"坐标精准 + 文字精准"。
3. **多输出格式**：纯文本、文字+坐标、Markdown 三种输出格式可切换。
4. **完全配置化**：所有服务商密钥/模型/地址/检测参数均通过 Umi-OCR 配置面板调节，无需改代码。
5. **本地离线支持**：Ollama、LM Studio、llama.cpp 三种本地推理方案，零网络依赖。

---

## 二、目录结构

```
AIOCR 2/
└── AI OCR 3.0/
    ├── __init__.py                # 插件入口：导出 Api 类与配置项
    ├── ai_ocr.py                  # 核心实现：Provider 适配器、Api 类、HTTP 客户端、模型列表拉取钩子
    ├── ai_ocr_config.py           # 配置定义：globalOptions / localOptions / PROVIDER_CONFIGS / 模型下拉生成
    ├── model_lists.py             # 模型列表模块（v3.1.0 新增）：精选列表 / 在线拉取 / .settings 读取 / 缓存
    ├── 刷新模型列表.bat            # 双击离线拉取各平台模型列表（v3.1.0 新增）
    ├── model_lists_cache.json     # 在线模型列表缓存（运行时生成，用户本地文件）
    ├── i18n.csv                   # 多语言翻译表（en / zh / zh-tw / ja）
    ├── README.md                  # 用户文档
    ├── .gitignore
    └── paddle_detector_v6/        # 本地文本检测器（PP-OCRv6 ONNX 实现）
        ├── __init__.py
        ├── detector.py            # 检测器 Api 类（仅检测，不识别）
        ├── ppocr_det.py           # DB 模型预处理 / 后处理（含行合并算法）
        ├── models/
        │   └── PP-OCRv6_det_small.onnx   # Small 检测模型（约 7.7MB）
        └── libs/                  # 内置依赖
            ├── onnxruntime/       # ONNX Runtime 推理库（含工具与算子）
            └── pyclipper/         # 多边形扩展库
```

> **说明**：`libs/onnxruntime/` 内置了完整的 ONNX Runtime 1.19.2 工具链（含 quantization、transformers、tools 等），保证检测器在用户机器上免安装即可运行。

---

## 三、插件入口

[__init__.py](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/__init__.py) 暴露 `PluginInfo` 字典，符合 Umi-OCR 插件规范：

```python
PluginInfo = {
    "group": "ocr",                       # 插件组别
    "global_options": globalOptions,      # 全局配置项（密钥、模型、超时等）
    "local_options": localOptions,        # 局部配置项（识别策略、输出格式、语言等）
    "api_class": Api,                     # OCR API 实现类
}
```

Umi-OCR 主程序读取该字典后：
- 在「设置 → OCR引擎」中渲染 `globalOptions` 与 `localOptions` 对应的 QML 控件；
- 实例化 `Api` 类，调用 `start()` / `runBase64()` / `stop()` 完成 OCR。

---

## 四、配置系统（ai_ocr_config.py）

### 4.1 服务商注册表 `PROVIDER_CONFIGS`

[ai_ocr_config.py#L10-L113](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/ai_ocr_config.py#L10-L113) 集中维护所有服务商的默认 `api_base` 与 `model`：

| Provider Key | 服务商 | 默认 API Base |
| --- | --- | --- |
| openai | OpenAI | https://api.openai.com/v1 |
| gemini | Google Gemini | https://generativelanguage.googleapis.com/v1beta |
| xai | xAI Grok | https://api.x.ai/v1 |
| openrouter | OpenRouter | https://openrouter.ai/api/v1 |
| siliconflow | 硅基流动 | https://api.siliconflow.cn/v1 |
| doubao | 豆包 | https://ark.cn-beijing.volces.com/api/v3 |
| alibaba | 阿里云百炼 | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| zhipu | 智谱 AI | https://open.bigmodel.cn/api/paas/v4 |
| glm_ocr | GLM-OCR | https://open.bigmodel.cn/api/paas/v4 |
| ollama / lmstudio / llamacpp | 本地服务 | http://localhost:11434 / 1234 / 8080 |
| groq | Groq | https://api.groq.com/openai/v1 |
| hunyuan | 腾讯混元 | https://tokenhub.tencentmaas.com/v1 |
| mistral | Mistral AI | https://api.mistral.ai/v1 |
| modelscope | 魔搭 | https://api-inference.modelscope.cn/v1 |
| mimo | 小米 MiMo | https://api.xiaomimimo.com/v1 |
| intern | 浦源书生 | https://chat.intern-ai.org.cn/api/v1 |
| kimi | Kimi（月之暗面） | https://api.moonshot.cn/v1 |
| nvidia_nim | NVIDIA NIM | https://integrate.api.nvidia.com/v1 |
| mineru | MinerU | https://mineru.net/api/v4 |
| paddle / paddle_vl_16 / pp_structure_v3 | 百度飞桨 OCR 系列 | https://paddleocr.aistudio-app.com |
| longcat | Longcat AI | https://api.longcat.chat/openai/v1 |

### 4.2 全局配置 `globalOptions`

按字段前缀排序，主要分组：

| 前缀 | 含义 |
| --- | --- |
| `a_prompt_*` | 三种模式的 Prompt 模板（纯文字 / 含坐标 / Markdown） |
| `a_provider` | 当前生效的 AI 服务商 |
| `a_timeout` | API 请求超时（5–120s，默认 30s） |
| `a_v6_detector_version` / `a_v6_model_size` | 双通道检测器版本与模型大小 |
| `<provider>_api_key` / `<provider>_model` / `<provider>_api_base` | 各服务商的密钥 / 模型 / 自定义地址 |
| `z_proxy_url` | 代理 URL（http/socks5） |
| `z_max_concurrent` | 批量并发上限（1–10，默认 3） |
| `z_rate_limit` | 每分钟最大请求数（令牌桶限速，0=不限制，默认 0） |

> **关键约定**：所有服务商配置都以 `<provider>_xxx` 命名，切换服务商时只需修改 `a_provider`，无需重输密钥。

### 4.3 局部配置 `localOptions`

控制单次识别行为：

- `a_l_provider`：当前 AI 服务商（默认空，跟随全局；非空则覆盖全局并联动同步）
- `dual_strategy`：识别策略
  - `ai_high_precision_with_coordinates`：**双通道：AI 高精度识别（含位置版）**（默认）
  - `ai_high_precision_text_only`：仅 AI 高精度识别（纯文本）
- `language`：识别语言（auto / zh / en / ja / ko / fr / de / es / ru / ar）
- `output_format`：输出格式（text_only / with_coordinates / markdown）
- `image_quality` / `max_image_size`：图像预处理参数
- 双通道性能参数：
  - `dual_limit_side_len`：检测器输入分辨率（320–4096px，默认 1440）
  - `paddle_timeout`：检测超时（5–120s，默认 20s）
  - `dual_max_boxes`：最大识别框数（1–500，默认 100）
  - `dual_min_area`：最小框面积过滤（0–50000 px²，默认 0）
  - `dual_max_workers`：并发识别数（1–20，默认 3）
  - `dual_crop_padding`：裁剪边缘补白（0–20px，默认 2）
- 平台专属选项：
  - MinerU：`mineru_enable_table` / `mineru_enable_formula`
  - Paddle 系列：`paddle_use_doc_unwarping` / `paddle_use_doc_orientation_classify` / `paddle_use_textline_orientation` / `paddle_use_layout_detection` / `paddle_use_chart_recognition` / `paddle_use_formula_recognition` / `paddle_use_seal_recognition` / `paddle_prettify_markdown` / `paddle_repetition_penalty` / `paddle_temperature` / `paddle_relevel_titles` / `paddle_merge_tables`

---

## 五、核心代码（ai_ocr.py）

文件分为三大部分：**Provider 适配器**、**HTTPClient**、**Api 主类**。

### 5.1 Provider 适配器

所有 Provider 继承自 [BaseProvider](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/ai_ocr.py#L34)，统一接口：

```python
class BaseProvider:
    def get_default_api_base(self) -> str
    def get_default_model(self) -> str
    def build_headers(self) -> dict
    def build_payload(self, image_base64, prompt) -> dict
    def parse_response(self, response_text) -> str | dict
    def rotate_key(self) -> str   # 多密钥池轮询（v3.0.6 新增，单密钥无副作用）
```

**Provider 一览**（共 28 个类，覆盖 31 家服务商）：

| 类名 | 适配服务商 | 备注 |
| --- | --- | --- |
| OpenAIProvider | OpenAI | OpenAI Chat Completions 协议 |
| GeminiProvider | Google Gemini | `generateContent` 接口，密钥放 URL 参数 |
| SiliconFlowProvider | 硅基流动 | OpenAI 兼容 |
| AlibabaProvider | 阿里云百炼 | OpenAI 兼容模式（v2.9.7b 优化速度） |
| DoubaoProvider | 豆包 | OpenAI 兼容，含 `thinking.disabled` |
| OpenRouterProvider | OpenRouter | 加 `HTTP-Referer` 与 `X-Title` 头 |
| XAIProvider | xAI Grok | OpenAI 兼容 |
| ZhipuProvider | 智谱 AI | OpenAI 兼容，禁用深度思考 |
| GLMOCRProvider | GLM-OCR | 智谱布局解析专用，支持 `words_result` 与 `layout_details` |
| MiMoProvider | 小米 MiMo | OpenAI 兼容 |
| ModelScopeProvider | 魔搭 | OpenAI 兼容 |
| OllamaProvider | Ollama | 本地，`/api/generate` 接口 |
| LMStudioProvider | LM Studio | OpenAI 兼容，本地 |
| LlamaCppProvider | llama.cpp | OpenAI 兼容，可选 API Key |
| GroqProvider | Groq | OpenAI 兼容，限制视觉模型白名单 |
| HunyuanProvider | 腾讯混元 | OpenAI 兼容 |
| MistralProvider | Mistral AI | 支持 `/chat/completions` 与 `/ocr` 双模式 |
| InternProvider | 浦源书生 | OpenAI 兼容 |
| KimiProvider | Kimi | OpenAI 兼容，支持自定义 Base URL |
| NvidiaNIMProvider | NVIDIA NIM | OpenAI 兼容，支持 202 异步轮询 |
| MinerUProvider | MinerU | 异步任务 + presigned PUT 上传 + zip 下载 |
| PaddleProvider | PaddleOCR（PP-OCRv6） | 异步任务 + jsonl 轮询 |
| PaddleVL16Provider | PaddleOCR-VL-1.6 | 异步任务 + layoutParsingResults |
| PPStructureV3Provider | PP-StructureV3 | 异步任务 + 版面解析 |
| LongcatProvider | Longcat AI | OpenAI 兼容 |
| AgnesProvider | Agnes | OpenAI 兼容（v3.0.3） |
| XFlyunProvider | 讯飞星辰 MaaS | OpenAI 兼容，xop 前缀模型名（v3.0.4） |
| ModelbestProvider | 面壁智能（ModelBest） | 文档解析专用：同步 /v1/document-parse 直出 + 大图异步 /v1/document-parse/jobs 轮询；返回页面 Markdown 与真实坐标块 ocr.blocks（v3.1.0） |

### 5.2 ProviderFactory

[ProviderFactory.create_provider](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/ai_ocr.py#L1457) 是工厂方法，根据 `provider_name` 实例化对应 Provider；若未提供 `api_base` 则使用 Provider 自身默认值，若未提供 `model` 则抛错（强制用户配置模型）。

### 5.3 HTTPClient

[HTTPClient](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/ai_ocr.py#L1506) 是基于 `urllib` 的轻量 HTTP 客户端：

- **Opener 复用**：`_get_opener()` 缓存 `urllib.request.build_opener()`，避免每次请求重新 TLS 握手，多 API 调用场景下显著提速；
- **代理支持**：支持 http/https/socks5 代理；
- **方法**：`get` / `post` / `put` / `request_bytes` / `get_bytes` / `post_multipart`（multipart 用于 PaddleOCR 上传图片与 MinerU presigned PUT）。

### 5.4 Api 主类

[Api](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/ai_ocr.py#L1868) 是 Umi-OCR 调用的入口，提供以下方法：

| 方法 | 作用 |
| --- | --- |
| `__init__(globalArgd)` | 读取全局配置，初始化变量 |
| `start(argd)` | 启动 API：解析局部配置、创建 Provider、创建线程池 |
| `stop()` | 关闭线程池、释放检测器 |
| `testConnection()` | 用测试图验证连接 |
| `runPath(imgPath)` / `runBytes(imageBytes)` / `runBase64(imageBase64)` | 三种图片输入入口 |
| `_preprocess_image(image_base64)` | 图像预处理：RGB 转换、按 `max_image_size` 等比缩放、JPEG 重编码 |
| `_run_ocr(image_base64, config)` | 单次 OCR：构建 Prompt → 发送请求 → 解析响应 |
| `_build_prompt(config)` | 按输出格式选择 Prompt 模板，自动追加"禁止繁简转换"约束 |
| `_send_request(image_base64, prompt)` | 路由到各 Provider 专属发送方法（含 MinerU / GLM-OCR / Paddle / NVIDIA NIM 异步） |
| `_send_paddle_async_request` | PaddleOCR 异步任务：提交 → 轮询 → 下载 jsonl → 合并 |
| `_send_mineru_request` | MinerU 流程：申请上传链接 → PUT 上传 → 轮询 → 下载 zip → 提取 `full.md` |
| `_send_nvidia_nim_request` | NVIDIA NIM：200 直返或 202 异步轮询 |
| `_send_glm_ocr_request` | GLM-OCR：根据输出格式调用 `/layout_parsing` 或 `/ocr` |
| `_run_paddle_first_correction` | **双通道主流程**（详见下一节） |
| `_match_ai_text_to_paddle_boxes` | 将 AI 文本行按从上到下顺序匹配到 Paddle 检测框 |
| `_recognize_lines_by_cropping` | 逐框裁剪 + 并发 AI 识别（双通道兜底回退路径） |
| `_convert_to_umi_format` | 按 `output_format` 转换为 Umi-OCR 标准结构 |
| `_parse_text_only` / `_parse_text_with_coordinates` / `_parse_markdown` | 三种输出格式解析器 |
| `_map_coordinates_to_original` | 将归一化/缩放后坐标映射回原图尺寸，统一输出四点多边形 |
| `_generate_estimated_boxes` | 纯文本模式生成估算边界框（用于 Umi-OCR 文本对齐显示） |
| `_sanitize_ocr_result` | 统一去除结果中的 `#` 符号（除非 Markdown 模式） |

---

## 六、双通道识别策略

### 6.1 设计动机

大模型 OCR 精度高，但**坐标信息不可靠**（大模型对像素位置的感知很弱）；本地 PaddleOCR 检测精准但**识别精度有限**。双通道将两者解耦：

- **本地检测**：PP-OCRv6 ONNX 仅做文本块定位，输出准确四点坐标；
- **云端识别**：将检测框坐标作为参考上下文喂给 AI，由 AI 按顺序输出每行文字；
- **结果合成**：AI 文本 + Paddle 坐标，按行 1:1 对齐。

### 6.2 主流程（`_run_paddle_first_correction`）

[ai_ocr.py#L2288-L2537](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/ai_ocr.py#L2288-L2537)：

```
1. _ensure_paddle_detector()                    # 懒加载本地检测器
2. detector.runBase64(image_base64)             # 本地检测，含超时回退
   ├── 超时 → 直接走 _run_ocr（AI 直出）
   └── 成功 → 得到检测框列表
3. 过滤 & 排序：
   - 按 _bounds_from_box 计算边界
   - 按 min_area 过滤小框
   - 按 center_y 升序排列（从上到下阅读顺序）
   - 截断到 max_boxes
4. 分支：若 provider 是 Paddle 在线服务
   └── 整图调用一次 Paddle 在线 API → 按行序号匹配到本地框
5. 通用分支（其他 AI 服务商）：
   - 构建上下文 JSON（仅 boxes，不传 Paddle 识别文本）
   - 构建纠错 Prompt：禁止繁简转换 + 按行输出
   - _send_request → provider.parse_response
   - 解析为纯文本行 ai_lines
6. 行数对齐校验（bad_alignment）：
   - ai_lines 为空 / 行数 < filtered / 行数 > 1.2×filtered / 单行≥160字且≥8行
   - 触发 → 先尝试 AI 整图含坐标识别 + _match_ai_text_to_paddle_boxes
   - 仍失败 → 逐框裁剪 _recognize_lines_by_cropping
7. 兜底回退：
   - AI 纠错为空 → AI 直出（含坐标 / 纯文本）→ 匹配 Paddle 框
   - 再失败 → 逐框裁剪识别
8. 组装输出：{text, box, score}（坐标始终来自 Paddle，文本仅来自 AI）
```

> **关键约束**（来自项目记忆）：检测器**只负责定位**，识别文本**完全交由 AI**，AI 未识别到时返回空文本，**绝不回退到 Paddle 的识别文本**，避免遮蔽 AI 的高精度结果。

### 6.3 行合并算法

[ppocr_det.py#L184-L280](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/paddle_detector_v6/ppocr_det.py#L184-L280) `merge_boxes_into_lines` 改进了原版贪心分组：

1. 每个框遍历**所有**已有行，选择 y 中心差异最小的行归入（而非只与"当前行"比较），避免排序错误导致的级联误差；
2. 同行判定阈值用 `min(box_h, line_h) * merge_y_ratio`，比滑动均值更稳定；
3. x 方向间距检查：`x_gap > 5 × line_h` 时不合并，避免跨列误合；
4. 合并后取最小外接矩形作为行框。

### 6.4 检测器懒加载

`_ensure_paddle_detector` 根据 `a_v6_detector_version` 选择加载路径：

- **v6_onnx**（默认推荐）：调用 `_load_v6_detector`，动态导入 `paddle_detector_v6/detector.py`，加载 `models/PP-OCRv6_det_{tiny,small,medium}.onnx`；
- **v3_legacy**：调用 `_load_v3_detector`，在 `plugins_root` 下查找 `PaddleOCR-json/PPOCR_umi.py` 作为兼容回退。

模型文件命名映射：

| `a_v6_model_size` | 文件名 | 大小 |
| --- | --- | --- |
| tiny | PP-OCRv6_det_tiny.onnx | ~1.5 MB |
| small | PP-OCRv6_det_small.onnx | ~7.7 MB |
| medium | PP-OCRv6_det_medium.onnx | ~34.5 MB |

---

## 七、本地检测器（paddle_detector_v6）

### 7.1 [detector.py](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/paddle_detector_v6/detector.py)

封装 PP-OCRv6 DB 检测模型，接口与旧版 `PPOCR_umi.py` 完全兼容：

```python
class Api:
    def __init__(self, globalArgd)
    def start(self, argd) -> str          # "" 成功，"[Error] xxx" 失败
    def stop(self)
    def runPath(self, imgPath) -> dict
    def runBytes(self, imageBytes) -> dict
    def runBase64(self, imageBase64) -> dict
```

返回结构（**不含 text 字段**，仅检测）：

```python
{"code": 100, "data": [{"box": [[x,y],...], "score": float}, ...]}
```

关键参数（来自 `globalArgd` 与 `argd`）：

| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `limit_side_len` | 960（detector 内部） / 1440（插件局部配置） | 输入图像长边上限 |
| `det_thresh` | 0.3 | 二值化阈值 |
| `det_box_thresh` | 0.5 | 框内分数阈值 |
| `det_unclip_ratio` | 1.5 | 框扩展系数 |
| `merge_into_lines` | True | 是否合并相邻框为行 |
| `merge_y_ratio` | 0.5 | 行合并 y 中心阈值比例 |
| `cpu_threads` | `os.cpu_count()` | ONNX Runtime 线程数 |

> **来自项目记忆的最佳实践**：双通道模式下推荐 `box_thresh=0.5`、`det_thresh=0.3`、`unclip_ratio=1.5`、`merge_y_ratio=0.5`、`limit_side_len=1440`、补白 100px 防止边缘小字漏检。

### 7.2 [ppocr_det.py](file:///a:/Umi%20OCR/Umi-OCR_Paddle_v2.1.5/UmiOCR-data/plugins/UmiOCR-AI-OCR-Plugin-main%202/AIOCR%202/AI%20OCR%203.0/paddle_detector_v6/ppocr_det.py)

- **DBPreProcess**：等比缩放 → pad 到 32 倍数 → ImageNet 归一化 → HWC 转 CHW → 加 batch 维度；
- **DBPostProcess**：从概率图二值化 → `cv2.findContours` 找轮廓 → `get_mini_boxes` 取最小外接矩形 → `box_score_fast` 计算框内分数 → `unclip` 用 pyclipper 扩展框 → `merge_boxes_into_lines` 合并同行框。

---

## 八、调用流程总览

### 8.1 启动流程

```
Umi-OCR 启动
   ↓
读取插件 __init__.py → PluginInfo
   ↓
渲染 globalOptions / localOptions 配置面板
   ↓
用户点击"应用修改"
   ↓
Api.__init__(globalArgd)       # 保存全局配置
   ↓
Api.start(localArgd)           # 创建 Provider / HTTPClient / 线程池
   ↓
返回 "" 表示启动成功
```

### 8.2 单张图片识别流程

```
Umi-OCR 调用 Api.runPath / runBytes / runBase64
   ↓
runBase64(imageBase64)
   ↓
读取 dual_strategy 与 output_format
   ↓
┌──────────────────────────────────────────────────────┐
│ 分支 A：strategy = ai_high_precision_with_coordinates │
│  → _run_paddle_first_correction（双通道，详见 §6.2）  │
├──────────────────────────────────────────────────────┤
│ 分支 B：strategy = ai_high_precision_text_only        │
│  → _preprocess_image → _run_ocr（整图 AI 识别）       │
├──────────────────────────────────────────────────────┤
│ 分支 C：output_format=markdown & provider=paddle_vl   │
│  → _preprocess_image → _run_ocr（Paddle 原生 Markdown）│
└──────────────────────────────────────────────────────┘
   ↓
_sanitize_ocr_result（去 # 符号，非 Markdown 模式）
   ↓
返回 {"code": 100, "data": [{"text", "box", "score"}, ...]}
```

### 8.3 异步任务流程（PaddleOCR / MinerU / NVIDIA NIM）

以 PaddleOCR 为例：

```
1. POST /api/v2/ocr/jobs (multipart 上传图片)
   ↓ 返回 jobId
2. 轮询 GET /api/v2/ocr/jobs/{jobId}
   间隔 [2.0, 3.0, 5.0]s 退避
   ↓ state=done → 拿到 resultUrl.jsonUrl
3. GET jsonUrl → 下载 jsonl
   ↓
4. 逐行解析 → 合并 ocrResults / layoutParsingResults
   ↓
5. 包装成同步响应格式返回
```

---

## 九、国际化（i18n.csv）

CSV 格式，5 列对应 5 种语言：

| key | en | zh | zh-tw | ja |
| --- | --- | --- | --- | --- |

由 `plugin_i18n.Translator(__file__, "i18n.csv")` 加载，所有配置项标题与提示均通过 `tr()` 包裹，支持中英日繁简切换。

---

## 十、关键工程约定（来自项目记忆）

| 约定 | 说明 |
| --- | --- |
| 双通道坐标对齐 | 双通道模式下坐标必须使用本地 Paddle 检测结果，AI 仅提供文本 |
| 检测器参数全开放 | `box_thresh` / `merge_y_ratio` / `det_thresh` / `unclip_ratio` 必须可在设置面板调节 |
| 检测器热重载 | 参数变化时检测器需重新加载（通过 `start()` 重建 session） |
| Paddle 在线整图识别 | 在线 API 必须整图调用，禁止裁剪小图逐个发送（小图导致版面分析模型返回空） |
| 边缘补白防漏检 | PP-OCRv6 DB 模型边缘检测弱，需自适应 padding（目标 100px） |
| 不遮蔽 AI 结果 | AI 识别失败的行返回空文本，不回退到 Paddle 识别文本 |
| 禁止繁简转换 | 中文场景在 Prompt 中明确禁止繁简/全角半角/字符归一化转换 |
| 服务商配置可切换 | 所有 `<provider>_api_key` / `_model` / `_api_base` 独立保存，切换不丢失 |
| 限速只限提交不限轮询 | 令牌桶作用于真正的 API 提交请求，Paddle/MinerU/NIM 的任务轮询 GET 不受限 |
| 多密钥零侵入轮询 | 密钥池在 `BaseProvider` 层解析分隔符并轮询 `rotate_key()`，单密钥时零副作用 |

---

## 十一、项目历程（开发与优化历程）

> 📌 **维护约定（重要）**：本节记录插件历次开发与优化历程。**以后每次优化和更新都必须同步更新本 md**——新增版本条目时，需在「11.2 版本演进速览」表格顶部追加一行，并在「11.3 历次开发与优化详情」中按时间倒序补充该版本的变更说明（含动机、改动点、影响范围）；同时更新文档头部的「当前版本」与「最近更新」日期，并将本文件名中的版本号同步改为最新版本（格式：`UmiOCR AI OCR 项目历程 V<版本号>.md`）。

### 11.1 历程主线

本插件自 v1.0.0 起步，历经四大里程碑演进：

1. **单厂商阶段（v1.x）**：以 Gemini OCR 为起点，验证 AI 视觉模型接入 Umi-OCR 的可行性。
2. **多厂商重构（v2.0–v2.5）**：重构为多厂商架构，陆续接入 10+ 云端服务商与本地离线服务，确立"一次配置、按需切换"的配置约定。
3. **双通道突破（v2.6–v2.9）**：首创双通道识别策略，本地 PaddleOCR 负责精准定位、云端 AI 负责高精度识别，彻底解决大模型 OCR 文字对齐难题；并持续优化 Prompt、异步解析、Markdown 输出等能力。
4. **双通道升级与生态扩展（v3.0+）**：将本地检测模块从 C++ PP-OCRv3 升级为 ONNX PP-OCRv6，检测器仅定位不识别，识别完全交由 AI；持续扩展服务商生态（腾讯混元、Agnes、讯飞星辰等）。

### 11.2 版本演进速览

| 版本 | 关键变更 |
| --- | --- |
| v3.1.0 | 🚀 新增面壁智能（ModelBest）文档解析平台（MiniCPM-OCR-1.0）；全局设置"模型"字段升级为可在线拉取的下拉菜单（model_lists.py）；修复 i18n 表头异常致 zh/ja 回落英文；刷新各平台建议模型 |
| v3.0.8 | ✨ 新增 OpenCode Go 与 OpenCode Zen 平台（均为 OpenAI 兼容网关，新增 opencode_go / opencode_zen 服务商） |
| v3.0.7 | ✨ 新增「自定义OpenAI兼容 (Custom)」服务商（#35）+ 修复 i18n.csv 空行导致翻译表加载失败 |
| v3.0.6 | 🚀 令牌桶限速（主动避免429，#12）+ API密钥池轮询（#12）+ Linux检测器不可用时回退AI直出（#28） |
| v3.0.5 | 修正讯飞星辰模型名为 xop 前缀格式（`xoppaddleocrv16`、`xophunyuanocr`） |
| v3.0.4 | 新增讯飞星辰（MaaS）平台支持 |
| v3.0.3 | 新增 Agnes 平台支持 |
| v3.0.0 | 🚀 双通道检测模块从 PP-OCRv3（C++）升级为 PP-OCRv6（ONNX）；检测器仅定位不识别；新增腾讯混元；移除无问芯穹 |
| v2.9.9 | 局部配置新增"当前 AI 服务商"快捷切换 |
| v2.9.8 | 百度 PaddleOCR 默认模型从 PP-OCRv5 升级至 PP-OCRv6 |
| v2.9.7b | 阿里云百炼改用 OpenAI 兼容模式；HTTPClient 复用 opener |
| v2.9.7a | 修复 NVIDIA NIM `_get_ocr_prompt` 报错 |
| v2.9.7 | 新增 Markdown 输出；新增 llama.cpp；Ollama 地址可自定义 |
| v2.9.6 | PaddleOCR-VL 升级至 1.6；全面废弃同步解析 |
| v2.9.5 | 新增 Kimi / NVIDIA NIM / Longcat；Paddle 系列切换异步 |
| v2.9.4 | LM Studio 自定义地址；新增小米 MiMo；暴露 Prompt 窗口 |
| v2.9.3 | Paddle / MinerU 功能开关；Markdown 输出去除 `#` |
| v2.9.2 | 新增 GLM-OCR、MinerU；默认关闭"深度思考" |
| v2.9.1 | 新增 PaddleOCR-VL-1.5 |
| v2.9.0 | 新增 PP-StructureV3 版面解析 |
| v2.8.0 | 新增 PaddleOCR-V5 及 PaddleOCR-VL |
| v2.7.0 | 调整双通道策略，精度与速度提升 |
| v2.6.0 | 🚀 双通道识别首发：解决大模型 OCR 文字对齐问题 |
| v2.5.0 | 🎉 社区贡献：新增 Groq / 魔搭 / Mistral / 浦源书生 |
| v2.4.0 | 🚀 新增本地离线识别（Ollama / LM Studio） |
| v2.3.0 | 新增阿里云百炼、智谱 AI；移除重试次数配置 |
| v2.2.0 | 支持一次性配置所有服务商，切换不丢失密钥 |
| v2.1.0 | 新增硅基流动、豆包视觉模型 |
| v2.0.0 | 重构为多厂商架构（OpenAI / Gemini / xAI / OpenRouter） |
| v1.2.0 | 支持 Gemini 2.5 Flash/Pro 预览版，优化精度 |
| v1.1.0 | 增加多语言支持，优化错误处理 |
| v1.0.0 | 初始版本，支持 Gemini OCR 功能 |

### 11.3 历次开发与优化详情

> 以下按版本倒序记录每次开发与优化的动机、改动与影响。

#### v3.1.0（2026-10）—— 🚀 面壁智能平台 + 模型下拉菜单与在线列表获取
**一、新增面壁智能（ModelBest）平台支持**
- **动机**：面壁智能推出新一代在线文档解析模型 MiniCPM-OCR-1.0（platform.modelbest.ai），可识别文字、表格、公式、印章与版面并返回坐标，与插件的文档解析类平台（MinerU/Paddle VL）定位一致。
- **接口**（官方 Document Parsing API）：
  - 同步：`POST {base}/v1/document-parse`，JSON `{"model", "image"(base64/dataURI), "upright", "recognize_seal"}`，单图直出（JSON body ≤32MiB）；
  - 异步：`POST {base}/v1/document-parse/jobs`（multipart），HTTP 202 返回 `{id: "ocr_...", status}`；轮询 `GET .../jobs/{id}`（1~2s，终态 Success/Failed/Cancelled）；原始图 >20MiB 时自动切换异步（base64 膨胀逼近 32MiB 上限），400/413 也回退异步重试；
  - 响应：`choices[0].message.content` = 页面 Markdown（表格 HTML、公式 LaTeX）；`ocr.blocks[]` = `{order, label, bbox[x1,y1,x2,y2], content, status}` 真实坐标块，`ocr.image_width/height` 为坐标系尺寸。
- **实现**（`ModelbestProvider` + `Api._send_modelbest_request`）：
  - parse_response 返回归一化页面字典 `{"__modelbest__": page}`（不落实例状态，多图并发线程安全）；
  - `_convert_modelbest_page` 按输出格式分发：markdown → 整页 Markdown；text_only / with_coordinates → `_parse_modelbest_blocks` 直接消费真实坐标块（按 order 排序、跳过 failed/skipped 块、bbox 先线性归一到发送图坐标系再经 `_map_coordinates_to_original` 映射回原图）；
  - `runBase64` 中 modelbest 走原生路径：含坐标策略不再经过本地检测+裁剪（文档解析自带块坐标），markdown 直出；
  - 鉴权 Bearer MAP API Key；默认地址 `https://api.modelbest.ai`；默认模型 `MiniCPM-OCR-1.0`；
  - 局部设置新增「文档自适应旋转」（默认开，精确坐标建议关）与「印章内容识别」（默认开）。

**二、全局设置"模型"字段升级为下拉菜单 + 在线获取模型列表**
- **动机**：各平台模型迭代快，手填模型名易错易旧；希望像"当前AI服务商"一样下拉选择，且能自动获得平台最新模型列表，同时不破坏手动输入与旧配置兼容。
- **Umi-OCR 配置系统约束**（逆向确认）：插件配置字典在启动时一次性传入 QML，枚举项候选列表静态；**枚举校验会把不在候选内的已存值重置为默认**——因此直接把模型字段改成枚举会丢用户配置。
- **方案**（`model_lists.py` + 配置生成 + 拉取钩子三层）：
  1. `model_lists.py` 新模块：内置精选列表 `MODEL_CURATED_LISTS`；`read_saved_ui_settings()` 解析 `UmiOCR-data/.settings`（QSettings INI 反转义，提取 `ocr.AIOCR.*` 短键名）；`build_model_options()` 合成候选 = 精选 + 在线缓存 + 已存值（原样+strip 双份兜底）+「自定义」；缓存文件 `model_lists_cache.json`；
  2. `ai_ocr_config.py` 导入时执行 `_upgrade_model_items_to_dropdown()`：把各平台 `{p}_model` 文本项原地转为枚举（移除显式 type:"text"，否则 QML 不按枚举渲染），默认值不在候选内时修正，并自动生成 `{p}_model_custom` 手填框（advanced，QVariantMap 字母序天然紧跟 model 项）；
  3. `Api.start()` 模型解析：`__custom__` → 取 `{p}_model_custom`（空则回退平台默认）；旧手填值原样透传，完全向后兼容；
  4. **在线拉取**：地址归一化与调用规则一致——Gemini（含 generativelanguage.googleapis.com）从裸 base、`/models`、完整 `:generateContent` 端点归一到列表端点并过滤 `supportedGenerationMethods` 含 generateContent 的模型；Ollama（/api 结尾或 :11434）走 `/api/tags` 无需密钥；其余 OpenAI 兼容 `GET {base}/models`（Bearer，容许 /chat/completions 后缀；裸域名如面壁智能自动补 /v1）；
  5. **按钮热刷新**（核心无侵入）：插件导入时检测核心 Configs.qml 是否支持"按钮 onClicked 字符串 → callPy"分发，且把 `aioFetchModels` / `aioFetchAllModels` 猴子补丁挂载到核心 `MissionOCR`（callPy 以 `method(*args)` 调用实例属性函数，无自动绑定，故为无参函数）；后台线程拉取后经主线程 QObject 通知器（QMetaObject.invokeMethod 队列回主线程）弹窗汇总，并重赋 `configDict.ocr` + 发布 `<<settingsReload>>` 实现下拉菜单即时刷新；核心不支持时按钮不渲染，用户可用 `刷新模型列表.bat`（调用 Umi-OCR 自带 runtime/python.exe 运行 `model_lists.py`）离线拉取，重启后生效。

**四、下拉弹层与枚举匹配补丁（核心 Configs.qml，维护者本地安装；原版核心不受影响）**
- **动机**：v3.1.0 模型下拉菜单上线后暴露三个 UI 问题——①候选项含首尾换行/空白的历史残值会把 ComboBox 文字撑成两行、与相邻行重叠（截图实锤：百炼残值 `qwen3-vl-235b-a22b-instructqwe n3.7-plus
`）；②候选上百条时弹层不限高，体验差；③Qt 默认滚动条极细，点不到也拖不动；④"自定义（手动输入）"的真实输入框随「高级」隐藏，指引不显眼。
- **核心补丁**（Configs.qml，改前备份 `Configs.qml.bak_v3.1.0`）：
  1. `initConfigDict` 枚举校验增加宽容匹配：精确匹配失败且值为字符串时，用 `trim()` 后的值再匹配一次，命中则采用去空白值——历史残值不重置、显示与调用均为干净值；
  2. `compEnum` 的 ComboBox 增加 `popup` 定义：高度上限约 12 行（`size_.line * 12`）、`margins: 4` 使底部空间不足时自动上翻、`ListView + ScrollBar.vertical(AlwaysOn, 宽14, 可点击拖动)`；
  3. 候选项 delegate 高度随内容自适应，长模型名 `wrapMode: WrapAnywhere` 自动折行（用户反馈"缺少换行"：弹层不再把长名挤成一行）；收起状态的选中值 `elide: ElideMiddle` 中间省略，不再撑出行外。
- **插件侧配套**：`build_model_options()` 合并已存值时统一去首尾空白后再入列（不再"原样+去空白"双份入列，消除弹层中两个视觉相同的候选）；含内部换行/制表的残值不入列（首枚举校验失败自动回退默认值，残值自愈）；每个平台「模型」下拉框悬停提示末尾追加自定义手填指引（含「高级」开关说明），对应新增 i18n 词条。
- **README**：「1.5 模型下拉菜单与在线获取」新增「★ 如何手填自定义模型（详细步骤，必读）」与「弹层与滚动条」小节。

**三、其他修复与刷新**
- 修复 i18n.csv 首行为 Excel 误存垃圾表头导致 Translator 语言索引失效：简体中文（langCode="zh"）与日语界面一直回落到英文列；去除垃圾行后 zh/en/zh-tw/ja 全部正确索引。
- 刷新各平台建议模型：硅基流动 Qwen2.5-VL 全系 / Qwen3-VL-235B / PaddleOCR-VL(1.0) 已于 2026-04 下线，改为 PaddlePaddle/PaddleOCR-VL-1.5（免费）与 Qwen3-VL-32B 等；豆包默认改 doubao-seed-2-0-pro；OpenRouter 免费视觉模型更新（kimi-k2.6:free、nemotron-3.5-super-vl:free 等）。
- 修复 llama.cpp 无密钥被误报「API密钥不能为空」（与配置项"可留空"说明一致）。

**五、模型列表获取修正与自动补拉（v3.1.0 追加，用户实测反馈）**
- **问题**：用户使用自定义 OpenAI 兼容平台（本地反代 `http://127.0.0.1:3066/v1`，其他 AI 软件均可用）却拉不到模型列表，怀疑下拉是纯内置列表而非实时获取。根因：`fetch_all_configured` 的跳过门槛只放行"有密钥或本地三平台"，`custom_openai` 无密钥（本地反代通常不设密钥）被误跳过——端点本身实测正常（GET /v1/models 返回 56 个模型）。
- **修正**：跳过门槛改为"有密钥 OR 本地平台 OR **API 地址被用户改写过**（自建/反代/中转，无密钥也尝试）"；跳过提示改为"未配置 API 密钥且未自定义 API 地址"。
- **自动补拉**：新增 `_auto_fetch_missing_models()`——首次「应用修改」某平台时后台补拉一次其在线模型列表（已有缓存的平台不打扰；失败静默，每平台每进程仅一次），拉取成功经通知器弹窗并热刷新下拉菜单。`_notify_fetch`/`_refresh_dropdowns` 由 `_aio_fetch_async` 内部闭包提升为模块级 `_aio_notify_fetch`/`_aio_refresh_dropdowns` 供复用。
- **验证**：实测无密钥拉取用户反代成功（56 模型入缓存并合并进「自定义OpenAI兼容」下拉，57 个候选）；回归 47/47。

**六、热刷新空转修复 + 在线列表强制优先 + 书生平台域名变更（v3.1.0 追加）**
- **热刷新空转（关键修复）**：最小 QML 环境实测证实——QML `property var` 从 Python 侧链式赋值（`gc.configDict.ocr = ...`）直接抛 AttributeError（对象属性须以 property() 访问，var 值包装为 QJSValue），异常被吞导致此前的"热刷新"完全是空操作，下拉菜单只能靠重启更新。修复：`refreshDropdowns` 改为 `gc.property("configDict").toVariant()` → 更新 ocr 键 → `gc.setProperty("configDict", 整表)` 写回 → `qmlapp.property("pubSub").publish_("<<settingsReload>>")`；notify 弹窗同样改经 property() 取 popup 对象；`_capture_qmlapp` 改用 `metaObject().indexOfProperty()` 判存在（对象型 var 属性取值行为跨版本不稳，元对象查询最稳）。全部机制先经最小 QML 环境（QGuiApplication + engine.load 内存 QML）逐项验证。
- **在线列表强制优先**：`build_model_options` 改为——已成功拉取在线列表的平台，候选仅由"在线列表 + 已存值 + 自定义"组成，**不再混入内置精选**；未拉取过的平台以内置精选 + 默认值引导（首次应用自动补拉后热刷新替换为纯在线列表）。`_upgrade_model_items_to_dropdown` 重构为可重入的 `rebuild_model_options()`（热刷新复用；指引追加用进程内标记防重——tr 译文随语言变化，文本标记在非中文语言下会失效导致重复追加）。
- **缓存并发写坏（连带发现）**：测试中多个自动补拉线程并发"读-合并-写" `model_lists_cache.json`，读到半截文件 JSON 解析失败后以空表覆盖，全量缓存被清空。修复：`save_model_list_cache` 全程持 `_CACHE_LOCK`（RLock）+ 临时文件 `os.replace` 原子替换。
- **书生平台域名变更**：API 地址更新为 `https://discovery-api.intern-ai.org.cn/v1`（2026-10 起启用，旧地址停用）；新增「浦源书生 API地址」高级配置项；文档与提示注明 RPM 限额（生成模型 50 次/分钟、决策模型 200 次/分钟，所有 Key 共享额度），建议配合"每分钟最大请求数"≈40；精选列表更新为 intern-latest / intern-s2-preview / intern-s1-pro / internvl3.5-241b-a28b。

### 七、发布记录（v3.1.0）
- **发布版本**：v3.1.0（`PluginInfo` 新增 `version: "v3.1.0"` 字段，便于日志排查）。
- **发布内容**：本文第 11.3 节 v3.1.0 条目全部内容——面壁智能（ModelBest）平台、模型下拉菜单与在线获取（在线列表强制优先 / 自定义地址免密钥拉取 / 首次应用自动补拉 / 热刷新修复 / 缓存并发写保护）、书生平台域名变更与 RPM 限额、核心界面补丁（弹层限高/滚动条/折行/省略/枚举宽容匹配）、i18n 表头修复、各平台建议模型刷新、llama.cpp 免密钥修复。
- **用户实测确认**（2026-10-31）：全部平台在线拉取正常；自定义 OpenAI 兼容反代（`http://127.0.0.1:3066/v1`）实拉 56 个模型；书生新域名实拉 13 个模型（旧密钥在新域名失效，更换新密钥后恢复——迁移提示已写入 README）。
- **随版本文件**：`model_lists.py`（新增）、`刷新模型列表.bat`（新增）、`ai_ocr.py` / `ai_ocr_config.py` / `i18n.csv` / `README.md` / `__init__.py`（更新）。
- **注意**：核心界面补丁（Configs.qml：弹层限高/加宽滚动条/长名折行/中间省略/枚举宽容匹配）**不随插件分发**，仅维护者本地安装（改前备份 `Configs.qml.bak_v3.1.0`）；原版 Umi-OCR 用户功能完整可用，仅下拉弹层为 Qt 默认样式。

#### v3.0.8（2026-08）—— ✨ 新增 OpenCode Go 与 OpenCode Zen 平台
- **动机**：社区希望接入 OpenCode 提供的 Go（低价订阅网关）与 Zen（按量付费 AI 网关）模型，二者均提供 OpenAI 兼容的 `chat/completions` 接口。
- **改动**：
  1. `PROVIDER_CONFIGS` 新增 `opencode_go`（`https://opencode.ai/zen/go/v1`）与 `opencode_zen`（`https://opencode.ai/zen/v1`）；
  2. 全局/局部服务商下拉框新增「OpenCode Go」「OpenCode Zen」选项；
  3. 新增对应 `api_key` / `model` / `api_base`（高级）配置项，默认模型 `grok-4.5` / `kimi-k3`（均为视觉模型）；
  4. `ProviderFactory` 将二者映射到 `OpenAIProvider`，复用 OpenAI 兼容请求/解析逻辑；默认请求地址为 `{api_base}/chat/completions`。
- **注意**：仅 chat/completions 接口的模型可用于 OCR；GPT/Claude/Gemini 等走 responses/messages 接口的模型暂不支持，需选择支持图像输入的视觉模型。
- **影响**：用户可直接在设置中填写 OpenCode 的 API 密钥与模型名即可使用其网关下的视觉模型，无需改动代码。

#### v3.0.7（2026-08）—— ✨ 新增「自定义OpenAI兼容 (Custom)」服务商（#35）
- **动机**：社区建议 #35 希望支持任意 OpenAI 兼容的 API 地址，便于接入 vLLM、One API、new-api 中转、自建服务等。
- **改动**：新增 `custom_openai` 服务商，可填写任意 OpenAI 兼容 API 地址（默认 `https://api.openai.com/v1`），请求发送至 `{地址}/chat/completions`，API 密钥与模型名均可自定义；修复 i18n.csv 空行导致翻译表加载失败的问题。
- **影响**：极大扩展可接入的模型范围，私有化/中转部署场景开箱即用。

#### v3.0.6（2026-08）—— 🚀 令牌桶限速、API 密钥池与 Linux 检测器回退（#12 / #28）
- **动机**：GitHub issue #12（taozhe6）指出：现有并发控制（`max_concurrent`）只能限制"同时"请求数，无法控制"单位时间"请求总数；单请求处理极快时仍可能在短时间内超出服务商频率限制（如 60 次/分钟）触发 429；另建议多账号分摊配额。GitHub issue #28（crazyn2）反馈：Linux（Fedora 42）下 OCR 返回空且 Ollama 从未被调用——根因是双通道模式的本地检测器（内置 ONNX Runtime / pyclipper 库与旧版 PaddleOCR-json.exe）均为 Windows 专属二进制，`_ensure_paddle_detector()` 加载失败后直接返回 `code 101`，导致 AI 完全未参与识别。
- **改动**：
  1. 新增线程安全的 `TokenBucket` 令牌桶限速器：按恒定速率补充令牌、桶容量封顶，支持短时突发同时严格保证长期平均速率；新增全局配置 `z_rate_limit`（每分钟最大请求数，0=不限制，默认 0，建议设为服务商限额的 80%）；
  2. 限速接入点：`_send_request` 中所有"提交类"API 请求前阻塞获取令牌（含 Paddle / MinerU / NVIDIA NIM 的异步任务提交）；**不限制任务轮询 GET**，避免拖慢识别；
  3. 429 重试增强：`_run_ocr` 重试时识别 429/Too Many Requests 错误并指数退避（5s→10s→20s→上限 30s），其他错误按次数递增等待（原固定 1s）；
  4. 新增 API 密钥池：`BaseProvider` 解析 `api_key` 字段中的逗号/分号/换行分隔符，自动维护多密钥列表并轮询切换（`rotate_key()`，每次请求前调用）；单密钥零副作用，全部现有 Provider 无需改动（api_key 全部经 `self.api_key` 属性使用）；
  5. **Linux/macOS 检测器回退**：`_run_paddle_first_correction` 中检测器加载失败/返回无效/异常三种情况全部回退到 AI 直出（`_run_ocr`），不再直接返回 `code 101`；非 Windows 平台在 `_ensure_paddle_detector` 中给出明确提示（可 pip 安装 onnxruntime + opencv-python 启用双通道，或改用"仅AI高精度识别"策略）；
  6. 更新 i18n.csv 四语言翻译与文档。
- **影响**：重度用户/受限服务商场景从"被动重试"变为"主动控速"，从根本上降低 429 概率；多账号用户吞吐量成倍提升；Linux/macOS 用户即使检测器不可用，AI 服务（Ollama 等）也能被正常调用完成识别。全部通过 Umi-OCR 自带 Python 验证（令牌桶时序、轮询顺序、分隔符解析、空密钥兼容、检测失败三路回退）。

#### v3.0.5（2026-08）—— 讯飞星辰模型名修正
- **动机**：讯飞星辰平台模型命名规则与其他平台不同，需使用 `xop` 前缀格式。
- **改动**：修正讯飞星辰平台模型名为 `xoppaddleocrv16`（PaddleOCR-VL-1.6，默认）、`xophunyuanocr`（HunyuanOCR）；在文档中注明 DeepSeek-OCR 暂不支持 API 调用。
- **影响**：讯飞星辰用户调用不再因模型名格式错误而失败。

#### v3.0.4（2026-08）—— 新增讯飞星辰（MaaS）平台
- **动机**：扩展国产 AI 服务商生态，接入讯飞开放平台 MaaS 服务。
- **改动**：新增讯飞星辰 MaaS Provider，兼容 OpenAI API 格式，默认地址 `https://maas-api.cn-huabei-1.xf-yun.com/v2`（2026-01-10 后发布服务的用户），存量用户可使用 v1 地址；默认模型 `PaddleOCR-VL-1.6`，支持 DeepSeek-OCR、HunyuanOCR 等模型。
- **影响**：服务商数量进一步扩展，为用户提供更多国产化选择。

#### v3.0.3（2026-08）—— 新增 Agnes 平台
- **动机**：接入 Agnes 平台，丰富服务商选项。
- **改动**：新增 Agnes Provider，兼容 OpenAI API 格式，默认模型 `agnes-2.0-flash`，默认地址 `https://apihub.agnes-ai.com/v1`。
- **影响**：用户多一个响应速度快的视觉识别选择。

#### v3.0.0（2026-07）—— 🚀 重大更新：双通道升级与检测器职责重构
- **动机**：旧版 C++ PP-OCRv3 检测器体积大、部署重；且检测器会返回识别文本，遮蔽了 AI 的高精度结果。
- **改动**：
  1. 双通道本地检测模块从基于 C++ 的 PP-OCRv3 替换为基于 ONNX 的 PP-OCRv6，速度更快、精度更高、体积更小（约 40MB）；
  2. 新增检测器版本（`a_v6_detector_version`）与模型大小（`a_v6_model_size`）配置项，用户可选择 Small / Medium / Tiny 模型；
  3. **修复检测模块遮蔽 AI 识别结果的问题**：检测器现在仅负责文本块定位，不再返回识别文本，识别任务完全交由 AI 完成（AI 未识别到时返回空文本，绝不回退 Paddle 识别文本）；
  4. 新增腾讯混元（Hunyuan）平台支持；移除无问芯穹（Infinigence）平台（官方已停止个人用户服务）。
- **影响**：双通道模式精度与速度双提升，部署更轻量；确立了"检测器只定位、AI 只识别"的关键工程约定（详见 §6.2、§10）。

#### v2.9.9（2026-06）—— 局部配置快捷切换服务商
- **动机**：日常使用中频繁打开全局设置切换服务商体验不佳。
- **改动**：在各功能板块的"文字识别(AI OCR)"设置顶部新增"当前 AI 服务商"快捷切换，默认跟随全局设置，也可直接选择服务商覆盖（选择后全局设置同步更新）。
- **影响**：切换服务商无需频繁打开全局设置，提升日常使用体验。

#### v2.9.8（2026-06）—— 百度 PaddleOCR 默认模型升级
- **改动**：将百度 PaddleOCR 默认模型从 PP-OCRv5 升级至 PP-OCRv6，API 端点和请求格式保持不变。
- **影响**：所有原有功能（文档扭曲矫正、方向分类、文本行方向矫正等）可继续使用，识别效果提升。

#### v2.9.7b（2026-05）—— 修复阿里云百炼识别极慢
- **动机**：阿里云百炼平台识别速度极慢（数分钟级），严重影响体验。
- **改动**：
  1. 将请求方式从 DashScope 原生 API（`/services/aigc/multimodal-generation/generation`）切换为 OpenAI 兼容模式（`/compatible-mode/v1/chat/completions`），与阿里云官方推荐方式一致；
  2. 优化 HTTP 客户端连接复用机制，`HTTPClient` 改为复用同一个 opener 实例，避免每次请求都重建 TLS 握手和 TCP 连接。
- **影响**：阿里云响应速度从数分钟降至正常水平；所有平台的多 API 调用场景（如双通道纠错回退）均受益于 opener 复用。

#### v2.9.7a（2026-05）—— 修复 NVIDIA NIM 报错
- **动机**：NVIDIA NIM 平台调用报错 `'Api' object has no attribute '_get_ocr_prompt'`。
- **改动**：`_send_nvidia_nim_request` 方法调用了不存在的 `_get_ocr_prompt()`，修正为接收上游已构建好的 `prompt` 参数。
- **影响**：NVIDIA NIM 平台恢复正常可用。

#### v2.9.7（2026-05）—— 新增 Markdown 输出与 llama.cpp
- **改动**：
  1. 新增 Markdown 格式输出选项，所有平台均可选择以 Markdown 格式直接输出识别结果；
  2. PaddleOCR-VL-1.6 和 PP-StructureV3 原生支持 Markdown 输出，无需裁剪即可获取完整 Markdown 结构；Markdown 模式下保留所有符号（包括 `#` 标题），仅文字和文字+坐标模式不受影响；
  3. 新增 llama.cpp 本地服务商支持；Ollama 平台 API 地址开放为用户可自定义。
- **影响**：输出格式更丰富，本地离线生态更完整。

#### v2.9.6（2026-05）—— PaddleOCR-VL 升级 1.6 与异步统一
- **改动**：更新 PaddleOCR-VL 至 1.6 版本，移除 PaddleOCR-VL 和 PaddleOCR-VL-1.5 支持，保留高级功能供 VL-1.6 使用；全面废弃 PaddleOCR 系列所有模型的同步解析模式，统一使用异步解析模式。
- **影响**：解析模式统一为异步，降低维护成本；VL 模型版本收敛到 1.6。

#### v2.9.5（2026-04）—— 新增 Kimi / NVIDIA NIM / Longcat，Paddle 切换异步
- **改动**：新增 Kimi（月之暗面）、NVIDIA NIM 和 Longcat AI 平台支持；PaddleOCR 系列全部切换为异步解析模式，适配官方 API 变更；PaddleOCR 配置简化为仅需填写 Token。
- **影响**：服务商生态扩展，Paddle 配置更简洁。

#### v2.9.4（2026-04）—— LM Studio 自定义地址 / 小米 MiMo / Prompt 窗口
- **改动**：完善 LM Studio 本地服务配置，新增自定义 API 地址支持；新增小米 MiMo 平台及其专属 Base URL 支持（Code 套餐用户可使用专属地址）；暴露提示词窗口，允许用户自定义纯文字识别和含坐标识别的提示词。
- **影响**：本地服务部署更灵活；用户可根据场景自定义 Prompt。

#### v2.9.3（2026-03）—— Paddle / MinerU 功能开关
- **改动**：增加 Paddle 系列和 MinerU 系列功能开关，提供更强大的识别功能；以 Markdown 为输出格式（Paddle 系列和 MinerU 系列）时，默认去除所有结果中的 `#`；修正文档说明。
- **影响**：版面解析等高级功能可按需开关。

#### v2.9.2（2026-03）—— 新增 GLM-OCR 与 MinerU
- **改动**：增加 GLM-OCR 和 MinerU；默认关闭所有平台的"深度思考"功能；略微优化识别结果与文字不对齐的表现。
- **影响**：新增智谱布局解析与 MinerU 文档解析能力。

#### v2.9.1（2026-03）—— 新增 PaddleOCR-VL-1.5
- **改动**：增加 PaddleOCR-VL-1.5，效果更好；默认关闭版面识别，默认开启 Markdown 美化，输出文本更美观。
- **影响**：PaddleOCR-VL 系列精度提升。

#### v2.9.0（2026-02）—— 新增 PP-StructureV3
- **改动**：增加 PP-StructureV3 功能，对复杂版面内容解析更精准；默认开启版面识别与 Markdown 美化。
- **影响**：复杂版面（多栏、表格、图文混排）解析能力增强。

#### v2.8.0（2026-02）—— 新增 PaddleOCR-V5 / VL
- **改动**：增加 PaddleOCR-V5 以及 PaddleOCR-VL 功能。
- **影响**：引入百度飞桨在线 VL 视觉识别能力。

#### v2.7.0（2026-01）—— 双通道策略调优
- **改动**：调整双通道策略，"双通道：AI 高精度识别（含位置版）"识别精度更高、识别速度更快。
- **影响**：双通道模式体验进一步打磨。

#### v2.6.0（2026-01）—— 🚀 重大更新：双通道识别首发
- **动机**：大模型 OCR 文字精度高，但坐标信息不可靠，导致识别文字与原图无法对齐。
- **改动**：新增并完善双通道识别，通过本地 PaddleOCR 检测识别真实坐标，再用所用 AI 模型识别文本，识别文字与原图文字完美对齐；并发识别、框数限制、本地高分直接采用、裁剪补白等参数可调；整图识别速度较之前版本更快。
- **影响**：彻底解决大模型 OCR 文字对齐难题，奠定后续双通道演进的基础架构。

#### v2.5.0（2025-12）—— 🎉 社区贡献：新增 5 个服务商
- **改动**：新增 Groq（高性能推理）、魔搭 ModelScope（阿里达摩院）、Mistral AI（欧洲 AI）、浦源书生 Intern（学术界 AI）；优化本地服务自定义地址功能。
- **影响**：服务商选择大幅扩展。

#### v2.4.0（2025-11）—— 🚀 重大更新：本地离线识别
- **动机**：满足完全离线、隐私保护场景需求。
- **改动**：新增 Ollama、LM Studio 本地服务商，支持自定义 API 地址，完全离线 OCR 成为可能；优化识别文字对齐，识别后文字与原图位置仅轻微偏移。
- **影响**：零网络依赖的本地 OCR 成为现实。

#### v2.3.0（2025-10）—— 新增阿里云百炼 / 智谱 AI
- **改动**：新增阿里云百炼和智谱 AI 支持，更新所有服务商默认模型，优化界面布局，移除重试次数配置（内置 3 次）。
- **影响**：国产大模型接入，重试逻辑内化。

#### v2.2.0（2025-10）—— 一次配置所有服务商
- **改动**：支持一次性配置所有服务商，切换时无需重新输入 API 密钥和模型。
- **影响**：确立了沿用至今的 `<provider>_api_key` / `_model` / `_api_base` 独立保存、切换不丢失的核心配置约定。

#### v2.1.0（2025-09）—— 新增硅基流动 / 豆包
- **改动**：增加支持硅基流动、豆包视觉模型。
- **影响**：补充高性价比国产视觉模型。

#### v2.0.0（2025-09）—— 重构为多厂商架构
- **改动**：重构为多厂商 AI OCR 插件，支持 OpenAI、Gemini、xAI、OpenRouter。
- **影响**：奠定 Provider 适配器 + ProviderFactory 的多厂商架构基础（详见 §5）。

#### v1.2.0（2025-08）—— 支持 Gemini 2.5 Flash/Pro
- **改动**：支持 Gemini 2.5 Flash 和 Pro 预览版模型，优化识别精度。
- **影响**：模型选择更丰富。

#### v1.1.0（2025-08）—— 多语言与错误处理
- **改动**：增加多语言支持，优化错误处理。
- **影响**：稳定性与适用语种提升。

#### v1.0.0（2025-07）—— 初始版本
- **改动**：初始版本，支持 Gemini OCR 功能。
- **影响**：项目起点，验证 AI 视觉模型接入 Umi-OCR 的可行性。

---

## 十二、扩展开发指南

### 12.1 新增一个 AI 服务商

1. 在 `PROVIDER_CONFIGS` 中添加 `"new_provider": {"api_base": "...", "model": "..."}`；
2. 在 `ai_ocr.py` 中实现 `NewProvider(BaseProvider)`，重写 5 个方法；
3. 在 `ProviderFactory.create_provider` 的 `providers` 字典中注册；
4. 在 `globalOptions` 中添加 `new_provider_api_key` / `new_provider_model` / `new_provider_api_base`；
5. 在 `a_provider` 与 `a_l_provider` 的 `optionsList` 中添加选项；
6. 在 `i18n.csv` 中补充翻译；
7. 在 `_send_request` 中如有特殊路由逻辑（如异步任务），添加对应分支。

### 12.2 调整检测器参数

修改 `localOptions` 中的 `dual_limit_side_len` / `paddle_timeout` / `dual_max_boxes` 等项，或在 `paddle_detector_v6/detector.py` 的 `start()` 中调整 `det_thresh` / `det_box_thresh` / `det_unclip_ratio` / `merge_y_ratio` 的默认值。

### 12.3 自定义 Prompt
> v3.1.0 起新增支持模型列表的平台只需在 `model_lists.py` 的 `PROVIDER_LIST_RULES` 登记获取方式（openai / gemini / ollama 三类）并在 `MODEL_CURATED_LISTS` 给出精选列表，模型下拉菜单即自动生效。

直接在 Umi-OCR 设置面板修改 `a_prompt_text_only` / `a_prompt_with_coordinates` / `a_prompt_markdown`，模板中 `{language}` 占位符会被当前识别语言自动替换。

---

## 十三、注意事项

1. **API 成本**：云端服务按量计费，注意控制 `dual_max_boxes` 与并发数；
2. **网络要求**：国外模型通常需要代理，可在 `z_proxy_url` 配置 http/socks5 代理；
3. **隐私安全**：图片会直接上传到服务商服务器，插件作者不会获取任何用户数据；
4. **本地服务部署**：Ollama / LM Studio / llama.cpp 支持自定义地址，可部署在高性能机器上远程调用；
5. **PaddleOCR 限额**：每位用户每日对同一模型上限 3000 页，超出返回 429；
6. **MinerU 限额**：每个账号每天 600 页最高优先级额度，单文件 ≤200MB / ≤600 页；
7. **Groq 模型白名单**：仅支持 `meta-llama/llama-4-scout-17b-16e-instruct` 与 `maverick-17b-128e-instruct` 两个视觉模型。

---

**感谢使用 Umi-OCR AI OCR 插件！**
