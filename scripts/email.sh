#!/usr/bin/env bash

set -e

FROMADDR=ihar.hrachyshka@gmail.com

# Format: e@mail1[,e@mail2,...]
TOADDRS=${TOADDRS:-$FROMADDR}

tmpdir=$(mktemp -d)
trap 'rm -r $tmpdir' EXIT

reportfile=$tmpdir/movies.report
./scripts/gen_report.sh -s "$reportfile"

subject="Movies for $(date '+%Y-%m-%d')"

if command -v mailsend-go > /dev/null; then
  mailsend-go -from $FROMADDR -t "$TOADDRS" -sub "$subject" \
    -use gmail auth -user $FROMADDR -pass "$(pass priv/google.com-mutt)" \
    body -file "$reportfile"
else
  if command -v ssmtp > /dev/null; then
    echo "Subject: $subject" > "$tmpdir/email.txt"
    cat "$reportfile" >> "$tmpdir/email.txt"

    # Convert TOADDRS into array.
    IFS=',' read -r -a TOADDRS <<< "$TOADDRS"

    ssmtp -d99 "${TOADDRS[@]}" < "$tmpdir/email.txt"
  else
    echo "No email client found. Please install mailsend-go or ssmtp."
    exit 1
  fi
fi
