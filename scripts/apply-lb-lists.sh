#!/usr/bin/env bash

urls=(
  "https://letterboxd.com/smlibrary/list/okay/"
  "https://letterboxd.com/retinaburn/list/the-most-comprehensive-list-of-hong-kong/"
  "https://letterboxd.com/wolfman07/list/every-horror-film-ever-made-1/"
  "https://letterboxd.com/infinityinc/list/every-tv-movie-aired-on-american-television/"
  "https://letterboxd.com/kaijufan67/list/the-bad-taste-list-weird-wild-psychotronic/"
  "https://letterboxd.com/buttersgreer/list/ultimate-list-of-every-movie-musical/"
  "https://letterboxd.com/natethecyborg/list/every-film-available-on-the-criterion-channel/"
  "https://letterboxd.com/mishima24/list/the-most-comprehensive-list-of-japanese-movies/"
  "https://letterboxd.com/elmiko_/list/every-animated-film-made-from-1878-present/"
  "https://letterboxd.com/clowchan/list/every-horror-film-made-from-1895-present/"
  "https://letterboxd.com/sr0man/list/erotic/"
  "https://letterboxd.com/dustin_b/list/films-i-own-the-complete-mega-load/"
)

tdir=$(mktemp -d)
for url in "${urls[@]}"; do
  echo "Applying list from url: $url"
  fetch-lb-list -N -u $url -o $tdir/list.csv
  fetch-directors -N -i $tdir/list.csv -o $tdir/directors.csv
  populate-directors -d $tdir/directors.csv
  make run-all  # fetch all films after each list so that "film already known" heuristic considers just added directors/movies
done
echo "Done applying lists; results are in $tdir"
# rm -rf $tdir
