stuff

dig example.com +stats | awk '/^;; QUERY:/ {query=$4} /Query time:/ {print query, $4 " ms"}'


domain=example.com; dig $domain +stats | awk -v d="$domain" '/Query time:/ {print d, $4 " ms"}'

