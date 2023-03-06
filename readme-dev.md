# Setup
Setup python environment via the environment.yml file:
```
    conda env create -f environment-dev.yml
```

Which feature need which package:

1. Base utilities
   - python=3.10
   - pip=21.2.4
   - git=2.34.1
   - pyyaml=6.0
2. Generator
   - pyyaml=6.0
3. Converter
   - pypandoc=1.8.1
4. Tracker
   - pandas=1.5.2
   - plotly=5.9.0
   - tqdm=4.64.1
   - pip: gitpython~=3.1.31

# Git guide

## Adding new feature or bug fixes

Create new branch for the feature. Use standard naming for ```<dev branch>```: ```ftr/<feature name>``` for features or ```fix/<fix name>``` for bug fixes
```
    git checkout main
    git pull
    git checkout -b <dev branch>
    git push --set-upstream origin <dev branch>
```

Commit all your dev work in the feature/fix branch. After finished, merge back into main:
```
    git checkout main
    git pull
    git merge <dev branch>
    git push
```

Then merge the updated main branch into each of your writing branches:
```
    git checkout <writing branch>
    git pull
    git merge main
    git push
```

## Cleaning up feature branches

After merging a feature branch to main, you should also archive and delete the feature branch. Ensure you are not checked out on the branch you are going to delete by doing ```git checkout main``` first.
```
    git tag archive/<dev branch> <dev branch>
    git push origin archive/<dev branch>
    git branch -d <dev branch>
    git push -d origin <dev branch>
```

If you need to restore this feature branch later:
```
    git checkout -b <dev branch> archive/<dev branch>
```

## Renaming branches

Renaming a local branch is pretty simple, but renaming the remote not so simple:
```
    git branch -m <old_name> <new_name>
    git push origin --delete <old_name>
    git branch --unset-upstream <new_name>
    git push origin -u <new_name>
```
And then to update the branch name on your other devices:
```
    git fetch --prune
    git branch -m <old_name> <new_name>
    git branch --unset-upstream <new_name>
    git branch --set-upstream-to origin/<new_name> <new_name>
```


