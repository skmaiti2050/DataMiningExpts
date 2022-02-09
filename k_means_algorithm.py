clusters = []
centroids = []


def c_clusters(c1, c2):
    if len([c for c in c1 if c not in c2]) > 0:
        return False
    return True


def cl_print(cl, s=""):
    print(f"\nThe{s} clusters are:")
    for it, val in enumerate(cl, 1):
        print(f"Cluster {it}:", *val)


def ce_print(ce):
    print("\nThe centroids are:")
    for it, val in enumerate(ce, 1):
        print(f"Centroid {it}: {round(val, 4)}")
    print("-" * 30)


try:
    n = int(input("Enter the number of elements: "))
    if n < 0:
        raise Exception("Numbers of elements cannot be negative")
    else:
        elements = sorted(map(int, input(f"Enter {n} elements: ")
                              .strip().split(" ")))
        if len(elements) < n or len(elements) > n:
            raise Exception("Enter the elements properly")
        nc = int(input("Enter the number of clusters: "))
        if nc < 0 or nc > n:
            raise Exception("Enter a valid number of clusters")
        else:
            for i in range(nc):
                clusters.append([elements[i]])
                centroids.append(elements[i])
            t_sum = sum(elements[j] for j in range(nc - 1, n))
            clusters[nc - 1] = elements[nc - 1:n]
            centroids[nc - 1] = t_sum / (n - nc + 1)
            cl_print(clusters, " initial")
            ce_print(centroids)
            while True:
                n_clusters = [[] for _ in range(nc)]
                for i in range(n):
                    idx, m_ed = 0, float('inf')
                    for j in range(nc):
                        ed = ((centroids[j] - elements[i]) ** 2) ** .5
                        if ed < m_ed:
                            m_ed, idx = ed, j
                    n_clusters[idx].append(elements[i])
                cl_print(n_clusters)
                t_sum = [sum(c) for c in n_clusters]
                centroids = [t_sum[y] / len(n_clusters[y]) for y in range(nc)]
                ce_print(centroids)
                if c_clusters(clusters, n_clusters):
                    clusters = n_clusters[:]
                    break
                clusters = n_clusters[:]
            cl_print(clusters, " final")
except Exception as e:
    print(e)
