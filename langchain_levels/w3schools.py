first_line = input().split()
n, t = int(first_line[0]), int(first_line[1])
numbers = [int(input()) for _ in range(n)]

print(f"n: {n}, t: {t}, numbers: {numbers}")  # Debugging output

# Find two indices that add up to t
for i in range(n):
    for j in range(i + 1, n):
        if numbers[i] + numbers[j] == t:
            print(i, j)  # Output 1-based indices
            exit()