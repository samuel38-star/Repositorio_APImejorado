from collections import defaultdict
import sys

lines = sys.stdin.read().strip().split()
i = 0
case = 1

while True:
    if i >= len(lines):
        break

    if lines[i] == '-1':
        break

    data = []
    count = 0

    # leer árbol completo
    while True:
        val = int(lines[i])
        i += 1

        data.append(val)

        if val == -1:
            count -= 1
        else:
            count += 1

        if count == 0:
            break

    # procesar
    piles = defaultdict(int)
    it = iter(data)

    def dfs(pos):
        val = next(it)

        if val == -1:
            return

        piles[pos] += val

        dfs(pos - 1)
        dfs(pos + 1)

    dfs(0)

    print(f"Case {case}:")
    case += 1

    for k in sorted(piles):
        print(piles[k], end=" ")
    print()
    print()