import base64
import json
import requests
from modelscope.utils.mcp import McpBase


class UmiOcrMcp(McpBase):
    """
    UmiOcrMcp类，用于通过HTTP接口与本地运行的Umi-OCR v2服务进行交互。
    """

    def __init__(self):
        super().__init__()

    def run(self, **kwargs):
        """
        MCP 的主执行函数。

        Args:
            **kwargs: 从 configuration.json 定义的输入参数。
                - image_base64 (str): 必需，图片的 base64 编码。
                - lang (str, optional): 识别语言。默认为 'zh-Hans'。
                - layout (str, optional): 排版方式。默认为 'auto'。
                - server_address (str, optional): Umi-OCR 服务地址。默认为 'http://127.0.0.1:1502'。

        Returns:
            dict: 包含 'text' 和 'result' 的字典。
        """
        # 1. 解析输入参数
        image_base64 = kwargs.get('image_base64')
        lang = kwargs.get('lang', 'zh-Hans')
        layout = kwargs.get('layout', 'auto')
        server_address = kwargs.get('server_address', 'http://127.0.0.1:1502')

        if not image_base64:
            raise ValueError("输入错误：'image_base64' 是必填项。")

        # 2. 构建请求体 (Payload)
        # 参考 Umi-OCR HTTP 接口手册构建请求
        api_url = f"{server_address}/api/ocr"
        headers = {'Content-Type': 'application/json'}

        payload = {
            "base64": image_base64,
            "options": {
                "lang": lang,
                # 注意：Umi-OCR的排版参数键名是 'tbpu.parser'
                "tbpu.parser": layout
            }
        }

        # 3. 发送 HTTP POST 请求
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status()  # 如果状态码不是 2xx，则抛出异常
        except requests.exceptions.RequestException as e:
            # 处理网络错误或Umi-OCR服务未启动的情况
            error_message = f"调用Umi-OCR服务失败，请确保Umi-OCR v2已启动并开启HTTP服务。地址: {api_url}。错误详情: {e}"
            raise ConnectionError(error_message)

        # 4. 解析并处理返回结果
        response_data = response.json()

        # 检查Umi-OCR返回的业务状态码
        if response_data.get('code') != 100:
            error_message = f"Umi-OCR处理失败。代码: {response_data.get('code')}, 消息: {response_data.get('message')}"
            raise RuntimeError(error_message)

        # 提取纯文本内容
        ocr_results = response_data.get('data', [])
        concatenated_text = "\n".join([item.get('text', '') for item in ocr_results])

        # 5. 返回符合 configuration.json 定义的输出
        return {
            'text': concatenated_text,
            'result': response_data
        }


# 本地测试代码
if __name__ == '__main__':
    # 使用一个简单的白色背景黑色文字 "Test" 图片的 base64 进行测试
    # 注意：你需要替换成你自己的图片base64编码
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAAAyCAYAAACqNX6+AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACnSURBVHhe7dixDQAhDEPB/4d6qYfgQoGDBTrTB/fecwEAAAAAAAAAAAAAAPCbO/fBvSgKAAAAAAAAAAAAAAD4y5374F5UBQAAAAAAAAAAAAAA/OVOffAvaqIAAAAAAAAAAAAAAPjLnfvgXlQFAAAAAAAAAAAAAAB85c598C9qogAAAAAAAAAAAAAA/nKnPvgXtVEAAAAAAAAAAAAAAMBfd+6De1EUAAAAAAAAAAAAAADwmzv3wb2oCgAAAAAAAAAAAADgX3d+A9o8BRs2/SHTAAAAAElFTkSuQmCC"

    mcp = UmiOcrMcp()
    try:
        # 模拟调用
        result = mcp.run(image_base64=test_image_base64, lang='en')
        print("======== 识别成功 ========")
        print("【纯文本结果】:")
        print(result['text'])
        print("\n【完整JSON结果】:")
        print(json.dumps(result['result'], indent=2, ensure_ascii=False))
    except (ValueError, ConnectionError, RuntimeError) as e:
        print(f"======== 识别失败 ========\n{e}")