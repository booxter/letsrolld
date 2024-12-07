#!/usr/bin/env bash

tdir=$(mktemp -d)
echo $tdir
for country in $(fetch-countries); do
  echo "Applying country: $country"
  fetch-country-list -N -c $country -o $tdir/list.csv
  fetch-directors -N -i $tdir/list.csv -o $tdir/directors.csv
  populate-directors -d $tdir/directors.csv
  make run-all  # fetch all films after each list so that "film already known" heuristic considers just added directors/movies
done
echo "Done applying countries; results are in $tdir"
# rm -rf $tdir
