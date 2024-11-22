# gitsync

gitsync is designed to bridge the gap in academic projects where contributors have different roles: some focus on coding and producing tables and figures, while others focus solely on writing. In these cases, integrated solutions like Python notebooks are often unsuitable because (1) writers may not use statistical software, and (2) writing often requires precise formatting that advanced tools like LaTeX can provide, which simple Markdown-to-LaTeX conversions cannot match. Consequently, such projects often resort to cloud storage solutions without version control, missing the advantages of tracking changes in both code and LaTeX.

gitsync addresses this need by enabling the synchronization of LaTeX projects managed in a Git repository with directories outside the repository (e.g., a Dropbox folder). The package is built with the assumption that the Git repository maintains a central library of shared tables and figures (by default, `./assets`), with each LaTeX project stored in its own folder within the repository (e.g., `./tex/article` for the paper, and `./tex/presentation` for the slides). gitlatex provides R functions to streamline syncing the local copy of each project with their remote counterpart.

## Installation
