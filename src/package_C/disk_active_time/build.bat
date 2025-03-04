gcc -fPIC -shared "./main.c" -o "../../../lib/disk_active_time.dll" -lpdh


@REM === Test C Code ===

@REM chcp 65001
@REM gcc "./main.c" -o "./main.exe" -lpdh
@REM main.exe
@REM pause
