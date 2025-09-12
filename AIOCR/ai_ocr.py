# -*- coding: utf-8 -*-
# AI OCR API Implementation with Multi-Provider Support

import json
import base64
import time
import re
import threading
import concurrent.futures
from io import BytesIO
from PIL import Image
import urllib.request
import urllib.parse
import urllib.error

# Provider基类
class BaseProvider:
    """AI OCR服务提供商基类"""
    
    def __init__(self, api_key, api_base=None, model=None, timeout=30, proxy_url=None):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.timeout = timeout
        self.proxy_url = proxy_url
        
    def get_default_api_base(self):
        """获取默认API基础URL"""
        raise NotImplementedError
        
    def get_default_model(self):
        """获取默认模型"""
        raise NotImplementedError
        
    def build_headers(self):
        """构建请求头"""
        raise NotImplementedError
        
    def build_payload(self, image_base64, prompt):
        """构建请求载荷"""
        raise NotImplementedError
        
    def parse_response(self, response_text):
        """解析响应"""
        raise NotImplementedError

# OpenAI Provider
class OpenAIProvider(BaseProvider):
    """OpenAI服务提供商"""
    
    def get_default_api_base(self):
        return "https://api.openai.com/v1"
        
    def get_default_model(self):
        return "gpt-4o"
        
    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }
        
    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析OpenAI响应失败: {str(e)}")

# Google Gemini Provider
class GeminiProvider(BaseProvider):
    def get_default_api_base(self):
        return "https://generativelanguage.googleapis.com/v1beta"
        
    def get_default_model(self):
        return ""
        
    def build_headers(self):
        return {
            "Content-Type": "application/json"
        }
        
    def build_payload(self, image_base64, prompt):
        return {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }]
        }
        
    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析Gemini响应失败: {str(e)}")

# 硅基流动 Provider
class SiliconFlowProvider(BaseProvider):
    """硅基流动服务提供商"""
    
    def get_default_api_base(self):
        return "https://api.siliconflow.cn/v1"
        
    def get_default_model(self):
        return ""
        
    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }
        
    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析硅基流动响应失败: {str(e)}")

# 豆包 Provider
class DoubaoProvider(BaseProvider):
    """豆包服务提供商"""
    
    def get_default_api_base(self):
        return "https://ark.cn-beijing.volces.com/api/v3"
        
    def get_default_model(self):
        return ""
        
    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }
        
    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析豆包响应失败: {str(e)}")

# xAI Grok Provider
class XAIProvider(BaseProvider):
    def get_default_api_base(self):
        return "https://api.x.ai/v1"
        
    def get_default_model(self):
        return ""
        
    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        }
        
    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析xAI响应失败: {str(e)}")



# OpenRouter Provider
class OpenRouterProvider(BaseProvider):
    def get_default_api_base(self):
        return "https://openrouter.ai/api/v1"
        
    def get_default_model(self):
        return ""
        
    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/hiroi-sora/Umi-OCR",
            "X-Title": "Umi-OCR AI Plugin"
        }
        
    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        }
        
    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析OpenRouter响应失败: {str(e)}")
            
# 智谱AI Provider
class ZhipuProvider(BaseProvider):
    """智谱AI服务提供商"""

    def get_default_api_base(self):
        return "https://open.bigmodel.cn/api/paas/v4"

    def get_default_model(self):
        return ""

    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        },
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "thinking": {
                "type": "enabled"
            }
        }

    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析智谱AI响应失败: {str(e)}")


# 阿里云百炼 Provider
class BailianProvider(BaseProvider):
    """阿里云百炼大模型平台服务提供商"""

    def get_default_api_base(self):
        return "https://dashscope.aliyuncs.com/compatible-mode/v1"

    def get_default_model(self):
        return ""  # 百炼模型需用户指定，如"qwen-vl-ocr-latest"

    def build_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def build_payload(self, image_base64, prompt):
        return {
            "model": self.model or self.get_default_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                                # 百炼特有参数：图像像素调整阈值
                                "min_pixels": 28 * 28 * 4,  # 最小像素阈值
                                "max_pixels": 28 * 28 * 8192  # 最大像素阈值
                            }
                        },
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
        }

    def parse_response(self, response_text):
        try:
            data = json.loads(response_text)
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                return None
        except Exception as e:
            raise Exception(f"解析百炼响应失败: {str(e)}")

# Provider工厂
class ProviderFactory:
    @staticmethod
    def create_provider(provider_name, api_key, api_base=None, model=None, timeout=30, proxy_url=None):
        providers = {
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
            "xai": XAIProvider,
            "openrouter": OpenRouterProvider,
            "siliconflow": SiliconFlowProvider,
            "doubao": DoubaoProvider,
        }
        
        if provider_name not in providers:
            raise ValueError(f"不支持的服务提供商: {provider_name}")
        
        provider_class = providers[provider_name]
        
        # 如果没有提供api_base，使用内置的默认值
        if api_base is None:
            temp_provider = provider_class(api_key)
            api_base = temp_provider.get_default_api_base()
        
        # 模型由用户在配置中指定，不使用默认值
        if not model:
            raise ValueError(f"请在配置中指定 {provider_name} 的模型名称")
            
        return provider_class(api_key, api_base, model, timeout, proxy_url)

# HTTP请求工具类
class HTTPClient:
    def __init__(self, timeout=30, proxy_url=None):
        self.timeout = timeout
        self.proxy_url = proxy_url
    
    def post(self, url, headers=None, data=None):
        """发送POST请求"""
        try:
            # 设置默认请求头
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
            
            # 合并请求头
            if headers:
                default_headers.update(headers)
            
            # 准备请求数据
            req_data = data.encode('utf-8') if isinstance(data, str) else data
            req = urllib.request.Request(url, data=req_data, headers=default_headers)
            
            # 创建 SSL 上下文
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # 设置代理和 SSL
            if self.proxy_url:
                proxy_handler = urllib.request.ProxyHandler({
                    'http': self.proxy_url, 
                    'https': self.proxy_url
                })
                https_handler = urllib.request.HTTPSHandler(context=ssl_context)
                opener = urllib.request.build_opener(proxy_handler, https_handler)
            else:
                https_handler = urllib.request.HTTPSHandler(context=ssl_context)
                opener = urllib.request.build_opener(https_handler)
            
            # 发送请求
            response = opener.open(req, timeout=self.timeout)
            response_data = response.read()
            
            # 处理压缩响应
            content_encoding = response.headers.get('Content-Encoding', '').lower()
            if content_encoding == 'gzip':
                import gzip
                response_data = gzip.decompress(response_data)
            elif content_encoding == 'deflate':
                import zlib
                response_data = zlib.decompress(response_data)
            
            # 处理编码
            try:
                response_text = response_data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    response_text = response_data.decode('latin-1')
                except UnicodeDecodeError:
                    response_text = response_data.decode('utf-8', errors='ignore')
            
            return {
                'status_code': response.getcode(),
                'text': response_text
            }
        except urllib.error.HTTPError as e:
            error_data = e.read()
            
            # 处理错误响应的压缩
            content_encoding = e.headers.get('Content-Encoding', '').lower() if hasattr(e, 'headers') else ''
            if content_encoding == 'gzip':
                import gzip
                try:
                    error_data = gzip.decompress(error_data)
                except:
                    pass
            elif content_encoding == 'deflate':
                import zlib
                try:
                    error_data = zlib.decompress(error_data)
                except:
                    pass
            
            try:
                error_text = error_data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    error_text = error_data.decode('latin-1')
                except UnicodeDecodeError:
                    error_text = error_data.decode('utf-8', errors='ignore')
            
            return {
                'status_code': e.code,
                'text': error_text
            }
        except Exception as e:
            raise Exception(f"HTTP请求失败: {str(e)}")

# 主API类
class Api:
    def __init__(self, globalArgd):
        self.provider = None
        self.http_client = None
        self.max_concurrent = globalArgd.get("max_concurrent", 3)
        self.executor = None
        
        # 保存全局配置
        self.global_config = globalArgd
        
        # 验证配置
        required_keys = ['provider', 'api_key']
        for key in required_keys:
            if key not in globalArgd or not globalArgd[key]:
                raise ValueError(f"缺少必需的配置项: {key}")
        
        print(f"AI OCR 插件初始化完成，使用服务商: {globalArgd['provider']}")
        
    def start(self, argd):
        """启动API"""
        try:
            # 获取配置
            provider_name = self.global_config.get("provider", "openai")
            api_key = self.global_config.get("api_key", "")
            api_base = self.global_config.get("api_base", "")
            model = self.global_config.get("model", "")
            timeout = self.global_config.get("timeout", 30)
            proxy_url = self.global_config.get("proxy_url", "")
            
            if not api_key:
                return "[Error] API密钥不能为空"
            
            # 创建Provider，使用内置的API基础URL
            self.provider = ProviderFactory.create_provider(
                provider_name, api_key, None, model, timeout, proxy_url
            )
            
            # 创建HTTP客户端
            self.http_client = HTTPClient(timeout, proxy_url)
            
            # 创建线程池
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent)
            
            # 保存局部配置
            self.local_config = argd
            
            return ""
        except Exception as e:
            return f"[Error] 启动失败: {str(e)}"
    
    def stop(self):
        """停止API"""
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None
    
    def testConnection(self):
        """测试连接"""
        try:
            # 创建一个简单的测试图像
            test_image = Image.new('RGB', (100, 50), color='white')
            buffer = BytesIO()
            test_image.save(buffer, format='JPEG')
            test_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # 发送测试请求
            result = self._run_ocr(test_base64, {"output_format": "text_only"})
            
            if result["code"] == 100 or result["code"] == 101:
                return {"code": 100, "data": "连接测试成功"}
            else:
                return {"code": 102, "data": result["data"]}
        except Exception as e:
            return {"code": 102, "data": f"连接测试失败: {str(e)}"}
    
    def runPath(self, imgPath: str):
        """处理图片路径"""
        try:
            with open(imgPath, 'rb') as f:
                image_bytes = f.read()
            return self.runBytes(image_bytes)
        except Exception as e:
            return self._create_error_result(f"读取图片失败: {str(e)}")
    
    def runBytes(self, imageBytes):
        """处理图片字节流"""
        try:
            image_base64 = base64.b64encode(imageBytes).decode('utf-8')
            return self.runBase64(image_base64)
        except Exception as e:
            return self._create_error_result(f"处理图片字节流失败: {str(e)}")
    
    def runBase64(self, imageBase64):
        """处理base64图片"""
        try:
            # 预处理图像
            processed_base64 = self._preprocess_image(imageBase64)
            
            # 执行OCR
            return self._run_ocr(processed_base64, self.local_config)
        except Exception as e:
            return self._create_error_result(f"OCR处理失败: {str(e)}")
    
    def _preprocess_image(self, image_base64):
        """预处理图像"""
        try:
            # 解码图像
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            
            # 转换为RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 调整图像大小
            max_size = self.local_config.get("max_image_size", 1536)
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # 调整图像质量
            quality_map = {
                "high": 95,
                "medium": 85,
                "low": 75,
                "auto": 85
            }
            quality = quality_map.get(self.local_config.get("image_quality", "auto"), 85)
            
            # 重新编码
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=quality, optimize=True)
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as e:
            # 如果预处理失败，返回原图像
            return image_base64
    
    def _run_ocr(self, image_base64, config):
        """执行OCR识别"""
        try:
            # 构建提示词
            prompt = self._build_prompt(config)
            
            # 发送请求
            max_retries = self.global_config.get("max_retries", 3)
            
            for attempt in range(max_retries + 1):
                try:
                    response_text = self._send_request(image_base64, prompt)
                    
                    # 解析响应
                    parsed_content = self.provider.parse_response(response_text)
                    
                    if parsed_content:
                        # 转换为Umi格式
                        return self._convert_to_umi_format(parsed_content, config)
                    else:
                        return self._create_empty_result()
                        
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    time.sleep(1)  # 重试前等待
                    
        except Exception as e:
            return self._create_error_result(str(e))
    
    def _build_prompt(self, config):
        """构建提示词"""
        language = config.get("language", "auto")
        output_format = config.get("output_format", "text_only")
        
        # 语言映射
        lang_map = {
            "auto": "自动检测语言",
            "zh": "中文",
            "en": "英文",
            "ja": "日文",
            "ko": "韩文",
            "fr": "法文",
            "de": "德文",
            "es": "西班牙文",
            "ru": "俄文",
            "ar": "阿拉伯文"
        }
        
        lang_instruction = lang_map.get(language, "自动检测语言")
        
        if output_format == "with_coordinates":
            prompt = f"""请识别图片中的所有文字内容，要求：
1. 识别语言：{lang_instruction}
2. 输出格式：JSON格式，包含文字内容和坐标信息
3. 坐标格式：每个文字块包含四个角点坐标 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
4. 输出结构：{{"texts": [{{"text": "文字内容", "box": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]}}]}}
5. 如果没有文字，返回：{{"texts": []}}

请直接返回JSON，不要包含其他说明文字。"""
        else:
            prompt = f"""请识别图片中的所有文字内容，要求：
1. 识别语言：{lang_instruction}
2. 输出格式：纯文本，保持原有的换行和格式
3. 如果没有文字，返回空字符串

请直接返回识别的文字内容，不要包含其他说明。"""
        
        return prompt
    
    def _send_request(self, image_base64, prompt):
        """发送API请求"""
        # 构建请求URL
        api_base = self.provider.api_base or self.provider.get_default_api_base()
        
        if self.global_config.get("provider") == "gemini":
            model = self.provider.model or self.provider.get_default_model()
            url = f"{api_base}/models/{model}:generateContent?key={self.provider.api_key}"
        else:
            url = f"{api_base}/chat/completions"
        
        # 构建请求头和载荷
        headers = self.provider.build_headers()
        payload = self.provider.build_payload(image_base64, prompt)
        
        # 发送请求
        response = self.http_client.post(url, headers, json.dumps(payload))
        
        if response['status_code'] != 200:
            raise Exception(f"API请求失败 (状态码: {response['status_code']}): {response['text']}")
        
        return response['text']
    
    def _convert_to_umi_format(self, content, config):
        """转换为Umi格式"""
        output_format = config.get("output_format", "text_only")
        
        if output_format == "with_coordinates":
            return self._parse_text_with_coordinates(content)
        else:
            return self._parse_text_only(content)
    
    def _parse_text_with_coordinates(self, content):
        """解析带坐标的文本"""
        try:
            # 尝试解析JSON
            if content.strip().startswith('{'):
                data = json.loads(content)
                if "texts" in data and isinstance(data["texts"], list):
                    result_data = []
                    for item in data["texts"]:
                        if "text" in item and "box" in item:
                            result_data.append({
                                "text": item["text"],
                                "box": item["box"],
                                "score": 1.0
                            })
                    
                    if result_data:
                        return {"code": 100, "data": result_data}
                    else:
                        return self._create_empty_result()
            
            # 如果不是JSON格式，尝试解析纯文本
            return self._parse_text_only(content)
            
        except Exception:
            # 解析失败，当作纯文本处理
            return self._parse_text_only(content)
    
    def _parse_text_only(self, content):
        """解析纯文本"""
        # 清理内容
        content = content.strip()
        
        if not content:
            return self._create_empty_result()
        
        # 按行分割文本
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not lines:
            return self._create_empty_result()
        
        result_data = []
        y_offset = 0
        
        for line in lines:
            # 为每行创建一个虚拟的边界框
            box = [[0, y_offset], [len(line) * 10, y_offset], 
                   [len(line) * 10, y_offset + 20], [0, y_offset + 20]]
            
            result_data.append({
                "text": line,
                "box": box,
                "score": 1.0
            })
            
            y_offset += 25
        
        return {"code": 100, "data": result_data}
    
    def _create_empty_result(self):
        """创建空结果"""
        return {"code": 101, "data": ""}
    
    def _create_error_result(self, error_msg):
        """创建错误结果"""
        return {"code": 102, "data": f"[Error] {error_msg}"}
