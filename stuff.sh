stuff

dig example.com +stats | awk '/^;; QUERY:/ {query=$4} /Query time:/ {print query, $4 " ms"}'
