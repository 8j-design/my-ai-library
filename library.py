"""Small offline Markdown catalogue. Python 3.10+, standard library only."""
import argparse
import hashlib
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
FIELDS = ('链接', '标签', '一句话用途', '状态', '检查日期')
STATES = ('待核查', '仅参考', '已验证', '已停用')


def canonical(value):
    url = urlsplit(value.strip())
    parts = url.path.strip('/').split('/')
    if url.scheme != 'https' or url.netloc.lower() != 'github.com' or len(parts) < 2:
        raise ValueError('请使用 https://github.com/作者/仓库 地址')
    owner, repo = parts[:2]
    repo = repo.removesuffix('.git')
    if not re.fullmatch(r'[A-Za-z0-9-]+', owner) or not re.fullmatch(r'[A-Za-z0-9_.-]+', repo) or repo in ('.', '..'):
        raise ValueError('仓库地址格式不正确')
    return f'https://github.com/{owner.lower()}/{repo.lower()}'


def atomic_write(path, text):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(text)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def records(root):
    result = []
    for path in sorted((root / 'cards').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        fields = dict(re.findall(r'^- (链接|标签|一句话用途|状态|检查日期)：(.*)$', text, re.M))
        if any(not fields.get(key, '').strip() for key in FIELDS):
            raise ValueError(f'{path.name} 缺少必填字段')
        if fields['状态'] not in STATES or canonical(fields['链接']) != fields['链接']:
            raise ValueError(f'{path.name} 状态或规范地址不正确')
        date.fromisoformat(fields['检查日期'])
        title = next((line[2:] for line in text.splitlines() if line.startswith('# ')), '')
        if not title:
            raise ValueError(f'{path.name} 缺少标题')
        result.append((path, title, fields, text))
    urls = [item[2]['链接'] for item in result]
    if len(set(urls)) != len(urls):
        raise ValueError('发现重复仓库地址，请合并卡片后再重建目录')
    return result


def index_text(root):
    rows = ['# 项目目录', '', '由 library.py index 生成；修改资料卡后重建。收藏状态不代表已经安装。', '', '| 项目 | 用途 | 检索词 | 状态 |', '| --- | --- | --- | --- |']
    for path, title, fields, _ in records(root):
        values = (f'[{title}](cards/{path.name})', fields['一句话用途'], fields['标签'], fields['状态'])
        rows.append('| ' + ' | '.join(value.replace('|', '／') for value in values) + ' |')
    return '\n'.join(rows) + '\n'


def add(root, url, title, tags, summary):
    for value in (title, tags, summary):
        if not value.strip() or '\n' in value or '\r' in value:
            raise ValueError('标题、标签、用途不能为空，也不能包含换行')
    normalized = canonical(url)
    for path, _, fields, _ in records(root):
        if fields['链接'] == normalized:
            return path, False
    folder = root / 'cards'
    folder.mkdir(exist_ok=True)
    identifier = hashlib.sha256(normalized.encode()).hexdigest()[:16]
    path = folder / f'{identifier}.md'
    content = f'# {title}\n\n- 链接：{normalized}\n- 标签：{tags}\n- 一句话用途：{summary}\n- 状态：待核查\n- 检查日期：{date.today().isoformat()}\n\n## 什么时候用\n\n待补充具体任务和预期产物。\n\n## 什么时候不用\n\n待补充排除条件。\n\n## 证据与限制\n\n只登记链接；没有自动联网、安装或验证。原始地址：{url.strip()}\n\n## 实际使用记录\n\n尚未实际使用。记录日期、版本、输入、结果、验收方式与下一步。\n'
    with path.open('x', encoding='utf-8') as handle:
        handle.write(content)
    atomic_write(root / 'INDEX.md', index_text(root))
    return path, True


def search(root, query):
    terms = [term.casefold() for term in query.split() if term.strip()]
    if not terms:
        raise ValueError('请填写至少一个检索词')
    matches = []
    for path, title, fields, text in records(root):
        if fields['状态'] == '已停用':
            continue
        searchable = ((title, 4), (fields['标签'], 3), (fields['一句话用途'], 2))
        score = sum(weight for value, weight in searchable for term in terms if term in value.casefold())
        if score:
            matches.append((score, path.name, title, fields['状态']))
    return sorted(matches, key=lambda item: (-item[0], item[1]))[:3]


def main():
    parser = argparse.ArgumentParser(description='离线资料库：入库、关键词检索、重建目录、检查')
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('add')
    create.add_argument('url')
    for key in ('title', 'tags', 'summary'):
        create.add_argument('--' + key, required=True)
    find = commands.add_parser('search')
    find.add_argument('query')
    commands.add_parser('index')
    commands.add_parser('check')
    args = parser.parse_args()
    try:
        if args.command == 'add':
            path, created = add(ROOT, args.url, args.title, args.tags, args.summary)
            print(('已创建：' if created else '已存在，未覆盖：') + path.name)
        elif args.command == 'search':
            matches = search(ROOT, args.query)
            for _, filename, title, state in matches:
                print(f'{title} | {state} | cards/{filename}')
            if not matches:
                print('没有匹配资料；尝试短关键词或请 Agent 阅读 INDEX.md 判断。')
        elif args.command == 'index':
            atomic_write(ROOT / 'INDEX.md', index_text(ROOT))
            print('目录已重建')
        else:
            expected = index_text(ROOT)
            if not (ROOT / 'INDEX.md').exists() or (ROOT / 'INDEX.md').read_text(encoding='utf-8') != expected:
                raise ValueError('目录缺失或过期，请运行 index')
            print(f'检查通过：{len(records(ROOT))} 张卡片，无重复地址，目录一致。此检查不验证工具可用性。')
        return 0
    except (OSError, ValueError) as error:
        print(f'检查失败：{error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
