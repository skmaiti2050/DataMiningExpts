import glob

docs, d_set, d_mag, cos_val, word_list = [], [], [], [], []


def read_text_file(file_path, d_num):
    p_list = [".", ";", ":", "!", "?", "/", "\\",
              ",", "#", "@", "$", "&", ")", "(", "\""]
    with open(file_path, 'r') as f:
        temp = f.read().split()
        nn_temp = [item for item in temp if not item.isdigit()]
        rp_temp = ["".join(x.lower() for x in par
                           if x not in p_list) for par in nn_temp]
        docs.append([d_num, rp_temp]), word_list.append(rp_temp)


def doc_pairs(d_list, check):
    indexes = list(range(0, len(d_list)))
    upg = ([x, y] for x in indexes for y in indexes)
    unique_list(word_list, check)
    for u_doc in d_set:
        if check == "sym":
            d_mag.append(sum(values ** 2 for values
                             in u_doc.values()) ** (1 / 2))
        elif check == "asy":
            d_mag.append(sum(1 for _ in u_doc.values()) ** (1 / 2))
    print("Magnitude values of the documents are as follows:")
    for d_num, mag in enumerate(d_mag):
        print(f"||D{d_num + 1}|| = {round(mag, 3)}")
    for p1, p2 in upg:
        cos_sim(d_set, p1, p2)


def cos_sim(d_org, dp1, dp2):
    if dp1 == dp2:
        cos_val.append([[dp1, dp2], 1.0])
    else:
        num = sum(d_org[dp1][k] * d_org[dp2][k]
                  for k in d_org[dp1] if k in d_org[dp2])
        den = d_mag[dp1] * d_mag[dp2]
        cos_val.append([[dp1, dp2], round(num / den, 3)])


def unique_list(d_list, check):
    if check == "sym":
        for doc in d_list:
            d_set.append(dict(zip(list(doc), [list(doc).count(word)
                                              for word in list(doc)])))
    elif check == "asy":
        for doc in d_list:
            d_set.append(dict(zip(list(doc), [1 for _ in list(doc)])))


def gen_table(t_val):
    ld = len(docs)
    counter = 1
    th = ["D" + str(num) for num in range(1, ld + 1)]
    print("\n", *th, sep="\t\t")
    print("\t" + "_" * ld * 8)
    for x in range(ld):
        print(f"D{x + 1}\t", end="|")
        for y in range(ld):
            if counter % ld == 0:
                print(t_val[x * ld + y][1], end="\t|\n")
            else:
                print(t_val[x * ld + y][1], end="\t|")
            counter += 1
    print("\t" + "‾" * ld * 8)
    hd = sorted(set(val[1] for val in cos_val))[-2]
    hd_idx = cos_val[[val[1] for val in cos_val].index(hd)]
    print(f"Documents D{hd_idx[0][0] + 1} and D{hd_idx[0][1] + 1} "
          f"have the highest similarity with value of {hd_idx[1]}")


for i, file in enumerate(glob.glob("*.txt")):
    if file.endswith(".txt"):
        read_text_file(f"{file}", i + 1)

try:
    print("Document similarity using cosine measure")
    opt1 = "Using symmetric attributes"
    opt2 = "Using asymmetric attributes"
    ch = int(input("1: " + opt1 + ", 2: " + opt2 + ", 3: Both\n"))
    if ch == 1:
        print("\n" + "-" * 50 + "\n" + opt1 + "\n" + "-" * 50 + "\n")
        doc_pairs(docs, "sym")
    elif ch == 2:
        print("\n" + "-" * 50 + "\n" + opt2 + "\n" + "-" * 50 + "\n")
        doc_pairs(docs, "asy")
    elif ch == 3:
        print("\n" + "-" * 50 + "\n" + opt1 + "\n" + "-" * 50 + "\n")
        doc_pairs(docs, "sym"), gen_table(cos_val)
        print("\n" + "-" * 50 + "\n" + opt2 + "\n" + "-" * 50 + "\n")
        d_set, d_mag, cos_val = [], [], []
        doc_pairs(docs, "asy")
    else:
        raise Exception("Invalid choice!")
    gen_table(cos_val), print("-" * 50)
except Exception as e:
    print(e)
