# Saverio Spinella — personal website

Static HTML/CSS, compatible with GitHub Pages. No dependencies or build step required.

- `index.html`: home page and introduction.
- `research.html`: research sections and native HTML abstract expanders.
- `styles/styles.css`: colors, typography, desktop width, and mobile layout.
- `resources/`: original CV, papers, and photographs supplied with the website.

The CV and Google Scholar buttons appear on both pages. The Inequality Multiplier
has no coauthor line because it is a solo-authored project.

The small sun/moon button beside the navigation switches light and dark mode.
It follows the device preference initially and remembers an explicit choice on that device.

## Portraits for light and dark mode

Both pages show `resources/propic.jpeg` in light mode and
`resources/propic-dark.jpeg` in dark mode. The two files currently contain the same
photo. To use a different dark-mode portrait, replace `resources/propic-dark.jpeg`
in GitHub with your new JPEG, keeping the exact filename and folder. No code
changes are needed. Replace `resources/propic.jpeg` to change the light-mode photo.

Both portraits use the same size, square crop, and rounded corners. The visible
portrait follows the active theme, including saved and device preferences.

## Update GitHub Pages

Copy this folder's contents into the root of your existing website repository,
then commit and push using your usual workflow.

The supplied PDFs have been preserved. To update the CV, replace `resources/CV.pdf`.

## Local preview and validation

Run `python3 -m http.server 8765`, then visit `http://localhost:8765/research.html`.
Run `python3 build.py` to validate HTML and local links and stage the private preview.
