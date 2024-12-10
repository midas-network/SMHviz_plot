# Release Process

Parts of this document is adapted for the U.S. Scenario Modeling Hub (SMH) from 
[The Hubverse](https://hubverse-org.github.io/hubDevs/articles/release-process.html) 
and from 
[The Carpentries Developer's Handbook](https://carpentries.github.io/workbench-dev/releases.html) ©
The Carpentries under the 
[CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). 

## Workflow

The release process follow a general workflow:

1. Iterate on small bug fixes and PRs on branches:
   - merging into `main` once ready to publish/deploy
   - merging into a development branch (here called `dev`) for ongoing test/process
2. When ready to release on `main`: bump the version, add an annotated git tag, and release
3. Bump the version in main back to a development version
 
Some of the steps in these instructions are specific for R packages, but they are largely process-based 
and can apply to Python packages as well.

### Versioning 

The SMH is built using very basic semantic versioning using the X.Y.Z[.9000] pattern. Everything that 
has a .9000 attached is considered in-development.

`X`: **Major version number**:  this version number will change if there are significant breaking 
changes to any of the user-facing workflows. That is, if a change requires users to modify their 
scripts, then it is a breaking change.

`Y`: **Minor version number**: this version number will change if there are new features or
 enhanced behaviors available to the users in a way that *does not affect how users who do not 
need the new features use the package*. This number grows the fastest in early stages of development.

`Z`: **Patch version number**: this version number will change if something that was previously 
broken was fixed, but no new features have been added.

`9000`: **Development version indicator**: this version number indicates that the package is in a 
development state and has the potential to change. When its on the main branch, it indicates 
that the features or patches introduced have been reviewed and tested. This version is appended 
after every successful release. 

###  Hotfixes

A hotfix is a bug fix for a situation where a bug has been found, but the main branch has new features 
that are not yet ready to be released.

## Checklist

### Updates

[] Create new branch from `main` (or `master`, or branch of interest) called `"<author initial>/<feature>/<issue>"`

[] Update `Changelog.md` accordingly

[] Commit, push

[] Open Pull-Request (PR) on branch of interest (`main` for release we want to implement quickly or ready to deploy, other 
 branch of interest for ongoing updates)

[] Merge after review, once all accepted 

**Create new release version only if important change, see version**

### Release

[] Create new branch from `main` (or `master`) called `"<author>/release/X.Y.Z"`

[] Update `pyproject.toml` and `Changelog.md` accordingly

[] Commit, push

[] Open Pull-Request (PR)

[] Merge after review, once all accepted 

[] Checkout `main` branch (or `master`) & make sure it's up to date

[] Add new tag

```
git tag -a v.X.Y.Z -m '<short message>'
git push --tags
```
    
[] Create a new release on GitHub (can be done using R, for example)

```r
usethis::use_github_release()
```

### Post-Release

[] Create new branch from `main` (or `master`) called `"post-release-X.Y.Z"`

[] Set project to dev version (can be done using R, for example): 
	- adding `.9000` to the version number
	-  adding new heading to `Changelog.md` (`## <package name> (development)`)
 
```r
usethis::use_dev_version()
```
    
[] Commit, push, open Pull-Request (PR) 

[] Merge after review, once all accepted 


### Subsequent updates

[] Create new branch from `main` (or `master`, or branch of interest) called `"<author initial>/<feature>/<issue>"`

[] Update `Changelog.md` accordingly

[] Commit, push

[] Open Pull-Request (PR)

[] Merge after review, once all accepted 

**Create new release version only if important change, see version**

### Hotfixes

[] Create new branch from `main` (or `master`) called `"<author>/hotfix/<issue>"`

```	
git switch --detach v.X.Y.Z'
git switch -c <author>/hotfix/<issue>
```
    
[] Write a test, fix the bug, commit, push
** Don't change the version **

[] Open Pull-Request (PR) 

[] Update `Changelog.md` accordingly and bump the patch version in `pyproject.toml`

```
git commit -m 'bump version to X.Y.Z+1'
git tag -a v.X.Y.Z+1 -m '<short message>'
git push
git push --tags
```
    
[] Create a new release on GitHub (can be done using R, for example)

```r
usethis::use_github_release()
```
    
[] Resolve conflicts in PR & merge into `main` (or `master`)
