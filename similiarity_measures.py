p_list, u_list, e_list, m_list, s_list, j_list = [], [], [], [], [], []


def dist(ul):
    for val in ul:
        for p1, p2 in val:
            e_list.append(sum([(i - j) ** 2
                               for i, j in zip(p1, p2)]) ** (1 / 2))
            m_list.append(sum([abs(i - j) for i, j in zip(p1, p2)]))


def co(ul):
    f00, f01, f10, f11 = 0, 0, 0, 0
    for v1, v2 in zip(ul[0], ul[1]):
        if v1 == 0 and v2 == 0:
            f00 += 1
        elif v1 == 0 and v2 == 1:
            f01 += 1
        elif v1 == 1 and v2 == 0:
            f10 += 1
        else:
            f11 += 1
    print(f"\nF00 = {f00}\nF01 = {f01}\nF10 = {f10}\nF11 = {f11}\n")
    print(f"Simple Matching coefficient: "
          f"{round((f00 + f11) / (f00 + f01 + f10 + f11), 3)}")
    print(f"Jaccard's coefficient: {round(f11 / (f01 + f10 + f11), 3)}")


def table(gl, pc):
    counter = 1
    th = ["P" + str(num) for num in range(1, pc + 1)]
    print("\n", *th, sep="\t\t")
    print("\t" + "_" * pc * 8)
    for x in range(pc):
        print(f"P{x + 1}\t", end="|")
        for y in range(pc):
            if counter % pc == 0:
                print(round(gl[x * pc + y]*1.0, 3), end="\t|\n")
            else:
                print(round(gl[x * pc + y]*1.0, 3), end="\t|")
            counter += 1
    print("\t" + "‾" * pc * 8)
    p_val = sorted(set(gl))[1]
    idx = gl.index(p_val)
    p_idx = sorted([idx % pc, int(idx / pc)])
    print(f"The points P{p_idx[0] + 1} and P{p_idx[1] + 1} are "
          f"similar with value of {round(p_val, 3)}")


try:
    print("Measures of similarity and dissimilarity")
    ch = int(input("1: Euclidean distance and Manhattan distance\n"
                   "2: Simple Matching Coefficient "
                   "and Jaccard's Coefficient:\n"))
    if ch == 1:
        np = int(input("\nEnter the number of points: "))
        nd = int(input("Enter the dimensionality: "))
        print("\nEnter the points")
        for pt in range(np):
            pl = list(map(int, input(f"Enter the point P{pt + 1}: ").split()))
            if len(pl) != nd:
                raise Exception("Incorrect dimensions")
            p_list.append(pl)
        u_list.append([[x, y] for x in p_list for y in p_list])
        dist(u_list)
        print("\n" + "-" * 50 + "\nEuclidean distance\n" + "-" * 50)
        table(e_list, np)
        print("\n" + "-" * 50 + "\nManhattan distance\n" + "-" * 50)
        table(m_list, np), print("-" * 50)
    elif ch == 2:
        ndp = int(input("\nEnter the dimensionality of points: "))
        for pt in range(2):
            pl = list(map(int, input(f"Enter the coordinates "
                                     f"of point {pt + 1}: ").split()))
            if len(pl) != ndp:
                raise Exception("Incorrect dimensions")
            elif any(x not in (0, 1) for x in pl):
                raise Exception("Incorrect values")
            else:
                u_list.append(pl)
        co(u_list)
    else:
        raise Exception("Incorrect choice")
except Exception as e:
    print(e)
