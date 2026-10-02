# Data dictionary

TXT header: instance title, VEHICLE, NUMBER/CAPACITY, then CUSTOMER fields.

| Position | Field | Meaning / unit |
|---|---|---|
| 0 | CUST NO. | Integer node ID, 0 depot, 1–1000 customers |
| 1 | X_UTM | Easting, metres, EPSG:32648 |
| 2 | Y_UTM | Northing, metres, EPSG:32648 |
| 3 | LAT | Latitude, degrees, EPSG:4326 |
| 4 | LON | Longitude, degrees, EPSG:4326 |
| 5 | DEMAND | Grams |
| 6 | READY TIME | Earliest service start, minutes |
| 7 | DUE DATE | Latest service start, minutes |
| 8 | SERVICE TIME | Service duration, minutes |

`NUMBER` is the available vehicle limit; `CAPACITY` is per-vehicle capacity in grams. Every customer must occur exactly once on a route beginning and ending at 0. Waiting is allowed. Due time constrains service start. Return to depot must occur by its due time. Route demand must not exceed capacity.

Distance matrices: `Distance_Matrix_{C1,C2,R,RC}.csv`, metres. Time matrices: `Time_Matrix_{C1,C2,R,RC}.csv`, seconds. Both use a header row and label column, in identical order. `node_order_{C1,C2,R,RC}.csv` maps TXT node IDs to matrix labels. RC retains mixed C1/R source labels; preserve their released positional order. Blank top-left cell is intentional. The diagonal is zero; off-diagonal entries are positive. Each matrix is directed.

The lexicographic experiment objective is minimum nonempty routes, then minimum total directed distance. Archived witnesses demonstrate feasibility only; use a separate solver release for algorithm comparison.

Family counts: C1 9, C2 8, R1 12, R2 11, RC1 8, RC2 8. Capacities: type 1 = 30,000 g; type 2 = 50,000 g. Service durations: C families 5 min; R/RC families 2 min.
