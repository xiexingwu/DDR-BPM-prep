#!/bin/bash
gh auth status | grep -B 1 "Active.*true" -
printf 'Confirm release(y/n)? '
read answer

if [ "$answer" != "${answer#[Yy]}" ] ;then 
  echo Release confirmed...
  gh release delete Latest -y --cleanup-tag
  echo Creating new release...
  gh release create Latest -n "$(date)" build/*.{txt,zip}
else
  echo Release stopped.
fi
