# gitsync

gitsync is designed to bridge the gap in academic projects where contributors have different roles: some focus on coding and producing tables and figures, while others focus solely on writing. In these cases, integrated solutions like Python notebooks are often unsuitable because (1) writers may not use statistical software, and (2) writing often requires precise formatting that advanced tools like LaTeX can provide, which simple Markdown-to-LaTeX conversions cannot match. Consequently, such projects often resort to cloud storage solutions without version control, missing the advantages of tracking changes in both code and LaTeX.

gitsync addresses this need by enabling the synchronization of LaTeX projects managed in a Git repository with directories outside the repository (e.g., a Dropbox folder). The program ackage is built with the assumption that the Git repository maintains a central library of shared tables and figures (by default, `./assets`), with each LaTeX project stored in its own folder within the repository (e.g., `./tex/article` for the paper, and `./tex/presentation` for the slides). gitsync provides two commands,`push` and `pull`, to streamline syncing the local copy of each project with their remote counterpart.

gitsync simplifies collaboration by allowing coders and writers to work seamlessly within their preferred tools while benefiting from the version control and change-tracking capabilities of Git. As a CLI program, it can be easily integrated with Makefiles or other automation scripts.

## Installation

Install through PyPi

## Usage: a minimal example

Say that Alice, Bob, and Charles are all working on a project. Alice and Bob are the writers/coders, and Charles is only a writer. The Git repo is structured as follows: 

```bash
├-- main.R # the statistical code
├-- assets # the folder that contains the tables and figures created by main.R
|   ├-- tables
|   |   └-- my-table.tex
|   └-- figures
|       └-- my-figure.pdf
└-- tex # the folder that contains all the writing
    ├-- presentation
    |   └-- main.tex
    └-- paper
        └-- main.tex
```

The team is working on a paper and a presentation. The paper is hosted on Overleaf, while the presentation is on Dropbox. 

To get started, open a terminal, navigate to the repo, and type `gitsync create` to set up gitsync in a new or existing project. This will create/update two configuration files, and encourage you to modify them according to your needs:

- **Public configuration file**, `./gitsync.yaml`: Specifies the path to the assets directory and the local paths of each LaTeX project within the repository.
- **Private configuration file**, `.env`: Indicates the remote paths for each project. As usual with .env files, this file is unique to each contributor’s environment and should not be committed to the repository.

```bash
cd my-project
gitsync create
```

The Git repo now looks like this: 
```bash
├-- main.R # the statistical code
├-- assets # the folder that contains the tables and figures created by main.R
|   ├-- tables
|   |   └-- my-table.tex
|   └-- figures
|       └-- my-figure.pdf
├-- tex # the folder that contains all the writing
|   ├-- presentation
|   |   └-- main.tex
|   └-- paper
|       └-- main.tex
├-- gitsync.yaml # the public configuration file
└-- .env # the private confifguration file
```

The file `gitsync.yaml` should be specified as follows: 

```yaml
assets: "./assets"
projects: 
    article: "./tex/article"
    presentation: "./tex/presentation"
```

The file `.env` indicates where the project folders are stored in each of Alice's and Bob's computer. Indeed, the Dropbox location is different for each coauthor. As such, `.env` should not be committed to Git. You should add it to the `.gitignore`.  Here is how `.env` looks for Alice: 

```bash
# other variables stored in .env
SOME_VARIABLE=SOME_VALUE
# variables required byt gitsync
GITSYNC_ARTICLE="/Users/alice/Library/CloudStorage/Dropbox/Apps/Overleaf/cool-paper"
GITSYNC_PRESENTATION="/Users/alice/Library/CloudStorage/Dropbox/projects/cool-project/presentation"
```

After initialization, both Alice and Bob can use `gitsync push` from the CLI to push the latest version of each project to its corresponding remote directory, along with the assets folder. To synchronize the current state of each remote project directory back into the repository (e.g., after Charles has made some changes), they can use `gitsync pull`.

```bash
cd my-project
gitsync push
gitsync pull
```

