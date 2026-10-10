"""Regression checks using isolated copies; never changes installed CapCut drafts."""
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

class WindowsPortTests(unittest.TestCase):
    def test_transform_backup_and_unicode(self):
        import windows_backend as backend
        with tempfile.TemporaryDirectory() as tmp:
            original_root = backend.DRAFT_ROOT
            backend.DRAFT_ROOT = Path(tmp)
            try:
                spec = importlib.util.spec_from_file_location('bridge', Path(__file__).with_name('capcut-bridge.py'))
                bridge = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(bridge)
                bridge.app_pid = lambda: None
                bridge.quit_app = lambda: None
                folder = Path(tmp) / 'prueba'
                folder.mkdir()
                draft = {'duration': 1000000, 'materials': {'videos': [], 'texts': []},
                         'tracks': [{'type': 'video', 'flag': 0, 'segments': [{'material_id':'m', 'id':'s',
                         'target_timerange': {'start':0,'duration':1000000}, 'source_timerange':None,
                         'clip': {'scale': {'x':1,'y':1}, 'transform': {'x':0,'y':0}, 'rotation':0, 'alpha':1}}]}], 'name':'Vídeo español'}
                path = folder / 'draft_content.json'
                original = json.dumps(draft, ensure_ascii=False)
                path.write_text(original, encoding='utf-8')
                bridge.set_transform('prueba', 'main', 0, scale=1.2)
                changed = json.loads(path.read_text(encoding='utf-8'))
                self.assertEqual(changed['tracks'][0]['segments'][0]['clip']['scale']['x'],1.2)
                self.assertEqual(changed['name'], 'Vídeo español')
                self.assertEqual(changed['tracks'][0]['segments'][0]['source_timerange']['duration'],1000000)
                backups=list((Path(tmp)/'.bridge-backups').glob('*/draft_content.json'))
                self.assertEqual(len(backups),1)
                self.assertEqual(backups[0].read_text(encoding='utf-8'),original)
                with self.assertRaises(SystemExit):
                    bridge.edit_draft('../outside', lambda *args: None)
            finally:
                backend.DRAFT_ROOT=original_root

    def test_encrypted_draft_is_rejected(self):
        from windows_backend import validate_plaintext
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'draft_content.json'
            path.write_bytes(b'\xffencrypted')
            with self.assertRaises(SystemExit):
                validate_plaintext(path)

if __name__ == '__main__':
    unittest.main()
