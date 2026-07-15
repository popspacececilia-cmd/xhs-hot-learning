---
name: xhs-hot-learning
description: Analyze pre-collected Xiaohongshu breakout-post, benchmark-note, and creator-profile packages through a reusable evidence-first workflow. Use when Codex needs to match upstream Lingzao results to an XHS inbox, identify note versus profile packages, select up to 10 account-relevant high-performing posts from provided creator data, build text/image/video/data fact sheets, analyze title-content mechanisms, separate observations from inferences, generate account-specific transfer ideas and candidate rules, hand results to a personal account-operation skill, or update a source record from 待处理 to 已处理 only after successful persistence. This skill consumes existing collection results and must not call Lingzao itself.
---

# 小红书爆款学习

把用户主动收集、且已由上游完成采集的小红书素材包转换成可追溯的事实底稿、机制判断、原创迁移建议和候选规则。不要把“爆款”理解成结果保证；本 skill 学习公开样本，不承诺复制数据表现。

## 核心分层

始终按以下顺序工作：

```text
素材收件箱 + 上游素材包
-> 输入匹配与完整性检查
-> 完整事实底稿
-> 关系与机制分析
-> 账号适配与原创迁移
-> 候选规则和内容机会
-> 写入目标账号工作区
-> 更新源素材状态
```

运行时可以综合判断，保存时必须分开：可见事实、推断、不确定项、候选规则、账号私有规则和验证结果。

## 开始前

1. 使用用户在任务中指定的收件箱目录；未指定时先询问，不猜测本地路径。确认目标账号工作区和单次处理上限。
2. 读取目标账号的定位、受众、表达偏好、阶段目标和已有规则；没有账号工作区时只输出通用分析，不虚构账号适配。
3. 读取 [references/inbox-and-capture.md](references/inbox-and-capture.md) 将收件箱记录与上游素材包匹配并检查缺失项。
4. 读取 [references/field-source-matrix.md](references/field-source-matrix.md) 判断每个底稿字段来自上游素材包、文本推断还是本地视频补充。
5. 识别到账号主页素材包时，读取 [references/profile-link-workflow.md](references/profile-link-workflow.md) 从已提供的近期笔记中筛选最多 10 篇高相关、高数据笔记。
6. 读取 [references/analysis-framework.md](references/analysis-framework.md) 建立底稿并分析机制。
7. 需要写入个人运营 skill、生成候选规则或更新状态时，读取 [references/persistence-and-lifecycle.md](references/persistence-and-lifecycle.md)。
8. 每日运行或每周五生成下周选题时，读取 [references/daily-and-weekly-operations.md](references/daily-and-weekly-operations.md)。

## 输入与工具边界

- 上游已提供单篇笔记素材包：直接复用笔记详情、逐字稿、评论和平台数据，不重新采集。
- 上游已提供账号主页素材包：从已提供的账号资料和近期笔记列表中筛选最多 10 篇；优先明显爆款，并在账号目录下管理子样本。
- 收件箱只有链接、没有对应素材包：记录缺失输入并等待上游补充，不调用平台采集工具，不把链接本身当作完整素材。
- 用户另行提供本地视频：可补充真实镜头、关键帧、OCR、字幕、声音和节奏，但必须作为独立证据来源。
- 账号适配：读取目标账号的项目本地资料，不把一个账号的私有偏好写入通用规则。

本 skill 不调用 Lingzao，也不执行搜索、笔记详情获取、主页内容获取或评论拉取。只分析上游已经返回并交付的字段；缺失项保留为空或“未获取”，并在输出中列入待补充清单。上游没有提供的镜头、关键帧、声音、字幕样式和节奏不得编造，等待本地视频或新的上游素材包补充。

## 分析原则

- 完整清单用于防漏，不能替代深入分析。
- 每篇只深挖 3-5 个核心机制，不把所有特点都升级为技巧。
- 分开分析标题结构、标题钩子、内容结构和内容钩子，再检查标题、封面、开头、过程和结果的承接关系。
- 热点工具、用户问题、个人判断和结果价值可以相辅相成，不预设谁必须位于前台。
- 数据只能支持倾向，不证明因果；轻微数据和时长差异若不改变判断可忽略。
- 原创迁移检查新问题、新判断、新方法、新经验、新证据和新表达，尤其保留账号自己的同意、反对、条件和取舍。
- 制作成本根据账号阶段和内容任务判断，由用户做最终决策。

## 规则边界

- 单篇素材产生的规则只能是 `candidate`。
- 优先给已有规则补证据和适用范围，不创建同义重复规则。
- 不自动批准、验证、删除或固化规则。
- 时间钩子、结果先行、流程图、固定镜头节奏、真人出镜和资料领取等都是候选策略，不是普适硬规则。
- 通用 skill 保存分析方法；账号定位、语言、人设和已验证偏好留在账号私有工作区。

## 完成条件

只有在上游素材包校验、事实底稿、机制分析、账号迁移、候选规则/内容机会和目标工作区记录全部保存成功后，才将源记录中的状态改为 `已处理`。

使用脚本：

```bash
python3 scripts/inbox_status.py scan --inbox-dir "/absolute/inbox/path"
python3 scripts/inbox_status.py mark --file "/absolute/inbox/path/素材.txt" --url "https://..."
```

脚本只负责识别记录和安全更新状态，不负责上游采集或分析。输入缺失、任务中断、无法定位唯一记录或写入校验失败时保持原状态。

## 输出

每篇输出并保存：

1. 来源和完整事实底稿。
2. 3-5 个核心机制及证据、不确定性和替代解释。
3. 可借鉴、不可照搬和账号适配结论。
4. 原创迁移建议。
5. 最多 3-5 条候选规则。
6. 最多 3 个内容机会。
7. 缺失项、待确认问题和处理状态。

普通汇报只说明新增数、成功数、重复数、失败数、核心判断、候选规则、内容机会和需要用户补充的事项。不要展示冗长 JSON、命令或内部实现，除非用户要求。

## 硬性边界

- 只处理用户主动提供或保存的公开链接。
- 不调用 Lingzao 或其他平台采集工具；只消费上游已经提供的素材包。
- 不批量监控平台，不绕过访问控制。
- 不编造标题、正文、指标、评论、逐字稿、画面、经验或案例。
- 不自动发布。
- 不把管线验证生成物称为正式内容。
- 不修改源记录中除 `状态` 值以外的用户内容。
