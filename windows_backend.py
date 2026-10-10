"""Windows filesystem/lifecycle support. Interactive UI uses Codex Computer Use."""
import ctypes
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import psutil

DRAFT_ROOT = Path(os.environ.get('CAPCUT_DRAFT_ROOT', str(Path(os.environ['LOCALAPPDATA']) / 'CapCut/User Data/Projects/com.lveditor.draft')))
DRAFT_FILE = 'draft_content.json'

def app_pid():
    return next((p.pid for p in psutil.process_iter(['name']) if (p.info['name'] or '').lower() == 'capcut.exe'), None)

def launch_app():
    exe = Path(os.environ.get('CAPCUT_EXE', str(Path(os.environ['LOCALAPPDATA']) / 'CapCut/Apps/CapCut.exe')))
    if not exe.is_file():
        raise SystemExit(f'CapCut executable missing: {exe}; set CAPCUT_EXE')
    subprocess.Popen([str(exe)], cwd=exe.parent)

def quit_app(timeout=20):
    """Request a normal close; never force-kill or discard a pending save."""
    pids = {p.pid for p in psutil.process_iter(['name']) if (p.info['name'] or '').lower() == 'capcut.exe'}
    if not pids:
        return
    user32 = ctypes.windll.user32
    user32.PostMessageW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_ssize_t)
    def close(hwnd, _):
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(ctypes.c_void_p(hwnd), ctypes.byref(pid))
        if pid.value in pids and user32.IsWindowVisible(ctypes.c_void_p(hwnd)):
            user32.PostMessageW(hwnd, 0x0010, 0, 0)
        return True
    user32.EnumWindows(callback_type(close), 0)
    deadline = time.monotonic() + timeout
    while app_pid() is not None:
        if time.monotonic() >= deadline:
            raise SystemExit('CapCut is still running. Close it normally and retry; no draft was written.')
        time.sleep(0.25)

def unsupported(*args, **kwargs):
    raise SystemExit('This live command uses macOS accessibility IDs. On Windows use Codex Computer Use; file commands are supported.')

ax_app = attr = geometry = walk = elements = find_one = ensure_front = click_at = click_element = send_key = read_playhead = timeline_clips = seek = select_clip = grab = unsupported

def backup(folder):
    root = DRAFT_ROOT / '.bridge-backups'
    target = root / f'{folder.name}-{time.time_ns()}'
    target.mkdir(parents=True)
    # Preserve native caches and all project metadata, but avoid copying source videos.
    for item in folder.iterdir():
        if item.name == 'Resources':
            continue
        if item.is_dir():
            shutil.copytree(item, target / item.name)
        else:
            shutil.copy2(item, target / item.name)
    registry = DRAFT_ROOT / 'root_meta_info.json'
    if registry.exists():
        shutil.copy2(registry, target / 'root_meta_info.snapshot.json')
    return target

def validate_plaintext(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f'{path} is not editable JSON (possibly encrypted). No changes made.') from exc
    if not isinstance(data, dict) or 'tracks' not in data or 'materials' not in data:
        raise SystemExit(f'Unsupported draft schema: {path}')
    return data

def extract_templates(name, target):
    draft = validate_plaintext(DRAFT_ROOT / name / DRAFT_FILE)
    materials = draft['materials']
    texts = {m['id']: m for m in materials.get('texts', [])}
    animations = {m['id']: m for m in materials.get('material_animations', [])}
    for track in draft['tracks']:
        for segment in track['segments']:
            material = texts.get(segment['material_id'])
            animation = next((animations[r] for r in segment.get('extra_material_refs', []) if r in animations), None)
            if material and animation:
                target.mkdir(parents=True, exist_ok=True)
                for filename, value in [('text-material.json', material), ('text-segment.json', segment), ('text-ref-material_animations.json', animation)]:
                    (target / filename).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
                print(f'Text templates extracted from {name}')
                return
    raise SystemExit('No text segment with animation references found; add styled text in CapCut first.')

def doctor():
    print(json.dumps({'platform': 'windows', 'draft_root': str(DRAFT_ROOT),
        'capcut_running': app_pid() is not None, 'drafts': [p.parent.name for p in DRAFT_ROOT.glob('*/draft_content.json')],
        'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe'),
        'live_control': 'Codex Computer Use'}, indent=2))
