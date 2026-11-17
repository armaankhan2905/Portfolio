# Armaan Khan — Portfolio

Open `dist/index.html` through a static server:

```powershell
python -m http.server 8080 --bind 127.0.0.1 --directory dist
```

Visit `http://127.0.0.1:8080/`. The published files are in `dist/` and do not need a build step. Edit `dist/index.html` for profile information and `dist/projects.js` for projects, categories and action links. The résumé PDF and its PNG preview are in `dist/assets/`; update both when replacing the résumé.

Run `node scripts/check.mjs` to check the project data and assets. The résumé PDF and cutting mat SVG can be regenerated with `python scripts/make_assets.py` (requires ReportLab).
