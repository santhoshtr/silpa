rsync --verbose  --progress --stats --compress --rsh=/usr/bin/ssh \
      --recursive --times --perms --links --delete --update  \
      --exclude "*bak" --exclude "*~" \
      /sda5/smc/smc/silpadev/* smcweb@smc.org.in:/home/smcweb/smc.org.in/silpadev/
