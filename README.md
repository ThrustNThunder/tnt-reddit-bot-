# TNT Reddit Bot

Reddit promotion bot for the [Thrust N Thunder](https://www.youtube.com/@ThrustNThunder) YouTube channel.

## What it does

- Posts new video reviews to relevant subreddits (r/Starlink, r/boondocking, r/vandwellers, r/overlanding, etc.)
- Monitors comments on posted content so the channel owner can respond quickly
- Tailors post copy to each subreddit community

## Setup

```bash
pip install -r requirements.txt
```

Set environment variables:
```bash
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret
export REDDIT_PASSWORD=your_password
```

## Usage

**Post a new video:**
```bash
python bot.py post \
  --title "PeakDo LinkPower 2 Review" \
  --url "https://youtu.be/zRHLKrFD1n0" \
  --product "PeakDo LinkPower 2"
```

**Dry run (preview posts without submitting):**
```bash
python bot.py post --title "..." --url "..." --product "..." --dry-run
```

**Monitor recent comments:**
```bash
python bot.py monitor
```

## Subreddits

- r/Starlink
- r/boondocking
- r/vandwellers
- r/overlanding
- r/GoRVing
- r/camping
- r/SolarDIY
- r/boating
- r/sailing
- r/Liveaboard
- r/fishing
