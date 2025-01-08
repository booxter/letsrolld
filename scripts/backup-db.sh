#!/usr/bin/env bash

DIR=backup

mkdir -p $DIR

function cleanup {
    # Delete oldest backup
    candidate="$(find $DIR -type f | sort | head -n 1)"
    echo "Deleting $candidate"
    rm "$candidate"
}

# Make sure backup directory doesn't take more than 30gb (+the new backup)
while [ "$(du -s $DIR | cut -f1)" -gt 3000000 ]; do
    cleanup
done

cp movie.db "$DIR/$(date +%Y-%m-%d-%H-%M-%S)-movie.db"
