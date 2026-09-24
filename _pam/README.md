# Editing the PAM visualization

The entry page is `simulations/pam.html`. Its **Initial condition** selector loads
`pam-delta.html` (the preserved point-mass trajectory) or `pam-hat.html` (the
localized continuous harmonic-hat trajectory). Both offer natural-log and linear
views. The Researches page embeds this selector with `_includes/pam-simulation.html`.

Share direct choices using `simulations/pam.html?initial=delta` or
`simulations/pam.html?initial=hat`. Visitors load saved data; GitHub Pages does not
run simulations. Both initial conditions use the same driving noise.

## Edit descriptions without rerunning

1. Edit `_pam/copy.json` for delta or `_pam/copy-hat.json` for the localized profile.
2. From the repository root, run `python3 _pam/update_captions.py`.
3. Commit the changed copy files and generated `simulations/pam-*.html`, then push.

Titles, captions, descriptions, equations, and expandable method notes are editable.
This standard-library-only script updates both pages, verifying that each embedded
simulation payload is byte-for-byte unchanged. It does not run Julia, read NPZ
files, or recompress arrays. To update just one page, supply both
`--page simulations/pam-hat.html --copy _pam/copy-hat.json` (or the delta pair).

The initial profile, coefficients, and trajectory are fixed numerical data.
Changing descriptive wording does not change the simulation. Retain the distinction
between numerical positivity at graph vertices and a theorem for the continuum
SPDE. Each choice has its own time-step sensitivity figures in the method notes.
A single path illustrates spatial concentration, not moment intermittency.

## Presentation sources

`_pam/viewer.template.html` is the common plotting source before saved payloads
are inserted. `_pam/selector.template.html` is the complete entry-page source;
after editing it, copy it to `simulations/pam.html`. The `_pam` editing directory
is excluded from the generated Jekyll website. Numerical datasets and full rebuild
tooling remain in the local simulation project; routine caption changes need only
the updater above.
