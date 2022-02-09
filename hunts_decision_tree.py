import math
from prettytable import PrettyTable

header = ["cust_id", "gender", "car_type",
          "shirt_size", "class"]
dataset = [
    ["1", "m", "family", "small", "c0"],
    ["2", "m", "sports", "medium", "c0"],
    ["3", "m", "sports", "medium", "c0"],
    ["4", "m", "sports", "large", "c0"],
    ["5", "f", "luxury", "small", "c1"],
    ["6", "f", "luxury", "large", "c1"],
    ["7", "f", "sports", "large", "c1"],
    ["8", "m", "luxury", "medium", "c1"],
    ["9", "m", "family", "large", "c0"],
    ["10", "m", "sports", "medium", "c0"]
]


def p_table(c):
    tbl = PrettyTable(header)
    for val in c:
        tbl.add_row(val)
    print(tbl)


def entropy(n1, n2, d):
    if n1 == 0 or n2 == 0:
        return 0
    else:
        return -(((n1 / d) * math.log2(n1 / d)) +
                 ((n2 / d) * math.log2(n2 / d)))


def u_sum(md, it, q, e=""):
    if e == "":
        return sum(d[it] == q for d in md)
    else:
        return sum(d[it] == q and d[4] == e for d in md)


def e_process(d_set, c_ent, c_str=None):
    e_comp = []
    for i, att in enumerate(header[1:-1], 1):
        if att == c_str:
            continue
        else:
            t_cal = []
            print(f"{spacer}\nEntropy of {att}\n{spacer}")
            m_att = sorted(set([j[i] for j in d_set]))
            for val in m_att:
                t = u_sum(d_set, i, val)
                v1 = u_sum(d_set, i, val, "c0")
                v2 = u_sum(d_set, i, val, "c1")
                t_e = entropy(v1, v2, t)
                print(f"\nFor {val}:\n{spacer}")
                print("Count of c0:", v1)
                print("Count of c1:", v2)
                print(f"Entropy ({val}): {round(t_e, 6)}")
                t_cal.append([t, t_e])
            n_ent = 0
            for v in t_cal:
                n_ent += (v[0] / len(d_set)) * v[1]
            g_val = c_ent - n_ent
            print(f"\nNet entropy ({att}):", round(n_ent, 6))
            print(f"Gain ({att}): {round(g_val, 6)}\n")
            e_comp.append([att, g_val])
    mg = max(e_comp, key=lambda x: x[1])
    print(f"{spacer}\nAttribute with max gain: {mg[0]}")
    print(f"Gain ({mg[0]}): {round(mg[1], 6)}")
    return mg[0]


print("The dataset is:")
p_table(dataset)
spacer = "-" * 30
c0_count = u_sum(dataset, 4, "c0")
c1_count = u_sum(dataset, 4, "c1")
d_entropy = entropy(c0_count, c1_count, len(dataset))
print("Count of c0:", c0_count)
print("Count of c1:", c1_count)
print("Entropy of dataset:", round(d_entropy, 6))
r_node = e_process(dataset, d_entropy, None)
print(r_node, "will be the root node of decision tree")
print("\nFor car_type = family, the label is c0")
print("For car_type = luxury, the label is c1")
print("\nThe dataset to be considered to evaluate "
      "car_type = sports is")
c_dataset = [i for i in dataset if i[2] == "sports"]
p_table(c_dataset)
c_c0_count = u_sum(c_dataset, 4, "c0")
c_c1_count = u_sum(c_dataset, 4, "c1")
c_entropy = entropy(c_c0_count, c_c1_count, len(c_dataset))
fl = e_process(c_dataset, c_entropy, "car_type")
print(f"\nFor {fl} = m, the label is c0")
print(f"For {fl} = f, the label is c1")
