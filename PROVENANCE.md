# Origin and Windows adaptation

This repository builds on [matt-j-penny/capcut-kit](https://github.com/matt-j-penny/capcut-kit), original commit `304c125`, whose history is preserved here.

The Windows adaptation adds `windows_backend.py`, `capcut.ps1`, platform-specific dependency selection and dispatch in `capcut-bridge.py`, isolated regression tests, and Windows documentation. It was used with CapCut Desktop 9.3.0 on Windows.

The file lane supports native JSON drafts, normal application shutdown, backups, media placement, transforms, overlays and keyframes. The original macOS accessibility commands remain macOS-only. Windows visual interaction uses the separately installed Codex Computer Use plugin.

Source footage, personal CapCut drafts, generated video assets, local caches and FFmpeg binaries are not included. Install FFmpeg and FFprobe or place their executables under `tools/bin`.

The upstream repository at the imported commit did not contain a project license. This adaptation does not assign a new license to upstream code. Bundled Inter fonts retain their included OFL notice.
