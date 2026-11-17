# Armaan Khan — Portfolio

Open `dist/index.html` through a static server:

```powershell
python -m http.server 8080 --bind 127.0.0.1 --directory dist
```

Visit `http://127.0.0.1:8080/`. The published files are in `dist/` and do not need a build step. Edit `dist/index.html` for profile information and `dist/projects.js` for projects, categories and action links. The résumé PDF and its PNG preview are in `dist/assets/`; update both when replacing the résumé.

Run `node scripts/check.mjs` to check the project data and assets. Regenerate the cutting mat with `python scripts/make_assets.py`. The updated résumé is authored by `scripts/update_resume.py`; after regeneration, render both PDF pages to replace `resume.png` and `resume-page-2.png`.

