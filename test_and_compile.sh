#!/bin/bash

exercise_number=$1
read exercise_number

directory="EX$exercise_number"
test_file="tests.py"

cd "$directory" || exit

if test -f "$test_file"; then
  echo "$test_file exists"
  python $test_file
fi

zip "ex$exercise_number.zip" * -i \*.py --exclude $test_file \*.zip
