# Editing the PAM visualization

The public, standalone page is `simulations/pam.html`. The homepage links to it as a standalone interactive page. The simulation has already been computed; visitors only load the saved data.

To change its title, descriptions, caption, or equation:

1. Edit `_pam/copy.json`.
2. From the repository root, run `python3 _pam/update_captions.py`.
3. Commit the modified copy file and `simulations/pam.html`, then publish through the normal website workflow.

The update script uses only Python's standard library, finishes quickly, and checks that the embedded simulation data are unchanged. It does not rerun Julia, require NumPy, or recompress numerical arrays. The `_pam` directory is not included in the generated Jekyll website.

The model coefficients, initial data, and trajectory are fixed numerical data. Changing those requires a new simulation, not just different captions. The model description on the page is intentionally concise.

`equation_mathml` contains native MathML, and `equation_accessible_text` provides its accessible description. The page works without external plotting libraries or API calls. No numerical backend is required on GitHub Pages.
