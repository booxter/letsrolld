#!/usr/bin/env bash

set -xe

tdir=$(mktemp -d)
echo "$tdir"
for country in $(fetch-countries); do
  echo "Applying country: $country"
  fetch-country-list -N -c "$country" -o "$tdir/list.csv"
  fetch-directors -i "$tdir/list.csv" -o "$tdir/directors.csv"
  populate-directors -d "$tdir/directors.csv"
  make run-update-directors # fetch all films after each list so that "film already known" heuristic considers just added directors/movies
  rm "$tdir/*.csv"
done
echo "Done applying countries; results are in $tdir"
# rm -rf $tdir
