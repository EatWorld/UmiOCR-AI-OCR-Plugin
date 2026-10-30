# Umi-OCR AI OCR 插件

## 🚀 项目简介

本插件为 **Umi-OCR** 提供 **31 家主流AI服务商** 的OCR功能，支持云端和本地AI服务的视觉识别API。作为离线OCR的强力补充，为用户提供更高精度、更广泛语言支持的智能文字识别服务。全局设置中各平台的"模型"字段均为**下拉菜单**，支持通过各平台API**在线获取模型列表**自动填充（见下文「模型下拉菜单与在线获取」），手动输入自定义模型依旧可用。

## 📋 关于 Umi-OCR

**Umi-OCR** 是一款免费、开源、可批量的离线OCR软件，基于 PaddleOCR 开发。它具有以下特点：

[![GitHub stars](https://img.shields.io/github/stars/hiroi-sora/Umi-OCR?style=social)](https://github.com/hiroi-sora/Umi-OCR)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Multi-AI](https://img.shields.io/badge/AI-Multi--Provider-orange.svg)]()

- 🆓 **完全免费**：无需付费，无广告，开源软件
- 📱 **界面友好**：现代化的图形界面，操作简单直观
- 🔄 **批量处理**：支持批量图片OCR，提高工作效率
- 🌐 **多语言支持**：支持中文、英文、日文、韩文等多种语言
- 🔌 **插件系统**：支持扩展插件，功能可定制
- 💻 **跨平台**：支持Windows、Linux等操作系统


## 🌟 支持的 AI 服务商

### 🌐 云端服务商
| 服务商 | 建议模型 | 特点 |
|--------|----------|------|
| **硅基流动 (SiliconFlow)** | PaddlePaddle/PaddleOCR-VL-1.5（**免费**，**强烈推荐**）或 Qwen/Qwen3-VL-32B-Instruct | 开源模型多，价格低，速度快，**中文识别准确率超高**。注意：Qwen2.5-VL 全系、Qwen3-VL-235B、PaddleOCR-VL(1.0) 已于 2026-04 下线 |
| **阿里云百炼 (Alibaba)** | qwen3-vl-235b-a22b-instruct （**强烈推荐**）/ qwen-vl-ocr / qwen3.7-plus | **顶尖OCR模型**，中外文识别**极其优秀**，**强烈推荐**（百炼平台模型名为短横线风格，不带 Qwen/ 前缀） |
| **智谱AI (ZhipuAI)** | GLM-4.6V/GLM-OCR | 国产大模型，多模态能力强，**相当优秀** |
| **豆包(Doubao)** | doubao-seed-2-0-pro / doubao-seed-2-1-pro | 中文优化效果好，性价比高 |
| **OpenAI** | gpt-5.5 | 高精度，多语言支持 |
| **自定义OpenAI兼容 (Custom)** | 任意兼容模型（如 gpt-4o、qwen-vl-plus 等） | **支持自定义API地址**，可接入 vLLM、One API、new-api 中转、自建服务等任意 OpenAI 兼容平台，请求发送到 `{地址}/chat/completions` |
| **Google Gemini** | gemini-3.5-pro/gemini-3.5-flash | 速度快，成本低 |
| **xAI Grok** | grok-4.2 | 创新模型，独特优势 |
| **OpenRouter** | moonshotai/kimi-k2.6:free、qwen/qwen3-vl-235b-a22b-instruct、nvidia/nemotron-3.5-super-vl:free | 统一接口，模型丰富，多种免费视觉模型 |
| **Groq** | meta-llama/llama-4-maverick-17b-128e-instruct | 高性能推理，速度极快 |
| **魔搭 (ModelScope)** | Qwen/Qwen3-VL-235B-A22B-Instruct **（强烈推荐）** | 阿里达摩院开源平台，模型丰富，免费使用|
| **腾讯混元 (Hunyuan)** | hy-vision-2.0-instruct | 腾讯自研多模态模型，支持图片理解，OpenAI兼容协议 |
| **Mistral AI** | mistral-ocr-4-0 (mistral-ocr-latest) | 欧洲AI公司，视觉模型优秀，免费使用|
| **浦源书生 (Intern)** | intern-s2-preview/intern-s1-pro/internvl3.5-241b-a28b | 学术界AI平台，多模态能力强，免费使用，其中intern-s2-preview/intern-s1-pro为**优秀OCR模型**，中文识别**非常优秀**，**十分推荐**|
| **Kimi（月之暗面）** | kimi-k2.6/kimi-k2.5 | 月之暗面AI平台，支持视觉模型，长文本处理能力强，**支持自定义Base URL**|
| **NVIDIA NIM** | moonshotai/kimi-k2.6 | NVIDIA高性能推理平台，视觉模型优秀，**支持自定义Base URL**|
| **百度PaddleOCR系列** | V3/V6/VL-1.6 | 百度飞桨平台，支持多语言识别，高效准确解析文档内容，其中PaddleOCR-VL-1.6 为**顶尖OCR模型**，中外文识别**极其优秀**，**非常推荐**|
| **MinerU系列** | pipeline(默认)/vlm(推荐) /MinerU-HTML/MinerU 2.5系列（官网暂未上线，上线后支持直接调用） | 行业领先的文档解析服务商，尤其擅长处理非标准和复杂文档，拥有**顶尖OCR模型**，中外文识别**极其优秀**，**非常推荐**|
| **面壁智能 (ModelBest)** | MiniCPM-OCR-1.0 | **文档解析专用模型**：识别文字、表格、公式、印章与版面，原生返回页面 Markdown 与**真实坐标块**，同步/异步双模式，坐标模式下无需本地检测，**强烈推荐** |
| **小米MiMo** | mimo-v2.5 | 小米自研AI模型，支持图片理解，**支持专属Base URL**（Code套餐用户可使用 token-plan-cn.xiaomimimo.com）|
| **Longcat AI** | LongCat-Flash-Chat/LongCat-Flash-Thinking | 美团旗下AI平台，兼容OpenAI和Anthropic API格式，每日免费Token额度 |
| **Agnes** | agnes-2.0-flash | 兼容OpenAI API格式，支持视觉识别，响应速度快 |
| **讯飞星辰 (MaaS)** | xoppaddleocrv16/xophunyuanocr | 讯飞开放平台MaaS服务，兼容OpenAI API格式，支持多模态视觉识别。注意模型名需用xop前缀格式 |
| **OpenCode Go** | grok-4.5/glm-5.2/kimi-k3/deepseek-v4-pro/hy3 | OpenCode 低价订阅网关，OpenAI兼容协议，统一访问精选开源编程/视觉模型，**需选择支持图像输入的视觉模型** |
| **OpenCode Zen** | kimi-k3/glm-5.2/deepseek-v4-pro/minimax-m3/hy3-free | OpenCode AI网关，OpenAI兼容协议，按量付费访问精选模型，**仅 chat/completions 接口的模型可用于OCR** |

### 🏠 本地服务商（离线识别）
| 服务商 | 建议模型 | 特点 |
|--------|----------|------|
| **Ollama** | qwen2.5vl:7b, qwen3vl:8b | 🔒 **完全离线**，隐私保护，免费使用，**支持自定义地址** |
| **LM Studio** | llava, llava-1.5-7b-hf | 🔒 **完全离线**，图形界面友好，OpenAI兼容，**支持自定义地址** |
| **llama.cpp** | 用户自行加载的视觉模型 | 🔒 **完全离线**，高性能推理，OpenAI兼容API，**支持自定义地址和可选API Key** |

> 💡 **自定义地址功能**：Ollama、LM Studio 和 llama.cpp 均支持自定义 API 地址，您可以：
> - 🌐 连接到局域网内其他机器上的 Ollama/LM Studio/llama.cpp 服务
> - ⚡ 在配置较低的机器上运行 Umi-OCR，连接到高性能机器上的 AI 服务  
> - 🔧 灵活部署，充分利用现有硬件资源
> - 📡 支持远程AI服务，实现分布式OCR处理



## 📊 对比识别效果

### 设置界面
![设置界面](docs/images/00.jpg)

### 识别图片："对于及其复杂的手写信息，也能完美识别"
![识别图片](docs/images/1.png)

### 本地PaddleOCR识别效果，结果很差劲
![PaddleOCR识别效果，很差劲](docs/images/2.jpg)

### WechatOCR识别效果，结果很差劲
![WechatOCR识别效果，很差劲](docs/images/3.jpg)

### AI OCR(模型：gemini 2.5 flash)识别效果，非常完美
![AI OCR识别效果，完美！](docs/images/4.png)

<img width="542" height="742" alt="image" src="https://github.com/user-attachments/assets/08df5339-7f6c-4061-a822-efe8a2d1da67" />

<img width="541" height="739" alt="image" src="https://github.com/user-attachments/assets/81d0bba5-eed2-4a72-bfc9-0dcf8a3aacf3" />






## ✨ 功能特点

| 功能 | 描述 |
|------|------|
| 🚀 **高精度识别** | 基于最新的AI视觉模型，支持多种语言文字识别 |
| 🌍 **多语言支持** | 支持中文、英文、日文、韩文、法文、德文、西班牙文、俄文、阿拉伯文等 |
| ⚡ **多厂商选择** | 支持31家 AI服务商，包括OpenAI、Gemini、xAI、OpenRouter、硅基流动、豆包、面壁智能、Agnes、讯飞星辰等 |
| 📋 **模型下拉菜单** | 全局设置中各平台的"模型"字段为下拉菜单，支持**在线获取平台模型列表**自动填充；选"自定义"可手填任意模型，旧配置无缝兼容 |
| 📍 **坐标提取** | 可选择输出文字的位置坐标信息（面壁智能/文档解析类模型原生返回真实坐标块） |
| 📝 **Markdown输出** | 支持以Markdown格式直接输出识别结果，保留标题、列表、表格等结构 |
| 🔧 **灵活配置** | 支持图像质量、尺寸、超时等多项参数调整 |
| 🌐 **代理支持** | 支持HTTP/SOCKS5代理，适应不同网络环境 |
| ⏱️ **速率限制** | 令牌桶限速（全局设置"每分钟最大请求数"），主动控制单位时间请求数，避免触发429限流 |
| 🔑 **密钥池** | 可在API密钥框填写多个密钥（逗号/分号/换行分隔），自动轮询分摊请求压力 |
| 🔄 **智能重试** | 自动重试机制，429时指数退避，提高识别成功率 |
| 🚀 **并发处理** | 支持批量图片并发识别，提高处理效率 |
| ✏️ **自定义提示词** | 暴露提示词窗口，允许用户根据不同场景自定义识别提示词 |

## 📦 安装要求

1. **Umi-OCR软件**：需要安装 [Umi-OCR](https://github.com/hiroi-sora/Umi-OCR) v2.0+
2. **AI服务API密钥**：需要获取对应服务商的API密钥
3. **网络连接**：需要能够访问对应的AI服务，国外模型通常需要魔法上网才行

## 🛠️ 安装步骤

1. [AIOCR-releases](https://github.com/EatWorld/UmiOCR-AI-OCR-Plugin/releases)中下载最新版本插件
2. 将压缩包中的AIOCR文件解压至 Umi-OCR 的插件目录：
   ```
   UmiOCR-data/plugins/
   ```
3. 重启 Umi-OCR 软件
4. 在OCR引擎选择中找到 "AI OCR（云端）"


## ⚙️ 配置说明


### 1. 配置插件

**首次配置（推荐一次性配置所有服务商）**：
1. 在Umi-OCR中选择 "AI OCR（云端）"
2. 在全局设置中配置所有你要使用的服务商：
   - 填写 OpenAI API密钥和模型（如需要）
   - 填写 Gemini API密钥和模型（如需要）
   - 填写其他服务商的配置（如需要）
   - **密钥池（可选）**：在任一服务商的API密钥框中填写多个密钥，用逗号、分号或换行分隔，插件会自动轮询使用，分摊请求压力（适合高频使用多个账号的场景）
3. 选择当前要使用的AI服务商并点击**应用修改**
4. （可选）自定义提示词：在全局设置中可修改"纯文字识别 Prompt"和"含坐标识别 Prompt"，根据特定场景优化识别效果。默认提示词适用于大多数情况，无需修改。
5. **速率限制（可选）**：若使用有严格频率限制的服务商（如"每分钟60次请求"），可在全局设置-高级中设置"每分钟最大请求数"（令牌桶限速，建议设为服务商限额的80%左右，0表示不限制），插件将主动控制单位时间内的请求总数，最大程度避免429错误。
6. 在局部设置中选择"识别策略"：
   - 双通道：AI高精度识别（含位置版）：输出带坐标的文本，适合PDF等文档识别。
   - 仅AI高精度识别：直接输出纯文本，不含坐标，适合只需要文本信息的识别。
6. 在局部设置中选择"输出格式"：
    - 仅文字：输出纯文本结果。
    - 文字+坐标：输出带位置坐标的文本。
    - Markdown格式：以Markdown格式直接输出识别结果，保留标题、列表、表格等结构。PaddleOCR-VL-1.6和PP-StructureV3原生支持Markdown输出（PaddleOCR-V5原生不支持此功能）。
7. 设置参数：
   - 裁剪边缘补白 ： 2 px
   - 最大识别框数 ： 30–100 （按图片复杂度与成本权衡）
   - 并发识别数 ： 3–6 （视本机与服务商速率）,Paddle系列和MinerU系列**上限为2**
   - 最小框面积 ： 0 或 100–500 px^2 （有小字场景建议 0 ）
<img width="598" height="789" alt="image" src="https://github.com/user-attachments/assets/17dcfc1a-4c4b-40a8-b686-ece5ecafe19a" />

**日常使用**：
- 只需在"当前AI服务商"下拉菜单中切换并点击**应用修改**即可
- 无需重新输入API密钥和模型
- 所有配置都会自动保存

### 1.5 模型下拉菜单与在线获取（v3.1.0 新增）

全局设置中各平台的"模型"字段已从手填文本框升级为**下拉菜单**：

- **候选列表来源**：**以从各平台实拉获得的在线列表为准**——已成功拉取的平台，下拉菜单仅由"在线列表 + 你已保存的值 + 自定义"组成，不再混入任何内置候选；从未成功拉取的平台才以内置精选列表作为引导（首次「应用修改」自动补拉，成功后即时替换为纯在线列表）。你已保存的当前值始终保留，升级不丢配置（历史值首尾误粘贴的空白/换行会被自动清理后匹配）。
- **在线获取模型列表**：点击全局设置顶部的「🔄 拉取当前服务商」或「🔄 拉取全部已配置平台」按钮，插件会调用各平台的模型列表 API 自动填充下拉菜单。**自定义 OpenAI 兼容平台（vLLM、One API、new-api、各类反代/中转等）只要填写了自定义 API 地址，无需 API 密钥也会尝试拉取**；本地服务（Ollama 等）需处于运行状态。拉取结果缓存于插件目录 `model_lists_cache.json`，**即时生效**；也可双击运行插件目录下的 `刷新模型列表.bat` 离线拉取（重启 Umi-OCR 后生效）。
- **自动获取**：首次「应用修改」某平台配置时，插件会在后台自动补拉一次该平台的在线模型列表（已有缓存则跳过；失败时静默，不影响识别，可稍后用按钮重试）。
- **手动输入依旧可用**：见下方「★ 如何手填自定义模型」详细步骤——与旧版纯手填行为完全一致，本地模型、未收录模型、中转站模型均可使用。
- **地址归一化**：与实际调用完全一致——Gemini 地址（含 `generativelanguage.googleapis.com`）从完整 `:generateContent` 端点自动归位到 models 列表端点并过滤出支持图像输入的模型；Ollama（`/api` 结尾或 `:11434`）走 `/api/tags` 无需密钥；其余平台按 OpenAI 兼容 `GET {地址}/models`（Bearer 认证，地址带不带 `/chat/completions` 后缀均可）。

#### ★ 如何手填自定义模型（详细步骤，必读）

「自定义（手动输入）」的**真实输入框默认是隐藏的**（属于高级选项，避免 28 个平台各多占一行拉长设置页）。请严格按以下步骤操作：

1. 打开 **全局设置**，在目标平台的「XX 模型」下拉菜单中选择 **自定义（手动输入）**；
2. 点击全局设置页面**顶部控制栏右侧的「高级」开关**（在「重置」按钮左侧；不开启时所有带 `*` 号的高级选项一律隐藏）；
3. 此时「XX 模型」下拉框**正下方**会出现带 `*` 号的「**\* XX 自定义模型**」文本框（例如「\* OpenAI 自定义模型」「\* 面壁智能 自定义模型」），在里面直接输入任意模型名（需支持图像输入）；
4. 点击「应用修改」保存。此后实际调用即使用该手填值。

> **注意事项**：
> - 仅当下拉框选中"自定义（手动输入）"时，「\* XX 自定义模型」输入框的值才会生效；下拉选中具体模型时该框会被忽略；
> - 自定义框**留空**时自动回退到该平台的默认模型；
> - 每个平台都有自己独立的「\* XX 自定义模型」输入框，位置都紧跟在各自「XX 模型」下拉框下方；本地服务（Ollama / LM Studio / llama.cpp）同样适用；
> - 关闭「高级」开关后输入框会再次隐藏，但**已保存的值不受影响**，照常生效；
> - 悬停任意平台的「XX 模型」下拉框，提示文字末尾也附有上述指引。

#### 弹层与滚动条

候选列表较多时（如硅基流动、豆包动辄上百个模型），下拉弹层**最多显示约 12 行**，右侧提供**加宽的滚动条（可点击、可拖动）**，靠近屏幕底部时会自动向上弹出；**过长的模型名在弹层中会自动折行**（行高自适应，不再挤成一行或重叠），收起状态下过长的选中值以中间省略号显示。该弹层体验由 Umi-OCR 核心界面补丁（Configs.qml）提供——维护者本地安装已包含；**原版 Umi-OCR 的弹层为 Qt 默认样式**（不限高、滚动条极细、长名单行裁剪），候选很多时建议用鼠标滚轮滚动，或使用「自定义」+手填、`刷新模型列表.bat` 精简候选。

> 注意：按钮联动依赖 Umi-OCR 全局设置对"按钮回调"的字符串分发支持。若你的 Umi-OCR 版本点击按钮无反应，请直接使用 `刷新模型列表.bat` 脚本，效果相同。

### 2. 开始识别

- 使用截图OCR、批量OCR等功能
- 插件会自动调用对应的AI API进行识别



## ⚠️ 注意事项

1. **API成本**：AI API按使用量计费，请注意控制使用频率
2. **网络要求**：需要稳定的网络连接访问AI服务
3. **图像大小**：建议设置合适的最大图像尺寸以控制成本
4. **隐私安全**：图像会直接上传到服务商服务器进行处理，插件作者不会得到你的任何图片和信息
5. **速度限制**：云端API可能有速度限制，不适合大量并发请求
6. **模型选择**：不同模型的精度和成本不同，请根据需求选择
7. **中文变体保留**：当语言为“自动/中文”时，插件已在提示词中明确禁止简繁转换、全角/半角转换和字符归一化；繁简混排保持混合状态；逐字抄写不重写。
8. **Linux/macOS 双通道**：内置本地检测器（ONNX Runtime 库）为 Windows 专属。Linux/macOS 下双通道模式会自动回退为 AI 直出（AI 服务不受影响）；如需启用双通道，可自行通过 pip 安装 `onnxruntime` 与 `opencv-python` 后重启。也可在识别策略中直接选择"仅AI高精度识别"。




## 🔑 API密钥获取

### 硅基流动 (SiliconFlow)
1. 访问 [硅基流动](https://cloud.siliconflow.cn/)
2. 注册账号并获取API密钥
3. 支持多种开源视觉模型

### 豆包 (Doubao)
1. 访问 [火山引擎](https://console.volcengine.com/ark/)
2. 开通豆包服务并获取API密钥
3. 字节跳动自研多模态模型

### OpenAI
1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登录账号并创建API密钥
3. 复制生成的密钥

### Google Gemini
1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录Google账号
3. 创建新的API密钥

### xAI Grok
1. 访问 [xAI Console](https://console.x.ai/)
2. 注册并获取API密钥

### 阿里云百炼 (Alibaba)
1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 开通百炼服务并获取API密钥
3. 支持通义千问系列视觉模型

### 智谱AI (ZhipuAI)
1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册账号并创建API密钥
3. 国产大模型，多模态能力强

### OpenRouter
1. 访问 [OpenRouter](https://openrouter.ai/keys)
2. 注册账号并创建API密钥

### Groq
1. 访问 [Groq Console](https://console.groq.com/)
2. 注册账号并获取API密钥
3. 高性能推理平台，速度极快

### 魔搭 (ModelScope)
1. 访问 [魔搭社区](https://www.modelscope.cn/)
2. 注册账号并获取访问令牌 (Access Token)
3. 阿里达摩院开源AI平台

### 腾讯混元 (Hunyuan)
1. 访问 [腾讯混元大模型平台](https://cloud.tencent.com/product/1823)
2. 注册账号并获取API密钥
3. 腾讯自研多模态模型，支持图片理解，兼容OpenAI协议
4. 默认API地址：`https://tokenhub.tencentmaas.com/v1`
5. 支持模型：hy-vision-2.0-instruct、hunyuan-t1-vision-20250916、youtu-vita 等

### Mistral AI
1. 访问 [Mistral Platform](https://console.mistral.ai/)
2. 注册账号并创建API密钥
3. 欧洲AI公司，视觉模型优秀

### 浦源书生 (Intern)
1. 访问 [书生·浦语平台](https://chat.intern-ai.org.cn/) 注册账号并获取API密钥；可自行申请更多Token
2. **2026年10月起 API 地址变更为 `https://discovery-api.intern-ai.org.cn/v1`**（插件默认值已同步更新；旧地址 `chat.intern-ai.org.cn/api/v1` 已停用，老用户无需手动修改，重启后自动使用新地址）
3. **RPM 限额**：生成模型 **50 次/分钟**、决策模型 **200 次/分钟**——所有 API Key 共享此额度、调用量合并计算（非单 Key 限额）；建议在全局设置-高级中将「每分钟最大请求数」设为 40 左右
4. 学术界AI平台，多模态能力强；支持模型：intern-latest / intern-s2-preview / intern-s1-pro / internvl3.5-241b-a28b 等，其中 intern-s2-preview/intern-s1-pro 为**优秀OCR模型**，中文识别**非常优秀**

### Kimi（月之暗面）
1. 访问 [Kimi 开放平台](https://platform.moonshot.cn/)
2. 注册账号，在 [API Keys](https://platform.moonshot.cn/console/api-keys) 页面创建API密钥
3. 月之暗面AI平台，支持视觉模型，长文本处理能力强
4. 默认API地址：`https://api.moonshot.cn/v1`
5. 支持模型：kimi-k2.6、kimi-k2.5 等

### NVIDIA NIM
1. 访问 [NVIDIA NIM](https://build.nvidia.com/)
2. 注册账号并获取API密钥
3. NVIDIA高性能推理平台，视觉模型优秀
4. 默认API地址：`https://integrate.api.nvidia.com/v1`
5. 支持模型：moonshotai/kimi-k2.6 等

### 小米MiMo
1. 访问 [Xiaomi MiMo API开放平台](https://platform.xiaomimimo.com/)
2. 使用小米账号登录，在 [控制台-API Keys](https://platform.xiaomimimo.com/#/console/api-keys) 创建API密钥
3. 小米自研AI模型，支持图片理解
4. 默认API地址：`https://api.xiaomimimo.com/v1`
5. 如购买了Code套餐，可使用专属地址：`https://token-plan-cn.xiaomimimo.com/v1`

### Longcat AI
1. 访问 [Longcat AI 开放平台](https://longcat.chat/platform/)
2. 注册账号（国内用户手机号注册，海外用户手机号或邮箱注册），在 [API Keys](https://longcat.chat/platform/api_keys) 页面创建API密钥
3. 美团旗下AI平台，兼容OpenAI和Anthropic API格式，每日免费Token额度
4. 默认API地址：`https://api.longcat.chat/openai/v1`
5. 支持模型：LongCat-Flash-Chat、LongCat-Flash-Thinking、LongCat-Flash-Lite 等

### Agnes
1. 访问 [Agnes 开放平台](https://agnes-ai.com/)
2. 注册账号并创建API密钥
3. 兼容OpenAI API格式，支持视觉识别
4. 默认API地址：`https://apihub.agnes-ai.com/v1`
5. 支持模型：agnes-2.0-flash 等

### 讯飞星辰 (MaaS)
1. 访问 [讯飞开放平台](https://www.xfyun.cn/)，在「服务管控」页面开通对应模型服务
2. 从服务管控页面获取 APIKey 和对应服务的 ModelID
3. 兼容 OpenAI API 格式，支持图像理解多模态识别
4. 默认API地址：`https://maas-api.cn-huabei-1.xf-yun.com/v2`（2026年1月10日后发布服务的用户）；存量用户可使用 `http://maas-api.cn-huabei-1.xf-yun.com/v1`
5. **注意：讯飞平台模型名需使用xop前缀格式，与其他平台不同**：
   - `xoppaddleocrv16`（PaddleOCR-VL-1.6，默认）
   - `xophunyuanocr`（HunyuanOCR）
   - DeepSeek-OCR 暂不支持 API 调用

### OpenCode Go
1. 访问 [OpenCode 控制台](https://opencode.ai/auth) 订阅 Go（首月 $5，之后 $10/月）并复制 API 密钥
2. 兼容 OpenAI API 格式（OpenAI-compatible），统一访问精选开源编程/视觉模型
3. 默认API地址：`https://opencode.ai/zen/go/v1`（请求发送至 `https://opencode.ai/zen/go/v1/chat/completions`）
4. 支持模型（需选择支持图像输入的视觉模型）：grok-4.5、glm-5.2、kimi-k3、kimi-k2.6、deepseek-v4-pro、mimo-v2.5、hy3 等
5. 完整模型列表见 `https://opencode.ai/zen/go/v1/models`

### OpenCode Zen
1. 访问 [OpenCode 控制台](https://opencode.ai/auth) 登录 Zen，添加账单信息并复制 API 密钥（按量付费）
2. 兼容 OpenAI API 格式（OpenAI-compatible），按量付费访问精选模型
3. 默认API地址：`https://opencode.ai/zen/v1`（请求发送至 `https://opencode.ai/zen/v1/chat/completions`）
4. **注意：仅 chat/completions 接口的模型可用于 OCR**；GPT/Claude/Gemini 等走 responses/messages 接口的模型暂不支持。可选视觉模型：kimi-k3、kimi-k2.6、glm-5.2、deepseek-v4-pro、minimax-m3、hy3-free 等
5. 完整模型列表见 `https://opencode.ai/zen/v1/models`

### 百度飞桨OCR
1. 访问 [AI Studio](https://aistudio.baidu.com/account/accessToken) 获取 Access Token
2. 支持模型：PP-OCRv6 / PaddleOCR-VL-1.6 / PP-StructureV3
3. 已切换为异步解析模式，只需填写 Token 即可使用
4. 每位用户每日对同一模型的解析上限为3000页，超出将返回429错误；可自行申请更多页数

### 面壁智能 (ModelBest)
1. 访问 [面壁智能开放平台](https://platform.modelbest.ai/) 注册账号
2. 在控制台的 API Keys 页面创建 **MAP API Key**，填入插件"面壁智能 API密钥"
3. 默认模型：MiniCPM-OCR-1.0（文档解析模型，识别文字/表格/公式/印章并返回版面坐标）
4. 默认API地址：`https://api.modelbest.ai`（同步端点 `{地址}/v1/document-parse`，异步任务 `{地址}/v1/document-parse/jobs`）
5. 特性说明：
   - 图片走同步接口直出；超大图片自动转异步任务并轮询结果
   - 原生返回页面 Markdown（表格为 HTML、公式为 LaTeX）与真实坐标块，**"文字+坐标"输出无需本地检测**，识别策略选"双通道"即可直接获得精准坐标
   - 局部设置中可调「文档自适应旋转」与「印章内容识别」；如需精确坐标建议关闭自适应旋转
   - 模型列表可在线获取（GET /v1/models），支持后续上新模型直接切换

### MinerU
1. 访问 MinerU官网：(https://mineru.net/apiManage/token)
2. 注册账号并免费获取**API TOKEN**和**模型名称**，如 pipeline（默认）/vlm(推荐) /MinerU-HTML等
3. 每个账号每天享有 600 页最高优先级解析额度，超过 600 页的部分优先级降低
4. 单个文件大小不能超过 200MB,文件页数不超出 600 页（“批量文档”和“批量OCR”可无视此约束）

   
## 🏠 本地服务安装指南

### Ollama (完全离线)
1. **安装Ollama**：
   ```bash
   # Linux/macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # 从 https://ollama.ai 下载安装包
   ```

2. **下载视觉模型**：
   ```bash
   # 下载llava模型（推荐）
   ollama pull llava
   
   # 或下载其他视觉模型
   ollama pull llava:7b
   ollama pull bakllava
   ```

3. **启动服务**：
   ```bash
   ollama serve
   # 服务将在 http://localhost:11434 启动
   ```

4. **在插件中配置**：
   - 服务商：选择 "Ollama (本地)"
   - 模型：填入已下载的模型名（如 llava）
   - 默认API地址（可修改）：http://localhost:11434/api
   - API密钥：留空即可

### LM Studio (图形界面)
1. **下载安装**：
   - 访问 [LM Studio官网](https://lmstudio.ai/)
   - 下载并安装适合您系统的版本

2. **下载模型**：
   - 在LM Studio中搜索并下载支持视觉的模型
   - 推荐：`llava-1.5-7b-hf`, `llava-1.6-34b-hf`

3. **启动本地服务器**：
   - 在LM Studio中点击"本地服务器"
   - 选择已下载的视觉模型
   - 启动服务器（默认端口1234）

4. **在插件中配置**：
   - 服务商：选择 "LM Studio (本地)"
   - 模型：填入LM Studio中加载的模型名
   - 默认API地址（可修改）：http://localhost:1234/v1
   - API密钥：留空或填入"not-needed"

### llama.cpp (高性能推理)
1. **安装llama.cpp**：
   - 从 [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases) 下载适合您系统的版本
   - 或通过包管理器安装

2. **下载视觉模型**：
   - 从 Hugging Face 等平台下载支持视觉的 GGUF 模型文件
   - 推荐：LLaVA、Qwen-VL 等视觉模型的 GGUF 量化版本

3. **启动服务**：
   ```bash
   llama-server -m <模型路径> --host 0.0.0.0 --port 8080
   # 服务将在 http://localhost:8080/v1 启动（OpenAI兼容API）
   # 如需设置API密钥：llama-server -m <模型路径> --api-key your-secret-key
   ```

4. **在插件中配置**：
   - 服务商：选择 "llama.cpp (本地)"
   - 模型：填入加载的模型名称
   - 默认API地址（可修改）：http://localhost:8080/v1
   - API密钥：如启动时设置了 `--api-key` 则填写对应密钥，否则留空

### 🔒 本地服务优势
- **完全离线**：无需网络连接，数据不上传
- **隐私保护**：所有处理在本地完成
- **免费使用**：无API调用费用
- **自主控制**：可选择和定制模型




## 📝 版本历史
- **v3.1.0**：🚀 **重大更新**
  - **新增面壁智能（ModelBest）平台支持**：接入其新一代在线文档解析模型 **MiniCPM-OCR-1.0**（[官方文档](https://platform.modelbest.ai/console/docs/models/document-parse)），识别文字、表格（HTML）、公式（LaTeX）、印章与版面结构。图片同步直出、超大图自动转异步任务轮询；原生返回真实坐标块，**"文字+坐标"模式无需本地检测**；局部设置提供「文档自适应旋转」「印章内容识别」开关。
  - **全局设置"模型"字段全面升级为下拉菜单，在线列表强制优先**：各平台模型列表通过 API 实时获取（Gemini 自动归位 models 端点并过滤可用模型、Ollama 走 /api/tags 无需密钥、其余按 OpenAI 兼容 /models）；**自定义 OpenAI 兼容平台（vLLM/One API/new-api/反代等）填写自定义地址后无需密钥即可拉取**；已成功拉取的平台仅使用在线列表 + 已存值 + 自定义，不再混入内置候选（未拉取过的平台以精选列表引导，**首次「应用修改」自动后台补拉**并即时热刷新替换）。已保存的旧模型值自动合并，升级不丢配置；选「自定义」仍可手填任意模型（详细步骤见 1.5 节）。
  - **拉取后即时热刷新（修复空转）**：修复 Python 侧对 QML `var` 属性链式赋值静默失败导致"拉取成功但下拉不更新"的问题；模型列表缓存增加并发写保护（锁 + 原子替换）。
  - **核心界面优化**（Configs.qml 补丁，随维护者安装提供；原版核心为 Qt 默认样式）：模型下拉弹层限高约 12 行、加宽可拖动滚动条、长模型名自动折行、收起态过长名称中间省略、枚举匹配容错历史值首尾空白。
  - **书生平台（Intern）域名变更**：API 地址更新为 `https://discovery-api.intern-ai.org.cn/v1`（旧地址停用），注明 RPM 限额（生成模型 50 次/分钟、决策模型 200 次/分钟，所有 Key 共享额度），新增可自定义 API 地址项。
  - **其他**：修复 i18n.csv 表头异常导致简体中文/日语界面回落英文翻译；刷新各平台建议模型（硅基流动已下线模型更换为 PaddleOCR-VL-1.5 等）；修复 llama.cpp 无密钥被误报"API密钥不能为空"；PluginInfo 增加 version 字段。
- **v3.0.8**：✨ **新增** - 添加 OpenCode Go 与 OpenCode Zen 平台支持（均为 OpenAI 兼容网关，默认地址 `https://opencode.ai/zen/go/v1` 与 `https://opencode.ai/zen/v1`，请求发送至 `{地址}/chat/completions`）。两者均复用 OpenAI 兼容协议，只需填写 API 密钥与模型名（需选择支持图像输入的视觉模型）即可使用。
- **v3.0.7**：✨ **新增** - 新增「自定义OpenAI兼容 (Custom)」服务商（社区建议 [#35](https://github.com/EatWorld/UmiOCR-AI-OCR-Plugin/issues/35)）。可填写任意 OpenAI 兼容的 API 地址（如 vLLM、One API、new-api 中转、自建服务等），请求将发送到 `{API地址}/chat/completions`，API 密钥与模型名均可自定义。修复 i18n.csv 空行导致翻译表加载失败的问题。
- **v3.0.6**：🚀 **重大更新** - 新增令牌桶速率限制（主动避免429限流）与API密钥池轮询（社区建议 #12）。全局设置新增"每分钟最大请求数"（0=不限制）；任意服务商的API密钥框支持填写多个密钥（逗号/分号/换行分隔）自动轮询；429重试改为指数退避。修复Linux/macOS下OCR返回空的问题（#28）：检测器不可用时自动回退AI直出，AI服务（如Ollama）始终被正常调用。
- **v3.0.5**：🔧 **修复** - 修正讯飞星辰平台模型名：使用 xop 前缀格式（`xoppaddleocrv16`、`xophunyuanocr`），注明 DeepSeek-OCR 暂不支持 API 调用。
- **v3.0.4**：✨ **新增** - 添加讯飞星辰（MaaS）平台支持（兼容 OpenAI API 格式，默认模型 `PaddleOCR-VL-1.6`，默认地址 `https://maas-api.cn-huabei-1.xf-yun.com/v2`，支持 DeepSeek-OCR、HunyuanOCR 等模型）。
- **v3.0.3**：✨ **新增** - 添加 Agnes 平台支持（兼容 OpenAI API 格式，默认模型 `agnes-2.0-flash`，默认地址 `https://apihub.agnes-ai.com/v1`）。
- **v3.0.0**：🚀 **重大更新** - 双通道模式全面升级！将本地检测模块从基于C++的PP-OCRv3替换为基于ONNX的PP-OCRv6，速度更快、精度更高、体积更小（约40MB）。新增检测器版本和模型大小配置项，用户可选择Small/Medium/Tiny模型。修复检测模块遮蔽AI识别结果的问题：检测器现在仅负责文本块定位，不再返回识别文本，识别任务完全交由AI完成。新增腾讯混元（Hunyuan）平台支持；移除无问芯穹（Infinigence）平台（官方已停止个人用户服务）。
- **v2.9.9**：在各功能板块的"文字识别(AI OCR)"设置顶部新增"当前AI服务商"快捷切换，默认跟随全局设置，也可直接选择服务商覆盖（选择后全局设置同步更新），无需频繁打开全局设置即可切换服务商。
- **v2.9.8**：百度PaddleOCR模型升级：将默认模型从PP-OCRv5升级至PP-OCRv6，API端点和请求格式保持不变，所有原有功能（文档扭曲矫正、文档方向分类、文本行方向矫正等）均可继续使用。
- **v2.9.7b**：修复阿里云百炼平台识别速度极慢的问题：将请求方式从DashScope原生API（`/services/aigc/multimodal-generation/generation`）切换为OpenAI兼容模式（`/compatible-mode/v1/chat/completions`），与阿里云官方推荐方式一致，响应速度从数分钟降至正常水平。同时优化HTTP客户端连接复用机制，`HTTPClient`改为复用同一个opener实例，避免每次请求都重建TLS握手和TCP连接，所有平台的多API调用场景（如双通道纠错回退）均受益。
- **v2.9.7a**：修复NVIDIA NIM平台报错 `'Api' object has no attribute '_get_ocr_prompt'` 的问题：`_send_nvidia_nim_request`方法调用了不存在的`_get_ocr_prompt()`，修正为接收上游已构建好的`prompt`参数。
- **v2.9.7**：新增Markdown格式输出选项，所有平台均可选择以Markdown格式直接输出识别结果；PaddleOCR-VL-1.6和PP-StructureV3原生支持Markdown输出，无需裁剪即可获取完整Markdown结构；Markdown模式下保留所有符号（包括#标题），仅文字和文字+坐标模式不受影响。新增llama.cpp本地服务商支持；Ollama平台API地址开放为用户可自定义。
- **v2.9.6**：更新PaddleOCR-VL至1.6版本，移除PaddleOCR-VL和PaddleOCR-VL-1.5支持，保留高级功能供VL-1.6使用；全面废弃PaddleOCR系列所有模型的同步解析模式，统一使用异步解析模式。
- **v2.9.5**：新增Kimi（月之暗面）、NVIDIA NIM和Longcat AI平台支持；PaddleOCR系列全部切换为异步解析模式，适配官方API变更；PaddleOCR配置简化为仅需填写Token。
- **v2.9.4**：完善LM Studio本地服务配置，新增自定义API地址支持；新增小米MiMo平台及其专属Base URL支持（Code套餐用户可使用专属地址）；暴露提示词窗口，允许用户自定义纯文字识别和含坐标识别的提示词。
- **v2.9.3**：增加Paddle系列和MinerU系列功能开关，提供更强大的识别功能；以Markdown为输出格式（Paddle系列和MinerU系列）时，默认去除所有的结果中的"#"; 修正文档说明。
- **v2.9.2**：增加GLM-OCR和MinerU；默认关闭所有平台的"深度思考"功能；略微优化了识别结果与文字不对齐的表现。
- **v2.9.1**：增加PaddleOCR-VL-1.5，效果更好，默认关闭版面识别，默认开启Markdown美化，输出文本更美观。
- **v2.9.0**：增加PP-StructureV3功能，对复杂版面内容解析更精准。默认开启版面识别，默认开启Markdown美化，输出文本更美观。
- **v2.8.0**：增加PaddleOCR-V5以及PaddleOCR-VL功能。
- **v2.7.0**：调整双通道策略，现在双通道:AI高精度识别(含位置版)识别精度更高、识别速度速度更快。
- **v2.6.0**：🚀 **重大更新** 完美解决大模型OCR无法文字对齐的问题！新增并完善双通道识别，通过本地PaddleOCR检测识别真实坐标，再用所用AI模型识别文本，识别文字与原图文字完美对齐！并发识别、框数限制、本地高分直接采用、裁剪补白等参数可调，整图识别速度较之前版本更快。
- **v2.5.0**：🎉 **社区贡献更新** - 新增5个AI服务商支持！添加Groq（高性能推理）、魔搭ModelScope（阿里达摩院）、Mistral AI（欧洲AI）、浦源书生Intern（学术界AI），大幅扩展AI服务商选择。优化本地服务自定义地址功能。
- **v2.4.0**：🚀 **重大更新** - 新增本地离线识别支持！添加Ollama、LM Studio本地服务商，支持自定义API地址，完全离线OCR成为可能。优化识别文字对齐，现在识别后的文字与原图位置只有轻微偏移。
- **v2.3.0**：新增阿里云百炼和智谱AI支持，更新所有服务商默认模型，优化界面布局，移除重试次数配置（内置3次）
- **v2.2.0**：支持一次性配置所有服务商，切换时无需重新输入API密钥和模型
- **v2.1.0**：增加支持硅基流动、豆包视觉模型
- **v2.0.0**：重构为多厂商AI OCR插件，支持OpenAI、Gemini、xAI、OpenRouter
- **v1.2.0**：支持Gemini 2.5 Flash和Pro预览版模型，优化识别精度
- **v1.1.0**：增加多语言支持，优化错误处理
- **v1.0.0**：初始版本，支持Gemini OCR功能




## 💖 支持

如果这个插件对您有帮助，请考虑：

- 给项目点个星⭐
- 分享给更多需要的人
- 提供反馈和建议
- 参与项目贡献

---

**感谢使用 Umi-OCR 多厂商 AI OCR 插件！**
