# 视频与公开仓库研究记录

研究日期：2026-10-11。区分：用户提供的标题、实际读取的公开资料、实测结果、我的建议。

## 五个链接的证据状态

| 用户给的线索 | 原始链接 | 本轮结果 |
| --- | --- | --- |
| 一只桌子：收藏的 GitHub 神器值得装吗 | https://v.douyin.com/zRIzwszZCz8/ | 短链接无法通过网页工具读取；浏览器跳到不相关的精选视频，不能视为目标内容 |
| 一只桌子：AI 不是变笨了，是工具太吵 | https://v.douyin.com/4R_ABFbHEKs/ | 网页无法读取，未取得字幕或完整正文 |
| 一只桌子：知识库为何 AI 不去翻 | https://v.douyin.com/o2Pfbfk49Zk/ | 网页无法读取，未取得字幕或完整正文 |
| 李小伊 Lee：Git 与 GitHub | https://v.douyin.com/wvlObxuem4o/ | 网页无法读取，未独立确认镜像课程及配套仓库 |
| 马克的技术工作坊：一个视频学会 Git + GitHub | https://v.douyin.com/zN-klztiY_k/ | 网页无法读取；找到同名公开视频的搜索线索及作者公开 MarkTodo 项目，不能确认短链接逐段对应 |

本轮没有看完五个目标视频，没有视频逐字稿或逐秒内容。接下来若要严格逐段复刻，需要可读取的视频文件、字幕或作者正文。仅凭标题不能确认视频的全部例子、发布日期和具体承诺。

## 已确认的作者公开资料

1. [一只桌子 GitHub 主页](https://github.com/duoduoler-ops)。仓库 README 同时列出“抖音 · 一只桌子”等作者渠道，因此与用户描述有较强对应证据。
2. [Table-GitHub-Capability-Router](https://github.com/duoduoler-ops/Table-GitHub-Capability-Router)：本次重点读取并下载实际源码，适合学习项目入库与按任务找能力。当前读取版本的 README 标为 v0.5.0；下载的是 main 分支 ZIP，不是固定 release 包。ZIP 哈希见 verification.md。
3. [Table-skills](https://github.com/duoduoler-ops/Table-skills)：查看公开 README。当前重点为项目交接；网页替身旧版已弃用，只保留设计思路。没有安装这个技能合集。
4. [Table-VideoSOP](https://github.com/duoduoler-ops/Table-VideoSOP)：查看公开 README，属于视频生产流程，与你本次个人资料库目标不同，未纳入执行部分。
5. [MarkTodo](https://github.com/MarkTechStation/MarkTodo)：作者的简单待办项目，适合作为 Git 练习素材。读取 README 和公开文件列表，没有运行应用，也没有复制其代码。本轮看不到明确 License，复制或发布其源码前应继续核对许可。

## 原版各环节怎么工作

| 环节 | 实际机制／边界 |
| --- | --- |
| 收链接 | new-project 把地址规范化、确定稳定 ID、创建候选卡；重复地址复用旧记录 |
| 评估 | 人或 Agent 阅读证据，填写实际用途和限制；脚本不会替你测试所有第三方项目 |
| 检索 | 短发现表和详细语义表供 Agent 读取、判断；这里不是已部署的向量数据库 |
| 能力登记 | 项目评级、安装范围、健康状态与调用方式分别记录；登记不等于真实安装 |
| 使用证据 | 关联版本、文件哈希和项目环境；实际任务的结果仍由执行者报告 |
| 写入维护 | CLI 管理锁、备份、事务清单和旧草稿哈希，减少误写 |
| validate | 核对资料与生成表的格式、一致性；不证明今天实际宿主能用某工具 |
| Hook | 可选提醒，需要客户端真正启用和触发；初始化不会自动接入 |

来源：[快速开始](https://github.com/duoduoler-ops/Table-GitHub-Capability-Router/blob/main/QUICKSTART.zh-CN.md)、[Agent 入口](https://github.com/duoduoler-ops/Table-GitHub-Capability-Router/blob/main/AGENT-START.md)、[使用证据说明](https://github.com/duoduoler-ops/Table-GitHub-Capability-Router/blob/main/docs/capability-lifecycle.md)。

## 逻辑和应用上的困难

**入口不等于可靠调用。** 一个目录规则只有被当前客户端加载并遵守才有用，跨客户端读取规则和技能发现的行为可能不同。实际验收应让新对话查一次库，检查它读取了哪个文件、为什么选择它。原版自己也说明真实 Hook 接入需额外验证。

**记录不等于验证。** “健康”标签、record-evidence 写入成功、一致性校验通过，都不是新的真实任务成功证明。必须留真实输入、输出和验收条件，避免用旧结论给新版本背书。

**压缩入口不等于无限扩展。** 短表能减少一开始的阅读量，但项目很多后仍会增加目录体积、语义冲突与更新负担。先测漏查率和误推荐，再升级全文检索或 RAG，不能只靠增加规则。

**证据有时效，也有维护成本。** 版本、权限和依赖会变化，人工更新记录需要时间。频繁全量重评会抵消工具带来的收益；应该只在任务、版本和环境实质变化时复查关键事实。

**原版保护机制有实际用途。** 并发锁、旧草稿拒绝和备份不是简单冗余；多人或自动写入时很有价值。你的精简版省略这些，就必须顺序编辑并依靠 Git 存档，不能假装获得同等可靠性。

## 精简决定

新库从零写了一个小型离线脚本，没有修改或删除作者源码。保留 Markdown、目录、去重、关键词查找、实际使用记录和 Git；暂不引入后台服务、自动安装、等级晋升、多客户端包装、可选 Hook、证据生命周期 JSON 和数据库。

这是基于个人入门目标的重新实现，不是对原版全部功能的等价复刻。作者源码保留在研究工作区，未打包进你的资料库；没有批量搬运第三方仓库。
