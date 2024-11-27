def LCS(X, Y): # Функция для нахождения максимальной подстроки
    m = len(X)
    n = len(Y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    max_length = 0
    end_pos_x = 0
    end_pos_y = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_pos_x = i
                    end_pos_y = j
            else:
                dp[i][j] = 0

    start_pos_x = end_pos_x - max_length
    start_pos_y = end_pos_y - max_length
    return (start_pos_x, end_pos_x), (start_pos_y, end_pos_y), max_length
