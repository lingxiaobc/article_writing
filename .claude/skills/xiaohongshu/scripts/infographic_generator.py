# To run this code you need to install the following dependencies:
# pip install google-genai
#
# 用法：python ai_studio_code.py "生图提示词" [输出目录]
# 参数1：生图提示词（必填）
# 参数2：图片输出目录（可选，默认使用项目根目录下的 generated_images/）
# 若不传任何参数则使用默认测试提示词

import mimetypes
import os
import sys
import datetime
from google import genai
from google.genai import types

_default_output = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "generated_images")
OUTPUT_DIR = sys.argv[2] if len(sys.argv) > 2 else _default_output
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def generate():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "请根据以下主题生成一张手绘笔记风格的图片：人工智能改变教育的三个核心方式：个性化学习、即时反馈、全球资源共享。"

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3.1-flash-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="MINIMAL",
        ),
        image_config = types.ImageConfig(
            aspect_ratio="16:9",
            image_size="1K",
        ),
        response_modalities=[
            "IMAGE",
        ],
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""## 角色（Role）        

-你是一名专业的 手绘笔记艺术家和信息设计师。        

## 任务（Task）        

-生图。字体设计,有创意,创意手绘字,文字排版艺术,手写字线条细,线条圆润,冲击力,艺术构图,先锋艺术,极致清晰,极简主义,简约高级,杰作。        

-基于我发布的内容图片，创建一张清晰、简洁的 手绘笔记风格的手绘草图图像，画风要有很强的手绘感        

-旨在帮助读者快速把握其内在逻辑和核心要点。  

- **背景纯白，禁止有多余多东西，比如黑板边框，手稿纸边框等**      

## 步骤（Steps）        

-阅读并提取“关键节点”（角色/动作/结果/条件），按流程或因果关系进行组织；        -确保每一幅图都有一个清晰、简短的主题，把主题用大字表现，并确保视觉集中。不要在一幅手绘图中提供过多信息，不要让视觉过于拥挤。        

-用简洁的中文关键词命名其他关键节点，确保文字书写正确、措辞易于理解，字号要比主题小至少一级。不要在一张图里放太多文字。文字是次要的，插图才是第一优先。        

-根据 #核心要求 创建图像。        

-让生成效果更简洁。        

-填满画布以保证视觉均衡，不要过度居中。        

## 核心要求（Core Requirements）        

-视觉风格：严格遵循 手绘笔记的手绘风格。所有元素都应具有手写感。使用干净、极简的线条，并配合简单图标。整体感觉应像用彩色铅笔在白板或笔记本上绘制。        

-构图与布局：整体布局必须清晰、简洁、有逻辑，能自然引导读者视线。布局不需要严格遵循从左到右或从上到下；合理自由地安排元素，并确保它们之间有足够的空间。严格避免箭头重叠；确保视觉不混乱。        

-颜色：黑色为主要素描线条，以确保视觉清晰，但可用其他颜色（如红色用于强调、绿色或黄色用于装饰），保持整体简洁；纯白色背景，高对比度；不使用渐变、不使用阴影、不使用照片/3D/拟物风格。

- 所有文字为简体中文        

-尺寸：始终保持16：9比例。        

## 输出目标（Output Goal）        

生成一张极简手绘草图，能清晰解释原文的核心思想，让任何看到这张图的人都能快速理解其主要内容。

**背景纯白，禁止有多余多东西，比如黑板边框，手稿纸边框等**"""),
        ],
    )

    file_index = 0
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.parts is None
        ):
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            file_index += 1
            inline_data = chunk.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            file_name = os.path.join(OUTPUT_DIR, f"generated_{timestamp}_{file_index}{file_extension}")
            save_binary_file(file_name, data_buffer)
        else:
            print(chunk.text)

if __name__ == "__main__":
    generate()


