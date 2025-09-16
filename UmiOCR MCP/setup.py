from setuptools import setup, find_packages

setup(
    name='modelscope-mcp-umi-ocr',
    version='0.1.0',
    description='A ModelScope Community Package to call the Umi-OCR HTTP API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kaz',
    author_email='your.email@example.com',
    url='https://github.com/4965898/UmiOCR-AI-OCR-Plugin/tree/patch-1/UmiOCR%20MCP',  # 替换成你的代码仓库地址
    packages=find_packages(),
    install_requires=[
        'modelscope',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)