import math

def mean(d_set):
	return sum(d_set)/len(d_set)


def min_max(d_set, new_min, new_max):
	min_a = min(d_set)
	max_a = max(d_set)
	for i, vi in enumerate(d_set):
		new_vi = ((vi - min_a)/(max_a-min_a)) * (new_max - new_min) + new_min
		print("a" + str(i+1) + " = " + str(round(new_vi,2)))

def z_score(d_set):
	d_mean = mean(d_set)
	v_mean_sq_sum = 0
	std_dev_f = 0
	for i, d_val in enumerate(d_set):
		v_mean = d_val - d_mean
		v_mean_sq = v_mean**2
		v_mean_sq_sum+=v_mean_sq
		print("a" + str(i+1) + " = " + str(v_mean), str(v_mean_sq))
	print("*"*50)
	print("Sum = " + str(v_mean_sq_sum))
	std_dev_sq = v_mean_sq_sum/len(d_set)
	std_dev_f = math.sqrt(std_dev_sq)
	print(str(v_mean_sq_sum/len(d_set)))
	print("Std deviation = " + str(std_dev_f))
	print("*"*50)
	for val in d_set:
		n_val = (val-d_mean)/std_dev_f
		print("a" + str(i+1) + "(new value) = " + str(val) + " - " + str(d_mean) + "/" + str(std_dev_f) + " = " + str(round(n_val,2)))

def d_scaling(d_set):
	temp = max(d_set)
	max_p = len([int(a) for a in str(temp)])
	for i, val in enumerate(d_set):
		n_val = val/(10**max_p)
		print("a" + str(i+1) + "(new value) = " + str(val) + "/10^" + str(max_p) + " = " + str(round(n_val,2)))

try:
	ch = int(input("Enter 1 for min max, 2 for z-score, 3 for decimal scaling: "))
	print("*"*50)
	if ch == 1:
		print("Min Max")
		print("Enter the dataset with a space:")
		dataset1 = list(map(int, input().strip().split()))
		n_min = int(input("Enter new min: "))
		n_max = int(input("Enter new max: "))
		min_max(dataset1, n_min, n_max)
	elif ch == 2:
		print("Z-score")
		print("Enter the dataset with a space:")
		dataset2 = list(map(int, input().strip().split()))
		z_score(dataset2)
	elif ch == 3:
		print("Decimal Scaling")
		print("Enter the dataset with a space:")
		dataset3 = list(map(int, input().strip().split()))
		d_scaling(dataset3)
	else:
		print("Invalid input")
except Exception as e:
	print(e)
