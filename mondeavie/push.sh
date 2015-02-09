#!/bin/bash
update_str="update"
if [ -z "$1" ]; then
   echo "update";    
else 
   update_str=$1;
fi
git add -A . && git commit -m "$update_str" && git push
