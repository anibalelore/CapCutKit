$bridgePath = Join-Path $PSScriptRoot 'capcut-bridge.py'
& uv run $bridgePath @args
exit $LASTEXITCODE
