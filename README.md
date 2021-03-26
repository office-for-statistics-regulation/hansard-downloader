## A Project Template for OSR Projects

### 1. Guides for Private AND Public Repositories

#### 1.1 Introduction

This repository is intended to provide you with the documents you need to
include to get a repository started and give guidance as to what the contents
should be. The minimum content contained in the README.md for your project
should be (in the most suitable order for the content):

- description of what the project is
- instruction on how to install the tool (if applicable)
- detailed instructions on basic use
- a demo of the code

With the inclusion of all documents included here, your repository should meet
all of the recommended [community standards on github.com](https://help.github.com/en/categories/building-a-strong-community).

Once you have copied this directory you should replace the content of this file
with the description of your work.

Whilst no mandatory recommendation is made as to how to
structure the directories or manage the project itself - as this will vary based
on the needs and the abilities of those doing the development work - guidelines
are provided below on how to conduct your project in an Agile manner.

If your project is complex enough to warrant a documentation website please add
a branch called `gh_pages` and place your documentation (in html format) there.
Once you do this your html files will be rendered at
https://office-for-statistics-regulation.github.io/projectName

#### 1.2. Cloning this Repo

There are two ways to use this template:

##### 1.2.1. Using GitHub (simple method)

At the top of the main page of this repo is a green [Use this template](https://github.com/office-for-statistics-regulation/osr-private-template/generate) button, which
will clone this repository into a new repository of your choice. The Issue Templates are 
also cloned. Unfortunately, Issue Labels, and Project Boards are not cloned automatically,
and you will have to manually add these (guidelines below).

##### 1.2.2. Using Git

Create your new repository with a suitable projectName.

Clone this template to the new repository using

``` sh
git clone git@github.com:office-for-statistics-regulation/osr-private-template projectName
```

which will then create a new directory with your project's name and place all of
the files into it. However, the remote address will remain as the skeletor repo
until you do

``` sh
git remote set-url origin git@github.com:office-for-statistics-regulation/projectName
```

### 2. Guides for Private Repositories ONLY

#### 2.1. Using GitHub for Project Management (Agile)

Note: All updates for a project must be included on the relevant
[project on the portfolio board](https://github.com/orgs/office-for-statistics-regulation/projects/1).
These guidelines relate to the `project repository` that you created using the above guidelines.

### 3. Guides for Public Repositories ONLY

Make a clean, fresh repository! This will make sure no git history is opened to the public. Copy your code into this repository and update the **CONTRIBUTING.md** file. Your **README.md** might also need more information too. And check you are using the relevant **LICENSE.md** file too.

### 4. Contents

* **CODE_OF_CONDUCT.md**: a statement from the [Contributor
  Covenant](https://contributor-covenant.org) regarding what is and isn't
  acceptable behaviour for contributors
* **CONTRIBUTING.md**: guidelines for how contributions should be made to the work,
  this should be updated when the work is made public
* **README.md**: this document, every repository should have one and it acts as
  the main landing page for your repository
* **LICENSE**: the UK public sector usually operate under two different
  licensing schemes. The most common for code is the MIT license which is
  included in this repo. Alternatively there is an Open Government license and
  a description of what OpenGov enforces can be found
  [here](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
* **.github**: this directory allows the user to specify templates for
  contribution types, included in this repository are a bug fix submission
  template, a feature request template and a pull request template. Each of them
  includes a series of tickboxes which you can use to help you decide whether or
  not the submission is suitable.
* **.gitignore**: this file allows you to specify which directories, files and
  globbed file types are to be ignored as part of the diffs being managed by
  git. This allows you to have your data in the same directory structure as your
  code without it needing to be pushed and pulled along with it. If you have
  data which you do need to manage I would highly advise the use of `git-annex`
  ahead of including data files in your repository (unless they are small).

Taken from Michael Hodge's work on Data Science Campus GitHub.