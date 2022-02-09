from prettytable import PrettyTable

it_list1 = [["bread", "cheese", "eggs", "juice"], ["bread", "cheese", "juice"],
            ["bread", "milk", "yogurt"], ["bread", "juice", "milk"],
            ["cheese", "juice", "milk"]]
it_list2 = [["strawberry", "litchi", "oranges"],
            ["strawberry", "butter_fruit"], ["butter_fruit", "vanilla"],
            ["strawberry", "litchi", "oranges"], ["banana", "oranges"],
            ["banana"], ["banana", "butter_fruit"],
            ["strawberry", "litchi", "apple", "oranges"], ["apple", "vanilla"],
            ["strawberry", "litchi"]]
it_list3 = [["A", "B", "C", "D", "E", "F"], ["G", "H", "C", "D", "E", "F"],
            ["A", "K", "D", "E"], ["A", "J", "M", "D", "F"],
            ["M", "B", "D", "N", "F"], ["A", "N", "J", "E", "F"],
            ["B", "M", "K", "D"], ["C", "D", "H", "M"]]
it_list = []
fi_list = []
c_set = []


def ceil(n):
    res = int(n)
    return res if res == n or n < 0 else res + 1


def p_table(c):
    tbl = PrettyTable(["Item set", "Support count"])
    for val in c:
        if isinstance(val[0], str):
            tbl.add_row([val[0], val[1]])
        else:
            tbl.add_row([', '.join(val[0]), val[1]])
    return tbl


def combinations(lst, it):
    result = []
    for p1 in range(len(lst)):
        for p2 in range(p1 + 1, len(lst)):
            if it == 0:
                result.append([lst[p1], lst[p2]])
            else:
                if list(lst[p1])[0:it] == list(lst[p2])[0:it]:
                    result.append(list(sorted(set(lst[p1] + lst[p2]))))
    return result


def gen_item_sets(fl, itc, msc_v, it_l):
    if itc > 0:
        fl = [i for i, _ in fl]
    ui_l = combinations(fl, itc)
    if len(ui_l) > 0:
        dfi = sorted([[sorted(val), sum(set(val).issubset(set(item))
                                        for item in it_l)] for val in ui_l])
        print(f"\nC{itc + 2} (Candidate item set):")
        fi_list.extend(dfi)
        print(p_table(dfi))
        cfi = sorted([[sorted(i), ic] for i, ic in dfi if ic >= msc_v])
        return cfi
    else:
        return []


def subset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in subset(seq[1:]):
            yield [seq[0]] + item
            yield item


def search_l(lst, m_list):
    lst = lst[0] if len(lst) == 1 else lst
    f_val = [val[1] for val in m_list if lst == val[0]][0]
    return f_val


def confidence(m_list, s_list, m_conf):
    m_set = set([val for val in s_list])
    # num_val = sum([m_set.issubset(set(val)) for val in item_list])
    num_val = search_l(s_list, fi_list)
    for val in m_list:
        diff = m_set.difference(val)
        # den_val = sum([set(val).issubset(set(i_val)) for i_val in item_list])
        den_val = search_l(val, fi_list)
        f_val = round((num_val / den_val) * 100, 2)
        if f_val >= m_conf:
            c_set.append([val, sorted(diff)])
        print(f"Confidence {val} => {sorted(diff)}")
        print(f"Support count({sorted(m_set)}) / Support count({val})")
        print(f"{num_val}/{den_val} = {f_val}%\n")
    return sorted(c_set)


def apriori(i_list, i_type, ms_pv, m_conf):
    f_rules = []
    if i_type == "p":
        msc_v = ceil((ms_pv * len(i_list)) / 100)
    elif i_type == "v":
        msc_v = ms_pv
    else:
        raise Exception("Invalid option")
    print("\nMinimum support count:", msc_v)
    print("Minimum confidence:", m_conf, "%")
    stl = [item for sublist in i_list for item in sublist]
    ci = sorted([[x, stl.count(x)] for x in set(stl)])
    print("\nC1 (Candidate item set):")
    print(p_table(ci))
    fi = sorted([[i, ic] for i, ic in ci if ic >= msc_v])
    print("\nL1: (Frequent item set):")
    fi_list.extend(fi)
    print(p_table(fi))
    ui = [i for i, _ in fi]
    it = 0
    best_fi = ui
    while len(ui) >= 2:
        n_ui = gen_item_sets(ui, it, msc_v, i_list)
        l_ui = len(n_ui)
        if l_ui > 0:
            print(f"\nL{it + 2} (Frequent item set):")
            print(p_table(n_ui))
            if l_ui > 1 or any(ic >= msc_v for i, ic in n_ui):
                best_fi = [i for i, _ in n_ui]
        else:
            break
        ui = n_ui
        it += 1
    if not any(isinstance(i, list) for i in best_fi):
        p_set = sorted([x for x in subset(best_fi)],
                       key=lambda l: (len(l), l))[1:-1]
        print("\nPossible subsets are:", p_set)
        print("\nDerivation of strong association:")
        f_rules = confidence(p_set, best_fi, m_conf)
    else:
        for sq in best_fi:
            p_set = sorted([x for x in subset(sq)],
                           key=lambda l: (len(l), l))[1:-1]
            print("\nPossible subsets are:", p_set)
            print("\nDerivation of strong association:")
            f_rules = confidence(p_set, sq, m_conf)
    print(f"The strong association rules are:")
    for i, val in enumerate(f_rules):
        if i < len(f_rules) - 1:
            print(f"{val[0]} => {val[1]}", end=", ")
        else:
            print(f"{val[0]} => {val[1]}")


try:
    spacer = "-" * 30
    print(f"{spacer}\nApriori Algorithm\n{spacer}")
    opt = int(input("0: Manual, 1: D1, 2: D2, 3: D3: "))
    if opt == 0:
        nt = int(input("Enter total number of transactions: "))
        if nt < 2:
            raise Exception("Cannot compare using lesser transaction")
        else:
            for t in range(nt):
                ti = input(f"Enter items for transaction {t + 1}: ") \
                    .replace(" ", "").split(",")
                it_list.append(ti)
        msc_o = input("Minimum support count, p: If in percentage, v: Value: ")
        if msc_o.lower() == "p":
            msc_p = int(input("Enter the percentage value: ").replace("%", ""))
            if msc_p < 0 or msc_p > 100:
                raise Exception("Incorrect percentage value entered")
            ms_v = ceil((msc_p * nt) / 100)
        elif msc_o.lower() == "v":
            ms_v = int(input("Enter the value: "))
        else:
            raise Exception("Invalid option")
        min_conf = int(input("Enter the minimum confidence percentage: ")
                       .replace("%", ""))
        if min_conf < 0 or min_conf > 100:
            raise Exception("Incorrect percentage value entered")
        apriori(it_list, msc_o, ms_v, min_conf)
    elif opt == 1:
        apriori(it_list1, "p", 50, 75)
    elif opt == 2:
        apriori(it_list2, "v", 3, 70)
    elif opt == 3:
        apriori(it_list3, "p", 60, 75)
    else:
        raise Exception("Invalid option")
except Exception as e:
    print("Error:", e)
