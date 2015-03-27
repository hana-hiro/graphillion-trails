#!/bin/sh

find -name '*~' -print -delete
find -name '*.sgraph' -print -delete
find -name '*.lsgraph' -print -delete
find -name '*.lsgraph.json' -print -delete
find -name '*.pyc' -print -delete

