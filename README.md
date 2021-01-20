# Morgan Freeman Deepfake Project

This is a school group project done in my final semester of undergraduate study. The project's intention is to create a deepfake video of Morgan Freeman by training our own text-to-voice synthesis (forking the *DCTTS* repository and modifying it) and having a pre-made template video of Morgan Freeman (using DeepFaceLab). To combine the video and audio product, *wav2lip* library was used.

## Demo

[Morgan Freeman with face swap](https://drive.google.com/file/d/1hStrbOGUt8-i3jseU9zvVlzT5aWgVmt3/view?usp=sharing)


[Morgan Freeman from Shawshank Redemption](https://drive.google.com/file/d/1EQkHy6vBa3qunDiyFdUlhkRowHedpJCI/view?usp=sharing)


[Morgan Freeman with Jackie Chan's voice](https://drive.google.com/file/d/1IM5HApHL9nsXV72gUsyN4SWGEp6LyMYa/view?usp=sharing)

## Steps to run

**This README contains deployment information for this project.**

1. Clone this repo

2. Dependencies *(links for setting up these **packages** and the **virtual environments** they need to run in)*

    - [dctts](libraries/dctts/dctts.md)
    - [wav2lip](libraries/wav2lip/wav2lip.md)

3. Ensure the paths in **dfmotiv/paths.yml** point the relevant dirs.

4. find a Morgan Freeman clip as template and store it into dfmotiv/**src**/**template.mp4**.


```


python3 dfmotiv.py -t "Hello World, this is Morgan Freeman"


```

voila, you've created a deepfake video. see dfmotiv/out/**output.mp4**


## Making DeepFake templates
- [DeepFaceLab](libraries/dfl/dfl.md)

## Other flags
```
// Specify output path
python3 dfmotiv.py -t "This is Morgan Freeman" -o /home/asim/Videos/myDeepfake.mp4

// Export audio only
python3 dfmotiv.py -t "This is Morgan Freeman" -a
// or
python3 dfmotiv.py -t "This is Morgan Freeman" -o /home/asim/Videos/mrFreeman.wav

// Specify a template video (no flag defaults to looking for dfmotiv/src/template.mp4)
python3 dfmotiv.py -t "This is Morgan Freeman" -v template_ssr.mp4
python3 dfmotiv.py -t "This is Morgan Freeman" -v /home/asim/Videos/template_ssr.mp4 -o /home/asim/Videos/myDeepfake.mp4

```

## Repo sanity!

- ensure no data, model, video, image, audio files are uselessly commited to this repo (use .gitignore)
- don't commit files that can/will be auto generated
- if you need to include the whole library/package, fine, but please use gitignore diligently


## Git Helpers

Use dev branches the do a pull request

If you're worried about conflicts
```
git stash              # store away your uncommited changes
git pull               # pull remote changes
git stash apply        # apply changes ontop
git commit -m 'blah'
git push
```

shorthand for git branch myBranch && git checkout myBranch
```
git checkout -b mybranch
```

set your local recent commits on top of latest remote commits (which you dont have)
```
git pull --rebase
```

Don't want to spam the commit history in remote ?...

create a branch, do all your commits, switch to master and do a squash merge (squashes them to a single commit).

```
git checkout -b myBranch

# edit and git commit as normal as many times as you like
# When you finally want to push changes then switch to master branch..

git checkout master
git merge --squash myBranch
git commit
```

Omitting the **-m** from **commit** lets you modify a draft message containing every message from your squashed commits before finalizing your commit.
