# Git 和 GitHub：先会日常操作

依据：[GitHub 入门](https://docs.github.com/en/get-started/using-github/hello-world)、[上传本地代码](https://docs.github.com/en/migrations/importing-source-code-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github)、[Git revert](https://git-scm.com/docs/git-revert)、[Git restore](https://git-scm.com/docs/git-restore)。

## 一次存档怎么发生

```text
改文件 → 查看差异 → 选择本次要保存的文件 → commit 本地存档 → push 上传远端
```

工作区是你正在编辑的文件；暂存区是你选择纳入下一次存档的改动；提交历史是已经保存的版本。commit 和 push 是两步：断网也可以本地 commit。

在这个资料库目录运行：

```text
git status
git diff
git add notes/git-practice.md
git commit -m "记录第一次 Git 学习"
git log --oneline -5
```

这里只添加练习文件，避免把其他改动一并保存。修改资料卡时，先重建 INDEX.md，再把卡片和目录一起提交。如果提示需要身份，设置你希望公开在提交里的名字和邮箱；不要照抄别人。可以使用 GitHub 账号设置里的 noreply 邮箱。

## 上传到你的 GitHub

你的公开账号已核对为 [8j-design](https://github.com/8j-design)。本地库的建议仓库名是 `my-ai-library`。首次建议选择 **Private**，公开展示时再检查内容并调整可见性。

1. 登录 GitHub，选择 New repository，Owner 选 8j-design，Name 填 my-ai-library，Visibility 选 Private。
2. 若上传这个已有本地仓库，保持远端为空，**不要勾选创建 README、.gitignore、License**。
3. 创建成功后，在本地仓库执行下面命令。只有确实创建成功后才有这个远端地址。

```text
git remote -v
git remote add origin https://github.com/8j-design/my-ai-library.git
git push -u origin main
```

如果 origin 已存在，先检查其地址，不要重复 add。如果地址是你已确认的目标则直接 push。登录由 Git 的正规登录入口处理；不要把令牌发到聊天或写进远端 URL。GitHub 不支持用账号密码直接做 HTTPS Git 密码认证，见 [命令行认证](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#authenticating-with-the-command-line)。

4. 在 GitHub 页面确认能看到 README、INDEX、卡片和最新提交。云端上传完成以这一步为准。
5. 在另一个空目录克隆，确认资料能读、历史能查：

```text
git clone https://github.com/8j-design/my-ai-library.git
```

如果你已经把远端建成有初始 README 的仓库，最简单的处理是先克隆它，再把本地资料文件复制到克隆目录，检查、提交、推送；不要强制覆盖远端历史。

## 以后怎么同步

开始工作时先 `git status`。工作区干净时执行 `git pull --ff-only`；它在需要合并时会停下，让你看清原因。修改完成后检查、add、commit，再 `git push`。工作区有未保存的修改时先处理它们，别盲目 pull。

## 改坏了怎么撤销

| 情况 | 操作 | 结果 |
| --- | --- | --- |
| 已暂存，但不想放进这次提交 | `git restore --staged 文件名` | 从暂存区移出，编辑内容仍在 |
| 未提交，确实不要这个文件的修改 | `git restore 文件名` | 丢弃工作区中该文件的未暂存修改；先查看差异或另存副本 |
| 已提交，尤其已上传 | `git revert 提交编号` | 新建一条反向提交，保留历史 |

先用 `git log --oneline` 找提交编号。revert 遇到冲突时需要解决后继续，或者 `git revert --abort` 返回开始前。初学日常撤销先掌握这三种；不要默认使用 reset --hard 或强制推送。

## 想试一个新想法

工作区干净后：

```text
git switch -c experiment/new-card-format
```

在分支上修改和提交。满意后回到 main 合并：

```text
git switch main
git merge experiment/new-card-format
```

冲突表示同一位置有不同修改，需要选出正确内容，而不是让 AI 无条件“全部接受”。PR 是 GitHub 上让别人审阅分支修改的入口，不是本地存档所必需。

## 照着做后检查自己是否真会了

- 能解释为什么 commit 后还需要 push。
- 能只提交指定文件，而不是把全部改动都保存。
- 能读 diff 看出一段文字被改了什么。
- 能通过 revert 撤销一次测试提交，并解释历史为什么还在。
- 能从远端克隆资料库，再让 AI 找到一张合适卡片。
