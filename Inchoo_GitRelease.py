#!/usr/bin/python
# Name: Inchoo_GitRelease
# Author: Marko Martinović (marko.martinovic@inchoo.net)
# License: GPLv2

# Git directory path
git_path = '.'

# Git tag format
git_tag_format = "%Y/%m/%d"

#### config ends here ####

from git import *
import os, sys, time

# Initiate repo object
repo = Repo(git_path)

# Check for master branch
if not hasattr(repo.heads, 'master'):
    print "No master branch found. Create a master branch first"
    sys.exit(1)

# Check for develop branch
if not hasattr(repo.heads, 'develop'):
    print "No develop branch found. Create a develop branch first"
    sys.exit(1)

# Check is origin set
if not hasattr(repo.remotes, 'origin'):
    print "No origin set. Please set origin first."
    sys.exit(1)

# Are there any uncommitted changes
if repo.is_dirty():
    print "Git repo is dirty. Please use commit or stash first."
    sys.exit(1)

# Checkout develop branch
repo.heads.develop.checkout() 

# Origin object
origin = repo.remotes.origin

# Pull from develop branch
origin.pull('develop')

# If tag already exists, calculate suffix, for eg.
# 2014/02/02_0, 2014/02/02_1, 2014/02/02_2 etc.
release_tag = time.strftime(git_tag_format)
release_tag_suffx = 0
while release_tag + "_" + str(release_tag_suffx) in repo.tags:
   release_tag_suffx = release_tag_suffx + 1
release_tag = release_tag + "_" + str(release_tag_suffx)

# Create the release branch
release_branch = "release/"+ release_tag
repo.create_head(release_branch)

# Checkout master branch
repo.heads.master.checkout() 

# Merge the release branch into master (low level due to --no-ff)
repo.git.merge(release_branch, no_ff=True)

# Create the tag
release_message = "Release " + release_tag
repo.create_tag(release_tag, 'HEAD', release_message)

# Push master branch to origin
origin.push('master')

# Push tags to origin (low level due to --tags)
repo.git.push(tags=True)
