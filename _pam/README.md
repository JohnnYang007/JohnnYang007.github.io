# Editing the PAM visualization

The gasket selector is `simulations/pam.html`. Its **Initial condition and noise
strength** selector loads `pam-delta.html` (point mass, λ = 2.5),
`pam-hat.html` (harmonic hat, λ = 2.5), or `pam-hat-low.html` (the same hat and
Brownian increments, λ = 0.5). All three offer natural-log and linear views.
The Researches page links to the standalone overview `simulations/fractal-pam.html`
using `_includes/pam-simulation.html`. The overview links to the gasket selector
and two standalone carpet views. The carpet files are saved simulations; the site
does not run their numerical solvers.

Share direct gasket choices using `simulations/pam.html?initial=delta`,
`simulations/pam.html?initial=hat`, or
`simulations/pam.html?initial=hat-low`. Visitors load saved data; GitHub Pages
does not run simulations. All three use the same Brownian increments.

## Edit descriptions without rerunning

1. Edit `_pam/copy.json` for delta, `_pam/copy-hat.json` for the strong-noise hat,
   or `_pam/copy-hat-low.json` for the mild-noise hat.
2. From the repository root, run `python3 _pam/update_captions.py`.
3. Commit the changed copy files and generated `simulations/pam-*.html`, then push.

Titles, captions, descriptions, and equations are editable.
This standard-library-only script updates all three pages, verifying that each embedded
simulation payload is byte-for-byte unchanged. It does not run Julia, read NPZ
files, or recompress arrays. To update just one page, supply both
`--page simulations/pam-hat.html --copy _pam/copy-hat.json` (or either other pair).

The initial profile, coefficients, and trajectory are fixed numerical data.
Changing descriptive wording does not change the simulation. Retain the distinction
between numerical positivity at graph vertices and a theorem for the continuum
SPDE. Detailed numerical checks remain in the local simulation project and are not displayed on the public pages.
A single path illustrates spatial concentration, not moment intermittency.

## Presentation sources

`_pam/viewer.template.html` is the common plotting source before saved payloads
are inserted. `_pam/selector.template.html` is the complete entry-page source;
after editing it, copy it to `simulations/pam.html`. The `_pam` editing directory
is excluded from the generated Jekyll website. Numerical datasets and full rebuild
tooling remain in the local simulation project; routine caption changes need only
the updater above.
