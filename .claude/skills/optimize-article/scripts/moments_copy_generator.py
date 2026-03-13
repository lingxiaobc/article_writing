#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朋友圈文案生成脚本

用法：python moments_copy_generator.py <文章文件路径>
功能：根据优化后的公众号文章生成 200 字左右的朋友圈推广文案

依赖：pip install google-genai
"""

import os
import sys
from google import genai
from google.genai import types


def read_article(file_path):
    """读取文章内容"""
    if not os.path.exists(file_path):
        print(f"错误：文件不存在 - {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def extract_title(content):
    """提取文章标题（第一个 # 标题）"""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return "未命名文章"


def generate_moments_copy(article_content, article_title):
    """调用 Gemini API 生成朋友圈文案"""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("错误：未找到 GEMINI_API_KEY 环境变量")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # 构建提示词
    prompt = f"""请根据以下公众号文章生成一段朋友圈推广文案。

文章标题：{article_title}

文章内容：
{article_content[:3000]}  # 只取前 3000 字符，避免超长

---

要求：
1. 字数控制在 180-220 字
2. 开头用钩子吸引注意（提问 / 痛点 / 反常识观点）
3. 中间点出核心价值（解决什么问题 / 带来什么启发）
4. 结尾引导点击（悬念 / 行动召唤）
5. 语气口语化，符合朋友圈场景，像朋友在分享而非广告
6. 避免标题党和过度营销感
7. 可以适当使用 emoji，但不要过多（最多 2-3 个）
8. 不要使用"点击阅读原文"等明显的广告用语，改用更自然的引导方式

请直接输出文案正文，不要包含任何标题、说明或格式标记。"""

    # 调用 API
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,  # 稍高的温度以获得更有创意的文案
            max_output_tokens=500,
        )
    )

    return response.text.strip()


def generate_hashtags(article_title, article_content):
    """生成话题标签建议"""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return []

    client = genai.Client(api_key=api_key)

    prompt = f"""请根据以下文章标题和内容，生成 2-3 个适合朋友圈的话题标签。

文章标题：{article_title}

文章内容摘要：
{article_content[:1000]}

要求：
1. 标签要简短（2-6 个字）
2. 标签要有传播性和话题性
3. 标签要与文章主题相关
4. 每个标签前加 # 符号
5. 直接输出标签，用空格分隔，不要其他说明

示例输出格式：#AI工具 #效率提升 #产品思维"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=100,
        )
    )

    return response.text.strip()


def main():
    if len(sys.argv) < 2:
        print("用法：python moments_copy_generator.py <文章文件路径>")
        sys.exit(1)

    article_path = sys.argv[1]

    # 读取文章
    print(f"正在读取文章：{article_path}")
    article_content = read_article(article_path)
    article_title = extract_title(article_content)
    print(f"文章标题：{article_title}")

    # 生成文案
    print("\n正在生成朋友圈文案...")
    moments_copy = generate_moments_copy(article_content, article_title)

    # 生成标签
    print("正在生成话题标签...")
    hashtags = generate_hashtags(article_title, article_content)

    # 输出结果
    print("\n" + "="*50)
    print("朋友圈文案")
    print("="*50)
    print()
    print(moments_copy)
    print()
    print("---")
    print()
    print(f"话题标签建议：{hashtags}")
    print()
    print("配图建议：使用文章中的信息图，或文章封面图")
    print()
    print("="*50)

    # 保存到文件
    output_dir = os.path.dirname(article_path)
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(article_path))[0]}_朋友圈文案.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("## 朋友圈文案\n\n")
        f.write(moments_copy)
        f.write("\n\n---\n\n")
        f.write(f"**话题标签建议：** {hashtags}\n\n")
        f.write("**配图建议：** 使用文章中的信息图，或文章封面图\n")

    print(f"\n文案已保存到：{output_file}")


if __name__ == "__main__":
    main()
