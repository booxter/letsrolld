#!/usr/bin/env bash

# https://letterboxd.com/eternalalien/list/all-narrative-feature-films-on-letterboxd/
# https://letterboxd.com/narpjay/list/exploitation-films-b-movie-cheese-grindhouse/
# https://letterboxd.com/seanmcgann98/list/sleazemovies-erotiga/
# https://letterboxd.com/mishima24/list/the-most-comprehensive-list-of-japanese-movies/
# https://letterboxd.com/ashleylynch/list/rarelust-complete-list/
# https://letterboxd.com/giniyapp/list/the-celluloid-void-rare-films-written-and/
# https://letterboxd.com/aopisaac/list/video-galactica-a-virtual-video-store-11293/
# https://letterboxd.com/sadhomersimpson/list/criterion/
# https://letterboxd.com/natethecyborg/list/every-film-available-on-the-criterion-channel/
# https://letterboxd.com/smiskfisk/list/almost-every-title-from-worldscinemaorg/
# https://letterboxd.com/robbob01/list/public-domain/
# https://letterboxd.com/ru6yy/list/every-movie-of-every-actor-actress-ive-seen/
# https://letterboxd.com/xob/list/films-of-interest-that-are-available-in-full/
# https://letterboxd.com/000_leo/list/every-film-ever-eligible-for-the-oscars/
# https://letterboxd.com/kordian86/list/list-of-polish-movies-1902-2023/
# https://letterboxd.com/ryokohakubi/list/a-comprehensive-animation-list/
# https://letterboxd.com/astroturd/list/no-average-rating/
# https://letterboxd.com/adamrant/list/the-definitive-films-about-film-list/
# https://letterboxd.com/terje_jr/list/struggles-of-the-global-south-in-progress/
# https://letterboxd.com/nodadyoushutup/list/nodadyoushutup-plex/
# https://letterboxd.com/marconerix/list/balkan-movies/
# https://letterboxd.com/solidaritycine/list/solidarity-cinema-archive/
# https://letterboxd.com/dessaint/list/best-korean/
# https://letterboxd.com/dmytro_malyar/list/ukrainian-films/
# https://letterboxd.com/bratofthe1980s/list/the-european-boys-adventure-tale/
# https://letterboxd.com/butterbud/list/the-working-class/
# https://letterboxd.com/jim13/list/cold-war-films/
# https://letterboxd.com/adarksong/list/films-from-classic-films-channel-to-watch/
# https://letterboxd.com/magrosleau/list/psychosexual-dramas-nihilistic-fever-dreams/
# https://letterboxd.com/evilbjork/list/avant-garde-underground/
# https://letterboxd.com/knuffeltje/list/zero-watches/
# https://letterboxd.com/artyficial/list/the-oxford-history-of-world-cinema/
# https://letterboxd.com/loureviews/list/i-l3ve-musicals/
# https://letterboxd.com/mitramitra/list/the-iran-archive-everything-wip/
# https://letterboxd.com/juliec/list/neverending-christmas-movie-list/
# https://letterboxd.com/stottiain/list/great-big-list-of-classic-cartoons/
# https://letterboxd.com/kodifranzese/list/kodi-franzeses-non-usa-foreign-filmography/
# https://letterboxd.com/timonist/list/east-germany/
# https://letterboxd.com/rhettman417/list/movies-on-rarefilmmcom/
# https://letterboxd.com/pakejanek/list/okru/
# https://letterboxd.com/liveandrew/list/genre-exploitation-100-years-1896-1995/
# https://letterboxd.com/gabrmachado/list/brazilian-cinema/
urls=(
  "https://letterboxd.com/sr0man/list/erotic/"
  "https://letterboxd.com/dustin_b/list/films-i-own-the-complete-mega-load/"
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
)

tdir=$(mktemp -d)
echo "$tdir"
for url in "${urls[@]}"; do
  echo "Applying list from url: $url"
  fetch-lb-list -N -u "$url" -o "$tdir/list.csv"
  fetch-directors -N -i "$tdir/list.csv" -o "$tdir/directors.csv"
  populate-directors -d "$tdir/directors.csv"
  make run-all  # fetch all films after each list so that "film already known" heuristic considers just added directors/movies
done
echo "Done applying lists; results are in $tdir"
# rm -rf $tdir
