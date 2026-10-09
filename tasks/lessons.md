# Lessons

## 2026-10-09: don't route work back through a tool the user is leaving
- **What happened:** after the site was rebuilt locally, I prepared a ZIP and instructions for re-uploading it to ChatGPT Sites. The user wanted ChatGPT dropped entirely, with the local folder as the master and a replacement hosted copy.
- **Rule:** when the user says "replace that site" or similar, confirm *where* the replacement should live before preparing hand-offs to the old platform. Default to hosting I can manage (a private claude.ai artifact, built with `make_artifact.py`), and treat the old platform only as something the user removes themselves.
