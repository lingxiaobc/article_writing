"""
word_count.py — 文章字数与基础可读性统计
用法：python scripts/word_count.py <文件路径>
"""

import sys
import re


def count_chinese_chars(text: str) -> int:
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def count_words(text: str) -> int:
    # 英文单词数
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    # 中文字符数（每个字算一个词）
    chinese_chars = count_chinese_chars(text)
    return english_words + chinese_chars


def count_sentences(text: str) -> int:
    return len(re.findall(r'[。！？.!?]+', text))


def count_paragraphs(text: str) -> int:
    return len([p for p in text.split('\n\n') if p.strip()])


def analyze(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    total_chars = len(text)
    chinese_chars = count_chinese_chars(text)
    word_count = count_words(text)
    sentences = count_sentences(text)
    paragraphs = count_paragraphs(text)
    avg_sentence_len = round(word_count / sentences, 1) if sentences else 0

    print("=" * 40)
    print(f"文件：{filepath}")
    print("=" * 40)
    print(f"总字符数（含空格）：{total_chars}")
    print(f"中文字符数：        {chinese_chars}")
    print(f"总词数（中+英）：   {word_count}")
    print(f"句子数：            {sentences}")
    print(f"段落数：            {paragraphs}")
    print(f"平均句长（词）：    {avg_sentence_len}")
    print("=" * 40)

    if avg_sentence_len > 50:
        print("⚠  平均句长过长，建议拆分长句以提升可读性")
    if paragraphs > 0 and word_count / paragraphs > 200:
        print("⚠  段落平均字数偏多，建议控制在150字以内")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python word_count.py <文件路径>")
        sys.exit(1)
    analyze(sys.argv[1])
