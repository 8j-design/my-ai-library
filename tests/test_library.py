import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('library', Path(__file__).resolve().parents[1] / 'library.py')
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)


class BehaviourTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def add(self, url='https://github.com/Example/Tool'):
        return lib.add(self.root, url, '练习项目', 'Git 存档', '学习提交历史')

    def test_readding_variant_preserves_user_notes(self):
        path, _ = self.add()
        original = path.read_text(encoding='utf-8') + '\n我的实际记录：成功。\n'
        path.write_text(original, encoding='utf-8')
        second, created = self.add('https://github.com/example/tool.git?tab=readme')
        self.assertFalse(created)
        self.assertEqual(second, path)
        self.assertEqual(path.read_text(encoding='utf-8'), original)
        self.assertEqual(len(lib.records(self.root)), 1)

    def test_invalid_urls_do_not_create_cards(self):
        for url in ('https://evil.test/a/b', 'https://github.com.evil.test/a/b', 'https://github.com/a/..', 'http://github.com/a/b'):
            with self.assertRaises(ValueError):
                self.add(url)
        self.assertFalse((self.root / 'cards').exists())

    def test_subpage_canonicalized_to_repository(self):
        self.assertEqual(lib.canonical('https://github.com/Owner/Repo/tree/main/docs'), 'https://github.com/owner/repo')

    def test_search_handles_chinese_and_retired(self):
        path, _ = self.add()
        self.assertEqual(len(lib.search(self.root, '存档')), 1)
        self.assertEqual(lib.search(self.root, '不存在的词'), [])
        text = path.read_text(encoding='utf-8').replace('- 状态：待核查', '- 状态：已停用')
        path.write_text(text, encoding='utf-8')
        self.assertEqual(lib.search(self.root, '存档'), [])

    def test_negative_conditions_do_not_become_positive_matches(self):
        path, _ = self.add()
        path.write_text(path.read_text(encoding='utf-8') + '\n不适用：知识库。\n', encoding='utf-8')
        self.assertEqual(lib.search(self.root, '知识库'), [])

    def test_stale_directory_is_visible(self):
        path, _ = self.add()
        initial = (self.root / 'INDEX.md').read_text(encoding='utf-8')
        path.write_text(path.read_text(encoding='utf-8').replace('学习提交历史', '学习分支'), encoding='utf-8')
        self.assertNotEqual(initial, lib.index_text(self.root))

    def test_duplicate_records_are_rejected(self):
        path, _ = self.add()
        (path.parent / 'duplicate.md').write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
        with self.assertRaises(ValueError):
            lib.records(self.root)


if __name__ == '__main__':
    unittest.main()
