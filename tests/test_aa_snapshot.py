import contextlib
import datetime as dt
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import aa_snapshot as snapshot


def payload(date=None):
    return {'generated_at': date or dt.date.today().isoformat(),
            'data': [{'name': 'Model', 'slug': 'model', 'evaluations': {'artificial_analysis_intelligence_index': 20}}]}


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root / 'aa-snapshot.json'

    def main(self, *args):
        with mock.patch.object(sys, 'argv', ['aa_snapshot.py', '--dir', str(self.root), *map(str, args)]), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return snapshot.main()

    def test_check_rejects_bad_dates_and_invalid_data(self):
        for date, data in [('bad', [{'name': 'x', 'slug': 'x'}]), (None, [{'name': 'x', 'slug': 'x'}]),
                           ((dt.date.today() + dt.timedelta(days=1)).isoformat(), [{'name': 'x', 'slug': 'x'}]),
                           (dt.date.today().isoformat(), 'invalid'),
                           (dt.date.today().isoformat(), []),
                           (dt.date.today().isoformat(), [None]),
                           (dt.date.today().isoformat(), [{'name': 'x', 'slug': 'x', 'pricing': []}])]:
            with self.subTest(date=date, data=data):
                self.cache.write_text(json.dumps({'generated_at': date, 'data': data}), encoding='utf-8')
                self.assertEqual(self.main('--check'), 1)
        self.cache.write_text(json.dumps(payload()), encoding='utf-8')
        self.assertEqual(self.main('--check'), 0)

    def test_file_preserves_date_and_bad_input_preserves_cache(self):
        old = (dt.date.today() - dt.timedelta(days=60)).isoformat()
        source = self.root / 'source.json'
        source.write_text(json.dumps(payload(old)), encoding='utf-8')
        self.assertEqual(self.main('--from-file', source), 0)
        self.assertEqual(json.loads(self.cache.read_text(encoding='utf-8'))['generated_at'], old)
        self.assertEqual(self.main('--check'), 1)
        before = self.cache.read_bytes()
        md = (self.root / 'aa-snapshot.md').read_bytes()
        for data in ({'generated_at': old, 'data': [None]}, {'data': [{'name': 'x', 'slug': 'x'}]}, []):
            source.write_text(json.dumps(data), encoding='utf-8')
            self.assertEqual(self.main('--from-file', source), 4)
            self.assertEqual(self.cache.read_bytes(), before)
            self.assertEqual((self.root / 'aa-snapshot.md').read_bytes(), md)
        source.write_text('{', encoding='utf-8')
        self.assertEqual(self.main('--from-file', source), 4)
        self.assertEqual(self.cache.read_bytes(), before)

    def test_shared_schema_rejects_duplicates_and_negative_values(self):
        source = self.root / 'source.json'
        good = payload()
        self.cache.write_text(json.dumps(good), encoding='utf-8')
        before = self.cache.read_bytes()
        for models in ([{'name': 'a', 'slug': 'same'}, {'name': 'b', 'slug': 'same'}],
                       [{'name': 'a', 'slug': 'a', 'pricing': {'price_1m_input_tokens': -1}}],
                       [{'name': 'a', 'slug': 'a', 'performance': {'median_time_to_first_token_seconds': -1}}],
                       [{'name': 'missing slug'}]):
            with self.subTest(models=models):
                invalid = {'generated_at': good['generated_at'], 'data': models}
                source.write_text(json.dumps(invalid), encoding='utf-8')
                self.assertEqual(self.main('--from-file', source), 4)
                self.assertEqual(self.cache.read_bytes(), before)
                self.cache.write_text(json.dumps(invalid), encoding='utf-8')
                self.assertEqual(self.main('--check'), 1)
                self.cache.write_bytes(before)

    def test_negative_max_age_is_rejected(self):
        with self.assertRaises(SystemExit) as exc:
            self.main('--check', '--max-age-days', '-1')
        self.assertEqual(exc.exception.code, 2)

    def test_fetch_malformed_json_and_timeout(self):
        for response, code in [(io.BytesIO(b'{'), 4), (TimeoutError('timeout'), 3)]:
            with self.subTest(code=code), mock.patch.object(snapshot.urllib.request, 'urlopen') as urlopen, \
                 contextlib.redirect_stderr(io.StringIO()):
                if isinstance(response, Exception):
                    urlopen.side_effect = response
                else:
                    urlopen.return_value = response
                with self.assertRaises(SystemExit) as exc:
                    snapshot.fetch_all('unused')
                self.assertEqual(exc.exception.code, code)

    def test_fetch_rejects_truncated_pagination(self):
        body = json.dumps({'data': [{'name': 'x', 'slug': 'x'}], 'pagination': {'has_more': True}}).encode()
        with mock.patch.object(snapshot, 'MAX_PAGES', 2), \
             mock.patch.object(snapshot.urllib.request, 'urlopen', side_effect=lambda *a, **k: io.BytesIO(body)) as call, \
             contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
            snapshot.fetch_all('unused')
        self.assertEqual(exc.exception.code, 4)
        self.assertEqual(call.call_count, 2)

    def test_render_failure_does_not_replace_cache(self):
        self.cache.write_text('original', encoding='utf-8')
        source = self.root / 'source.json'
        source.write_text(json.dumps(payload()), encoding='utf-8')
        with mock.patch.object(snapshot, 'render_markdown', side_effect=ValueError('bad render')):
            self.assertEqual(self.main('--from-file', source), 4)
        self.assertEqual(self.cache.read_text(encoding='utf-8'), 'original')

    def test_atomic_write_preserves_file_on_replace_failure(self):
        self.cache.write_text('original', encoding='utf-8')
        with mock.patch.object(snapshot.os, 'replace', side_effect=OSError('failed')):
            with self.assertRaises(OSError):
                snapshot.atomic_write(self.cache, 'new')
        self.assertEqual(self.cache.read_text(encoding='utf-8'), 'original')
        self.assertEqual(list(self.root.iterdir()), [self.cache])


if __name__ == '__main__':
    unittest.main()
