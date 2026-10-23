import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]


class PortabilityTests(unittest.TestCase):
    def test_relocation_and_missing_asset(self):
        # Keep temporary files under the workspace; do not depend on sandbox TEMP.
        with tempfile.TemporaryDirectory(prefix='relocated-',dir=ROOT/'desktop/build') as name:
            destination=Path(name)/'春喜 moved project'
            (destination/'desktop').mkdir(parents=True)
            for folder in ('src','assets','config'):
                shutil.copytree(ROOT/'desktop'/folder,destination/'desktop'/folder,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(ROOT/'desktop/run.py',destination/'desktop/run.py')
            shutil.copytree(ROOT/'shared/sprites',destination/'shared/sprites')
            command=[sys.executable,str(destination/'desktop/run.py'),'--check']
            result=subprocess.run(command,cwd=ROOT/'desktop/build',capture_output=True,text=True,timeout=20)
            self.assertEqual(result.returncode,0,result.stderr+result.stdout)
            self.assertTrue(json.loads(result.stdout)['ok'])
            (destination/'shared/sprites/dozing.png').unlink()
            result=subprocess.run(command,cwd=ROOT/'desktop/build',capture_output=True,text=True,timeout=20)
            self.assertEqual(result.returncode,1,result.stderr+result.stdout)
            self.assertFalse(json.loads(result.stdout)['ok'])

    def test_lite_snapshot_and_original_art_intact(self):
        manifest=json.loads((ROOT/'shared/sprites/provenance.json').read_text(encoding='utf-8'))
        for name,info in manifest.items():
            path=ROOT/name if name.startswith('lite/') else ROOT/'shared/sprites'/name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),info['sha256'])
            self.assertTrue(info['unchanged_copy'])
        installed=Path.home()/'.codex/pets/chunxi'
        if all((installed/name).exists() for name in ('pet.json','spritesheet.webp')):
            for name in ('pet.json','spritesheet.webp'):
                self.assertEqual((installed/name).read_bytes(),(ROOT/'lite'/name).read_bytes())


if __name__=='__main__':
    unittest.main(verbosity=2)
