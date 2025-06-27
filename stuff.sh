stuff

dig example.com +stats | awk '/^;; QUERY:/ {query=$4} /Query time:/ {print query, $4 " ms"}'


domain=example.com; dig $domain +stats | awk -v d="$domain" '/Query time:/ {print d, $4 " ms"}'


max_attempts=10
attempt_num=1
while [ -f /var/lib/rpm/.rpm.lock ] && [ "$attempt_num" -le "$max_attempts" ]; do
  echo "Waiting for RPM lock... ($attempt_num)"
  sleep 5
  attempt_num=$((attempt_num + 1))
done

