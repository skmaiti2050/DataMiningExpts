import math

def_dataset = [[4, "N"], [5, "Y"], [8, "N"], [12, "Y"], [15, "Y"]]
print("Enter the dataset")
spacer = "-" * 50


def ceil(num):
    if num - int(num) != 0:
        return int(num) + 1
    else:
        return num


def mean(data):
    return round(sum(data) / len(data), 1)


def median(data):
    mid = len(data) // 2
    if len(data) % 2 == 0:
        d1 = data[mid]
        d2 = data[mid - 1]
        return (d1 + d2) / 2
    else:
        return data[mid]


def boundary(data):
    b_list = []
    for val in data:
        bound = int(data[0] + (data[-1] - data[0]) / 2)
        if val < bound:
            b_list.append(data[0])
        else:
            b_list.append(data[-1])
    return b_list


def eq_width(d_set, wk):
    width = (max(d_set) - min(d_set)) / wk
    width = ceil(width)
    t_bin, m_bin = [], []

    for i in range(0, wk):
        c_bound1 = min(d_set) + (i * width)
        c_bound2 = min(d_set) + ((i + 1) * width)
        for val in d_set:
            if i + 1 != wk:
                if c_bound1 <= val < c_bound2:
                    t_bin.append(val)
            else:
                if c_bound1 <= val <= c_bound2:
                    t_bin.append(val)
        t_bin_str = ", ".join(map(str, t_bin))
        print(f"Bin {i + 1} [{c_bound1}-{c_bound2}) = {t_bin_str}")
        m_bin.append(t_bin)
        t_bin = []
    return m_bin


def eq_depth(d_set, n):
    s_set = [d_set[i:i + n] for i in range(0, len(d_set), n)]
    for i, m_bin in enumerate(s_set):
        s_bin_str = ", ".join(map(str, m_bin))
        print(f"Bin {i + 1} : {s_bin_str}")
    return s_set


def data_calc(bin_set):
    print(f"{spacer}\nBin Mean")
    for i, m_bin in enumerate(bin_set):
        rm_bin = [mean(m_bin) for _ in range(len(m_bin))]
        rm_bin_str = ", ".join(map(str, rm_bin))
        print(f"Bin {i + 1} : {rm_bin_str}")

    print(f"{spacer}\nBin Boundary")
    for i, m_bin in enumerate(bin_set):
        rm_bin_str = ", ".join(map(str, boundary(m_bin)))
        print(f"Bin {i + 1} : {rm_bin_str}")

    print(f"{spacer}\nBin Median")
    for i, m_bin in enumerate(bin_set):
        rm_bin = [median(m_bin) for _ in range(len(m_bin))]
        rm_bin_str = ", ".join(map(str, rm_bin))
        print(f"Bin {i + 1} : {rm_bin_str}")
    print(f"{spacer}")


def entropy(ny, nn, t, val):
    if ny == 0:
        ent = round(-(((ny / t) * 0) + ((nn / t) * math.log(nn / t, 2))), 2)
    elif nn == 0:
        ent = round(-(((ny / t) * math.log(ny / t, 2)) + ((nn / t) * 0)), 2)
    else:
        ent = round(-(((ny / t) * math.log(ny / t, 2)) +
                      ((nn / t) * math.log(nn / t, 2))), 2)
    print(f"Entropy({val}):")
    print(f"\t = -[({ny}/{t})log₂({ny}/{t}) + ({nn}/{t})log₂({nn}/{t})]")
    print(f"\t = {ent}")
    return ent


def sbin(d_set):
    comp = []
    total = len(d_set)
    yes = (sum(val[1] == "Y" for val in d_set))
    no = (sum(val[1] == "N" for val in d_set))

    print(f"\n{spacer}")
    m_ent = entropy(yes, no, total, "D")
    print(f"{spacer}")
    print("Number of classes = 2")
    print(f"Number of yes = {yes}")
    print(f"Number of noes = {no}")

    for val1, val2 in zip(d_set, d_set[1:]):
        print(f"{spacer}")
        print(f"Take adjacent values {val1[0]} & {val2[0]}")

        avg = round((val1[0] + val2[0]) / 2, 2)
        vl_str = "<= " + str(avg)
        vg_str = "> " + str(avg)
        lv_y = sum(val[1] == "Y" for val in d_set if val[0] <= avg)
        lv_n = sum(val[1] == "N" for val in d_set if val[0] <= avg)
        gv_y = sum(val[1] == "Y" for val in d_set if val[0] > avg)
        gv_n = sum(val[1] == "N" for val in d_set if val[0] > avg)
        tl = lv_y + lv_n
        tg = gv_y + gv_n
        print(f"Average = ({val1[0]} + {val2[0]})/2 = {avg}")
        print("|" + "-" * 31 + "|")
        print("|\t|Y\t|N\t|Total\t|")
        print("|" + "-" * 31 + "|")
        print(f"|<={avg}\t|{lv_y}\t|{lv_n}\t|{tl}\t|")
        print(f"|>{avg}\t|{gv_y}\t|{gv_n}\t|{tg}\t|")
        print("|" + "-" * 31 + "|\n")

        e1 = entropy(lv_y, lv_n, tl, vl_str)
        e2 = entropy(gv_y, gv_n, tg, vg_str)
        n_ent = round(((tl / total) * e1) + ((tg / total) * e2), 2)
        gain = round(m_ent - n_ent, 2)
        comp.append([avg, n_ent, gain])
        print(f"\nNet Entropy = {tl}/{total} x {e1} + {tg}/{total} x {e2}")
        print(f"\t    = {n_ent}")
        print(f"Gain({avg}) = entropy(D) - net entropy({avg})")
        print(f"\t   = {m_ent}-{n_ent} = {gain}")
    return comp


def d_split(d_set, c_bound):
    bin1, bin2 = [], []

    for val in d_set:
        if val <= c_bound:
            bin1.append(val)
        else:
            bin2.append(val)

    t_bin1_str = ", ".join(map(str, bin1))
    t_bin2_str = ", ".join(map(str, bin2))
    print(f"Bin 1 <= {c_bound} = {t_bin1_str}")
    print(f"Bin 2 > {c_bound} = {t_bin2_str}")
    m_bin = [bin1, bin2]
    return m_bin


def get_gain(res):
    return res[1]


def pre_sbin(d_set):
    result = sbin(d_set)
    print(f"{spacer}")
    f_result = sorted(result, key=get_gain)
    print(f"Max gain is found for the average value of {f_result[0][0]}")
    print(f"\nThe bins are formed as follows:")
    d_d_set = [val[0] for val in d_set]
    split_d_set = d_split(d_d_set, f_result[0][0])
    data_calc(split_d_set)


try:
    bm = int(input("Enter 1 for unsupervised and 2 for supervised binning: "))
    if bm == 1:
        print("\nEnter dataset values separated by a space:")
        dataset = list(map(int, input().strip().split()))
        if not any(dataset) and len(dataset) >= 0:
            raise Exception("Dataset values are zeroes!")
        dataset.sort()
        k = int(input("\nEnter number of bins: "))
        if k > len(dataset):
            raise Exception("Too many bins!")
        ch = int(input("Enter 1 for equal width, 2 for equal depth binning: "))
        print(f"\n{spacer}")
        bins = []
        if ch == 1:
            bins = eq_width(dataset, k)
            data_calc(bins)
        elif ch == 2:
            eq = int(ceil(len(dataset) / k))
            bins = eq_depth(dataset, eq)
            data_calc(bins)
        else:
            print("Invalid choice")
    elif bm == 2:
        cd = int(input("Enter 1 for default data or 2 for custom dataset: "))
        if cd == 1:
            pre_sbin(def_dataset)
        elif cd == 2:
            t_dataset, f_dataset = [], []
            print("\nEnter dataset values separated by a space:")
            c_dataset_val = list(map(int, input().strip().split()))
            if not any(c_dataset_val) and len(c_dataset_val) >= 0:
                raise Exception("Dataset values are zeroes!")
            print("Enter associated Y/N values respectively by a space")
            c_dataset_class = list(map(str, input().strip().split()))
            if len(c_dataset_val) == len(c_dataset_class):
                for class_inp in c_dataset_class:
                    class_inp = class_inp.upper()
                    if class_inp == "Y" or class_inp == "YES":
                        temp_str = "Y"
                    elif class_inp == "N" or class_inp == "NO":
                        temp_str = "N"
                    else:
                        raise Exception("Invalid input")
                    t_dataset.append(temp_str)
                for x, y in zip(c_dataset_val, t_dataset):
                    f_dataset.append([x, y])
                pre_sbin(f_dataset)
            else:
                raise Exception("Dataset mismatch")
        else:
            print("Invalid input")
    else:
        print("Invalid input")
except Exception as e:
    print(e)
