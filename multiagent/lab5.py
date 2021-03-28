if __name__ == "__main__":

    S = []
    for i in range (0, 9):
        S.append(i * i)
    
    T = [i for i in (1, 13, 16)]
    M = [i for i in S if i in T and i % 2 == 0]

    print(S)
    print(T)
    print(M)
    