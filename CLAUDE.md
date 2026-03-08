# 文章写作项目 — 项目记忆

## 项目定位
本项目专用于公众号文章的撰写、优化与配图管理。所有技能、命令和智能体均存放于 `.claude/` 目录。

---

## 核心技能

| 技能 | 触发方式 | 说明 |
|------|----------|------|
| `optimize-article` | 提供文章链接/路径，或说"优化文章"、"润色" | 全面优化公众号文章，含结构、语言、逻辑，并为每个大板块自动生成手绘信息图 |
| `physics-lecture` | 提供物理草稿/大纲，或说"写物理讲义" | 针对40-50分学生，以费曼风格编写高中物理讲义 |
| `cover-generator` | 说"请为{文章路径}生成封面"，或说"生成封面图" | 根据文章生成公众号封面图：含IP形象（Q版小猫）+ 标题艺术字，简约彩色风格，2.35:1比例 |

---

## 技能关键文件

### optimize-article
- **技能逻辑**：`.claude/skills/optimize-article/SKILL.md`
- **优化原则**：`.claude/skills/optimize-article/principles.md`（用户自定义规则）
- **写作参考**：`.claude/skills/optimize-article/references/`（检查清单、风格指南）
- **输出模板**：`.claude/skills/optimize-article/assets/`
- **生图脚本**：`.claude/skills/optimize-article/scripts/infographic_generator.py`（调用 Gemini API 生成手绘信息图）
- **子智能体**：`.claude/agents/article-critic.md`（文章评审，在第二步被调用）

### physics-lecture
- **技能逻辑**：`.claude/skills/physics-lecture/SKILL.md`
- **写作原则**：`.claude/skills/physics-lecture/principles.md`（费曼风格、结构规范）
- **学生画像**：`.claude/skills/physics-lecture/student-profile.md`（40-50分学生痛点分析）
- **讲义模板**：`.claude/skills/physics-lecture/assets/lecture_template.md`

### cover-generator
- **技能逻辑**：`.claude/skills/cover-generator/SKILL.md`
- **生图脚本**：`.claude/skills/cover-generator/scripts/cover_generator.py`（调用 Gemini API，传入IP形象参考图生成封面）
- **IP形象原图**：`.claude/skills/IP_character/IP_character.jpg`（所有封面的IP参考图，造型不可更改）
- **封面风格**：简约彩色，不超过3种主色，背景纯色/渐变为主，禁止堆砌复杂元素

---

## 重要约定

- **API Key**：Gemini API Key 存放于 `.claude/settings.local.json` 的 `env.GEMINI_API_KEY`，脚本自动读取，无需手动配置
- **保存策略**：优化/生成完成后，自动在 `draft/` 目录下创建以文章标题命名的文件夹，文章和配图分别存放在该目录及其 `image/` 子目录中
- **语言跟随**：中文文章输出中文，英文文章输出英文
- **目录命名规范**：去除 Windows 不允许的字符（`\ / : * ? " < > |`），长度不超过 50 个字符

---

## 工作流程规范（适用于所有技能与任务）

- **执行前确认**：执行任何任务前，必须先向用户详细说明将要执行的流程、步骤与目标，等待用户确认或给出建议后，方可正式开始
- **终端命令说明**：每次调用 Bash 执行终端命令前，须向用户说明该命令的具体作用，不得静默执行
- **不确定即汇报**：遇到任何不确定、没把握、拿不准的情况，必须立即向用户汇报并说明疑虑，不得擅自推进或凭猜测处理

---

## 长文档写入规范（适用于所有技能与任务）

### 核心原则

**禁止边思考边写入**：当需要写入的文档或文字内容**超过 200 行**时，严格遵循以下流程，不得边思考边写入文件。

### 标准流程

1. **第一步：编写框架**
   - 先构思完整的文档框架（大纲、章节结构、核心要点）
   - 将框架写入文件，作为文档骨架
   - 等待用户审核框架，确认无误后再继续

2. **第二步：逐板块填充内容**
   - 按框架顺序，逐个板块思考并填充内容
   - 每完成一个板块，立即写入文件
   - 不要一次性思考所有板块，避免"手没跟上脑子"

3. **第三步：全文检查**
   - 所有板块填充完成后，**必须**通读全文
   - 检查板块之间的衔接是否自然
   - 检查逻辑是否合理、前后是否一致
   - 发现问题立即修正

### 子代理并行处理

**适用场景**：当任务中有多个独立的板块（板块之间关联性不强、可独立完成）时，可使用子代理并行处理。

**操作方法**：
- 将独立板块分配给不同的子代理
- 每个子代理独立完成自己的板块
- 所有子代理完成后，主进程汇总结果
- 汇总后**必须**进行全文检查，确保板块之间衔接合理

**示例场景**：
- 优化多篇独立文章
- 生成多个独立的配置文件
- 编写多个独立的功能模块文档

### 判断标准

**如何判断是否超过 200 行？**
- 预估文档最终行数（包括空行、代码块、列表等）
- 如果不确定，按"可能超过 200 行"处理
- 宁可多一步框架审核，也不要冒险边想边写

**如何判断板块是否独立？**
- 板块之间没有强依赖关系（A 板块不需要 B 板块的结果）
- 板块可以独立理解和完成
- 板块的顺序可以调整而不影响整体逻辑

### 违规后果

如果违反此规范导致文档出现以下问题：
- 内容不完整或突然中断
- 板块之间逻辑不连贯
- 前后矛盾或重复

**必须**：
1. 向用户说明问题原因
2. 按标准流程重新编写
3. 将此次错误记录到项目记忆中，避免再犯

---

## Git 操作约束

### 绝对禁止的操作
- **只允许在本地 Commit，绝对不允许自动执行 `git push`**：所有的推送到云端（GitHub）的操作，必须留给用户手动执行。
- 不要执行 `git reset` 或删除历史记录的操作。

### 出现错误时的回滚提示
- 如果你修改的代码导致了运行报错，或者用户表示对修改不满意，请主动提示用户可以使用 `git reset --hard HEAD~1` 或提供相应的 Git 命令来撤销刚才的自动提交。

---

## 项目结构

```
article_writing/
├── CLAUDE.md
├── draft/                        ← 文章草稿存储目录
│   └── [文章标题]/               ← 每篇文章独立目录（以文章标题命名）
│       ├── [文章标题].md         ← 优化后的文章
│       └── image/                ← 该文章的配图目录
│           ├── generated_xxx_1.png
│           ├── generated_xxx_2.png
│           └── ...
├── generated_images/             ← 图片生成默认输出目录（已废弃，保留兼容）
└── .claude/
    ├── settings.json
    ├── settings.local.json          ← 存放 GEMINI_API_KEY（私有，勿提交）
    ├── skills/
    │   ├── IP_character/
    │   │   └── IP_character.jpg     ← 公用IP形象参考图（Q版小猫）
    │   ├── optimize-article/
    │   │   ├── SKILL.md
    │   │   ├── principles.md
    │   │   ├── scripts/
    │   │   │   ├── infographic_generator.py
    │   │   │   ├── word_count.py
    │   │   │   └── extract_outline.py
    │   │   ├── references/
    │   │   └── assets/
    │   ├── physics-lecture/
    │   │   ├── SKILL.md
    │   │   ├── principles.md
    │   │   ├── student-profile.md
    │   │   └── assets/
    │   │       └── lecture_template.md
    │   └── cover-generator/
    │       ├── SKILL.md
    │       └── scripts/
    │           └── cover_generator.py
    ├── commands/
    │   ├── optimize.md              ← /optimize
    │   ├── physics-lecture.md       ← /physics-lecture
    │   └── cover.md                 ← /cover
    └── agents/
        └── article-critic.md        ← 文章评审子智能体
```

---

## 目录用途说明

| 目录 | 说明 |
|------|------|
| `draft/` | 文章草稿存储目录，每篇文章一个独立子文件夹（以文章标题命名），包含优化后文章及配套图片 |
| `draft/[文章标题]/` | 单篇文章的独立目录，包含文章文件和 `image/` 子目录 |
| `draft/[文章标题]/image/` | 该文章的所有配图存放目录 |
| `generated_images/` | 图片生成默认输出目录（已废弃，保留兼容） |
| `.obsidian/` | Obsidian 笔记软件配置，用于 Markdown 编辑与预览 |

---

## 依赖环境

图片生成脚本需要以下 Python 依赖：

```bash
pip install google-genai pillow
```

脚本会自动从环境变量读取 `GEMINI_API_KEY`（配置在 `.claude/settings.local.json`）。

---

## 常用脚本命令

| 功能 | 命令 |
|------|------|
| 生成文章封面 | `python .claude/skills/cover-generator/scripts/cover_generator.py "标题" "IP行为描述" [输出目录]` |
| 生成信息图 | `python .claude/skills/optimize-article/scripts/infographic_generator.py "提示词" [输出目录]` |
| 统计文章字数 | `python .claude/skills/optimize-article/scripts/word_count.py <文件路径>` |
| 提取文章大纲 | `python .claude/skills/optimize-article/scripts/extract_outline.py <文件路径>` |
