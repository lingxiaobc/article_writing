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
- **保存策略**：优化/生成完成后默认询问用户是否保存，不自动覆盖原文件
- **语言跟随**：中文文章输出中文，英文文章输出英文
- **封面输出目录**：默认在文章所在目录下创建 `cover/` 子文件夹

---

## 工作流程规范（适用于所有技能与任务）

- **执行前确认**：执行任何任务前，必须先向用户详细说明将要执行的流程、步骤与目标，等待用户确认或给出建议后，方可正式开始
- **终端命令说明**：每次调用 Bash 执行终端命令前，须向用户说明该命令的具体作用，不得静默执行
- **不确定即汇报**：遇到任何不确定、没把握、拿不准的情况，必须立即向用户汇报并说明疑虑，不得擅自推进或凭猜测处理

---

## 项目结构

```
article_writing/
├── CLAUDE.md
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
