---
title: LinkedIn grow workflow diagnosis
created: 2026-04-25
type: diagnosis
---

## Summary

The Task Scheduler trigger is correctly configured and has been firing every weekday at 08:30 NZST. The pipeline is not stalled: it ran successfully on Apr 20, 21, 22, 23, and 24, producing output folders for each day. The user's impression that it "stopped after one run" is not supported by the session folder evidence. However, there are real reliability gaps: Apr 21 and 22 session folders are empty (no candidates.json, no drafts.json), Apr 23 produced candidates but an empty drafts.json (`[]`), and Apr 24 was the only day with a posted comment. These failures point to three distinct root causes: (1) the `claude -p` subprocess failing silently on some runs, (2) the headed Playwright browser being killed when the laptop lid closes mid-scout, and (3) the 30-minute Task Scheduler execution time limit being tight for a headed browser plus multiple `claude -p` calls in sequence.

---

## Root causes

**RC-1: Headed Playwright browser is killed when the laptop closes mid-run.**

`config/playwright_settings.py` sets `HEADLESS = False` (required to avoid LinkedIn bot detection). `CLAUDE.md` confirms: "tools/browser.get_browser_context() must stay headed". A headed Chromium window requires an active Windows desktop session. When the laptop lid closes, Windows may suspend the display session or put the machine to sleep before the 30-minute execution limit expires. Even with `WakeToRun` set, a sleep that occurs _during_ a run (not before it) terminates the headed browser mid-execution. Evidence: Apr 21 and 22 output folders are completely empty -- the session folder was created (`new_session_folder()` runs before scout) but no `candidates.json` was written, meaning the Playwright scout phase crashed before returning anything. The `atexit` flush handler would still write an empty `grow_log.json` entry.

**RC-2: `claude -p` subprocess fails silently, producing empty drafts.**

Apr 23 has two candidates in `candidates.json` but `drafts.json` is `[]`. That exact pattern means `draft_comments_for_candidates()` ran but every `_invoke_claude()` call either raised an exception (logged to stderr and skipped) or returned non-JSON output. Evidence from `execute_scheduled_log.json`: on Apr 22 a separate pipeline logged `"GH draft failed: claude -p exited 1; stderr: . Continuing without GH comments."` -- exit 1 with empty stderr. This is the `claude -p` subscription-mode invocation failing, likely because Claude Code requires an interactive terminal/session and is not available in a background Task Scheduler run.

The `.env` strips `ANTHROPIC_API_KEY` intentionally (`_invoke_claude` removes it so `claude -p` uses the subscription rather than API key). But `claude -p` in subscription mode requires the user to be authenticated and may require an interactive session. In a Task Scheduler background run, this authentication may not be available.

**RC-3: The 30-minute execution time limit is too tight.**

The task XML shows `<ExecutionTimeLimit>PT30M</ExecutionTimeLimit>`. A full run involves: headed Playwright browse across multiple target profiles (scout), multiple `claude -p` calls for drafting (2 minutes each, up to 8 candidates = 16 minutes), a second `claude -p` pass for self-critique per draft, and SMTP for the digest. On a slow day or with 8 candidates, total runtime easily exceeds 30 minutes. Windows Task Scheduler hard-kills the process when the limit is hit, leaving log files incomplete and the session folder partially written.

**RC-4 (secondary): The `LogonType` is `InteractiveToken`, which requires an active user session.**

The task XML shows `<LogonType>InteractiveToken</LogonType>`. This means the task only runs when the user (reonz) is logged in. It will not run from a locked screen or hibernate. `WakeToRun` will wake the machine from sleep, but if the machine goes back to sleep before the user session is fully active, the task may fire into a degraded state. This compounds RC-1.

**RC-5 (secondary): No structured logging to file -- failures disappear.**

`grow_run.py` writes all diagnostic output to `sys.stderr`, which Task Scheduler captures only if a log file redirect is configured in the task action. There is no `--log` flag and no log file path in the task command. Failed runs produce no accessible error log. The only evidence available is the partial session folder contents.

---

## Proposed fixes

### Fix for RC-1 and RC-4: Switch Task Scheduler logon type to run-whether-logged-on-or-not

This is the primary fix. Change the task to run as a background service-style task that does not require an interactive desktop session. For the Playwright headed-browser requirement, this is contradictory: a truly headless task cannot run a headed browser. The pragmatic fix is to add explicit machine sleep prevention during the run.

**Option A (preferred): Add a PowerShell sleep-block wrapper around the run.**

Replace the task action with a wrapper that prevents sleep during the run and redirects stderr to a log file.

Proposed new task command (update `scripts/install_grow_scheduler.ps1` line 73):

```powershell
# Before (line 73 in install_grow_scheduler.ps1):
$cmdLine = "/c cd /d `"$RepoRoot`" && `"$PythonPath`" `"$ScriptRel`""

# After:
$wrapperPath = Join-Path $RepoRoot "scripts\run_grow_with_sleep_block.ps1"
$cmdLine = "-NonInteractive -ExecutionPolicy Bypass -File `"$wrapperPath`""
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $cmdLine -WorkingDirectory $RepoRoot
```

New file `scripts/run_grow_with_sleep_block.ps1`:

```powershell
# Prevent Windows sleep during the grow run.
# Add-Type to call SetThreadExecutionState before launching Python.
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class SleepBlock {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
    public const uint ES_CONTINUOUS = 0x80000000;
    public const uint ES_SYSTEM_REQUIRED = 0x00000001;
    public const uint ES_DISPLAY_REQUIRED = 0x00000002;
    public static void Prevent() {
        SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED);
    }
    public static void Allow() {
        SetThreadExecutionState(ES_CONTINUOUS);
    }
}
"@

[SleepBlock]::Prevent()

$repoRoot = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $repoRoot "temporary\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir ("grow_run_" + (Get-Date -Format "yyyy-MM-dd") + ".log")

$python = "C:\Users\reonz\AppData\Local\Programs\Python\Python312\python.exe"
& $python (Join-Path $repoRoot "scripts\grow_run.py") 2>&1 | Tee-Object -FilePath $logFile

[SleepBlock]::Allow()
```

**Option B: Increase execution time limit and add explicit sleep inhibitor in Python.**

In `grow_run.py` main(), add a ctypes call to block sleep before the scout phase:

```python
# Add near the top of main() in grow_run.py, before Phase 2:
import ctypes
try:
    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)
except Exception:
    pass  # Non-Windows or unsupported; safe to skip

# ... existing code ...

# At the end of main(), before return 0:
try:
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
except Exception:
    pass
```

### Fix for RC-2: Redirect stderr to a log file and diagnose `claude -p` in background

Add stderr capture to the task action so errors are visible. This does not fix the underlying claude issue but enables diagnosis.

In `scripts/install_grow_scheduler.ps1`, change line 73:

```powershell
# Before:
$cmdLine = "/c cd /d `"$RepoRoot`" && `"$PythonPath`" `"$ScriptRel`""

# After (adds stderr+stdout redirect to a dated log file):
$logDir = Join-Path $RepoRoot "temporary\logs"
$cmdLine = "/c cd /d `"$RepoRoot`" && mkdir `"$logDir`" 2>nul && `"$PythonPath`" `"$ScriptRel`" >> `"$logDir\grow_run_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.log`" 2>&1"
```

Note: `%DATE%` formatting is locale-dependent on Windows. A more robust alternative is the PowerShell wrapper in Option A above, which uses `Get-Date -Format "yyyy-MM-dd"`.

To diagnose whether `claude -p` works in a Task Scheduler context, run this test manually from a fresh `cmd.exe` (not a terminal that already has the Claude session):

```cmd
cd C:\Users\reonz\cursor\LinkedIn
"C:\Users\reonz\AppData\Local\Programs\Python\Python312\python.exe" -c "import subprocess; r = subprocess.run(['C:/Users/reonz/.local/bin/claude.exe', '-p', '--output-format', 'text'], input='Say hello', capture_output=True, text=True, timeout=30); print('RC:', r.returncode); print('OUT:', r.stdout[:200]); print('ERR:', r.stderr[:200])"
```

If `claude -p` exits 1 in non-interactive mode, the fix is to set `ANTHROPIC_API_KEY` in `.env` as a fallback (uncomment the second key on line 6) and remove the key-stripping logic in `_invoke_claude`, or configure `claude` with a persistent auth token that does not require an interactive session.

### Fix for RC-3: Increase execution time limit

In `scripts/install_grow_scheduler.ps1`, change the `ExecutionTimeLimit`:

```powershell
# Before (line 80):
-ExecutionTimeLimit (New-TimeSpan -Minutes 30)

# After:
-ExecutionTimeLimit (New-TimeSpan -Minutes 90)
```

Re-run `install_grow_scheduler.ps1` to apply. This gives a full run (8 targets, two claude passes each, browser, SMTP) a 3x safety margin.

### Fix for RC-5: Add persistent log file from the outset

Add this block near the top of `grow_run.py`, immediately after the `ROOT` definition (around line 63):

```python
# Redirect stderr to a persistent daily log so Task Scheduler runs leave evidence.
import io
_LOG_DIR = ROOT / "temporary" / "logs"
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_log_path = _LOG_DIR / f"grow_run_{datetime.now(NZ_TZ).strftime('%Y-%m-%d')}.log"
try:
    _log_fh = _log_path.open("a", encoding="utf-8", buffering=1)
    sys.stderr = io.TextIOWrapper(
        io.FileIO(str(_log_path), "a"),
        encoding="utf-8",
        line_buffering=True,
    )
except Exception:
    pass  # If log file can't be opened, fall back to original stderr
```

Note: this redirects stderr only; stdout is already visible in the Task Scheduler last-run result. A simpler alternative is to use the PowerShell wrapper in RC-1 Fix Option A which captures both streams.

---

## Quick test to confirm fix

1. **Confirm task fires and logs**: After applying the log-redirect fix (RC-5), manually trigger the task from an elevated terminal: `Start-ScheduledTask -TaskName LinkedIn_Grow_Run`. Wait 5 minutes, then check `temporary/logs/grow_run_YYYY-MM-DD.log` for evidence of run progress.

2. **Confirm sleep block works**: Close the laptop lid 1 minute after manually triggering the task. Open it 10 minutes later. Check whether the log file shows continuous output through to Phase 7, or stops abruptly.

3. **Confirm `claude -p` in background**: Run the diagnostic command in Fix for RC-2 from a plain `cmd.exe` (not Claude Code terminal). If exit code is non-zero, the API key fallback fix is needed.

4. **Check grow_log.json date coverage**: After a week of runs, verify `temporary/grow_log.json` has entries for every weekday. Gaps indicate the session was killed before Phase 7 (the log write).

---

## Assumptions

- The "ran successfully once then stopped" description from the task context is likely referring to Apr 20 grow-2 being the first clean run, with Apr 21 and 22 appearing broken. The task was actually firing daily; the failures were silent because stderr was not captured.
- Apr 21 empty session folder: created by `new_session_folder()` then scout crashed (likely lid-close mid-Playwright). The folder was created at 08:30 but no files were written.
- Apr 22 empty session folder: same pattern, same cause.
- Apr 23 candidates written but empty drafts: scout succeeded but all `claude -p` calls failed (exit 1 with empty stderr, matching the execute_scheduled_log.json pattern from the same day).
- Apr 24 full success (1 comment posted): run completed; laptop stayed open; `claude -p` worked.
- The `li_at` session cookie expires 2027-04-15: LinkedIn auth is not the cause of failures.
- No virtual environment is present: Python packages are installed to the system Python312 install. This is fine for Task Scheduler as long as the packages are installed globally.
- `ANTHROPIC_API_KEY` is present in `.env` but stripped by `_invoke_claude`. If `claude -p` requires an interactive login session to use subscription mode, this stripping is the cause of RC-2.

All output is a first draft for human review.
