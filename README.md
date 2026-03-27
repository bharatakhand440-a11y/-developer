# Smart Study Assistant

A friendly and interactive **smart study assistant** for students preparing at IIT level.

## Features

- Clean, interactive UI (Streamlit).
- Summarizes study notes into concise key points.
- Generates challenging IIT-style conceptual/practical questions.
- Assesses level from performance (`weak`, `intermediate`, `intelligent`).
- Personalized suggestions:
  - YouTube channels/playlists
  - Standard books
  - Improvement strategy tailored to level
- Explanation mode that adapts to student understanding level.
- Customizable distraction restriction workflow (demo model).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

The distraction blocker in this version is a safe simulation (no OS-level process killing).
You can integrate real mobile/desktop APIs later for production-grade enforcement.
