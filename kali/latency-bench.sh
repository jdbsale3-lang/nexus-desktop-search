#!/usr/bin/env bash
# latency-bench.sh — measure estate latency before/after the cache fix.
set -u
echo "═══ ZEUS LATENCY BENCH (5 samples/endpoint) ═══"
: > /tmp/lat.csv
for spec in \
  "flagship|https://zeusaiintelligence.com" \
  "reach-health|https://zeusaiintelligence.com/reach/health" \
  "reach-self|https://zeusaiintelligence.com/reach/self" \
  "reach-doctor|https://zeusaiintelligence.com/reach/doctor" \
  "reach-monitor|https://zeusaiintelligence.com/reach/monitor" \
  "reach-search|https://zeusaiintelligence.com/reach/search?q=zeus" ; do
  N="${spec%%|*}"; U="${spec##*|}"
  for i in 1 2 3 4 5; do
    curl -s -o /dev/null --max-time 30 -w "$N,%{time_starttransfer},%{time_total}\n" "$U" >> /tmp/lat.csv
  done
done
python3 - <<'PY'
import csv, collections
d=collections.defaultdict(lambda:([],[]))
for r in csv.reader(open('/tmp/lat.csv')):
    if len(r)<3: continue
    try: d[r[0]][0].append(float(r[1])); d[r[0]][1].append(float(r[2]))
    except ValueError: pass
print(f"  {'endpoint':14s} {'TTFB(ms)':>9s} {'total(ms)':>10s}")
for k,(a,b) in d.items():
    if a: print(f"  {k:14s} {sum(a)/len(a)*1000:9.0f} {sum(b)/len(b)*1000:10.0f}")
PY
