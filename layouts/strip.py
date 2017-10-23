#!/usr/bin/env python

spacing = 0.11  # m
lines = []
for c in range(-1, 2):
    rs = [range(1), reversed(range(90))][c % 2]
    for r in rs:
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                     (c*spacing, 0, (r - 25)*spacing))
print '[\n' + ',\n'.join(lines) + '\n]'
