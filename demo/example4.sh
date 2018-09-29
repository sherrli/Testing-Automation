#!/usr/bin/env bash
# chmod 755 filename.sh
# If you code in Windows, then lines end in LF and not CRLF. Must convert windows line endings to unix endings.

# Example of some file checking commands in Shell, with a call to LastPass CLI.

USER="user"
echo $USER


if [ -e data_file.json ]; then
  echo "file exists"
fi

if [ -r data_file.json ]; then
  echo "file readable"
fi

# cat login.sh
echo "enter lpass username"
read user
lpass login $user

