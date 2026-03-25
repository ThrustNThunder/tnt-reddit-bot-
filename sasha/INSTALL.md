# How to Deploy Sasha's Rebuild

Jon prepared these files. Michael installs them.

## Steps

1. On your Mac, find Sasha's OpenClaw workspace directory
   - Usually: `~/.openclaw/workspace/` or wherever her agent files live
   - Check with: `ls ~/.openclaw/agents/`

2. Copy these files into her workspace:
   - `SOUL.md`
   - `USER.md`
   - `MEMORY.md`
   - `AGENTS.md`

3. Create the memory folder if it doesn't exist:
   ```bash
   mkdir -p ~/.openclaw/workspace/memory
   ```

4. Restart Sasha's session (close TUI, reopen)

5. Sasha will read the files on startup and wake up knowing exactly who she is and who you are.

## What Changes

- No more amnesia between sessions
- No more hallucinating technical solutions (that's Jon's job now)
- No more asking who you are
- Clear role: creative only, not technical

## If Something Looks Wrong

Ping Jon via WhatsApp or TUI — he'll fix it.
