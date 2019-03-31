!#/usr/bin/python
import csv
myfile = open('SDS00007.csv','rb')
myfile.seek(597)
myreader= csv.reader(myfile)
clock_val=[]
data_val=[]
for row in myreader:
	clock_val.append(row[5])
	data_val.append(row[4])


clock_high = 0.7*float(max(clock_val))
clock_high_index_list=[]
clock_low_index_list=[]
clock_rising_edge_index_list=[]
clock_falling_edge_index_list=[]
def detect_clock_high_low_index():
	going_high=False
	going_low=False
	high_start_index=0
	high_stop_index=0
	low_start_index=0
	low_stop_index=0
	for i,val in enumerate(clock_val):
		if (float(val)<clock_high):
			if not (going_low):
				low_start_index=i
				clock_falling_edge_index_list.append(i)
			if (going_high):high_stop_index=i
			going_low=True
			going_high=False
			if not ((high_start_index+((high_stop_index-high_start_index)/2)) in clock_high_index_list):
				clock_high_index_list.append(high_start_index+((high_stop_index-high_start_index)/2))
		else:
			if not (going_high):
				high_start_index=i
				clock_rising_edge_index_list.append(i)
			if (going_low):low_stop_index=i
			going_low=False
			going_high=True
			if not ((low_start_index+((low_stop_index-low_start_index)/2)) in clock_low_index_list):
					clock_low_index_list.append(low_start_index+((low_stop_index-low_start_index)/2))


data_high = 0.7*float(max(data_val))
data_high_index_list=[]
data_low_index_list=[]
data_rising_edge_index_list=[]
data_falling_edge_index_list=[]
def detect_data_high_low_index():
	going_high=False
	going_low=False
	high_start_index=0
	high_stop_index=0
	low_start_index=0
	low_stop_index=0
	for i,val in enumerate(data_val):
		if (float(val)<data_high):
			if not (going_low):
				low_start_index=i
				data_falling_edge_index_list.append(i)
			if (going_high):high_stop_index=i
			going_low=True
			going_high=False
			if not ((high_start_index+((high_stop_index-high_start_index)/2)) in data_high_index_list):
				data_high_index_list.append(high_start_index+((high_stop_index-high_start_index)/2))
		else:
			if not (going_high):
				high_start_index=i
				data_rising_edge_index_list.append(i)
			if (going_low):low_stop_index=i
			going_low=False
			going_high=True
			if not ((low_start_index+((low_stop_index-low_start_index)/2)) in data_low_index_list):
				data_low_index_list.append(low_start_index+((low_stop_index-low_start_index)/2))


def detect_start_condition():
	#Defined as Data line transition from high to low while clock line is high
	for val in data_falling_edge_index_list:
		if (float(clock_val[val]) > clock_high):
			print("Start condition detected at index:")
			print(val)


def detect_stop_condition():
	#Defined as Data line transition from low to high while clock line is high
	for val in data_rising_edge_index_list:
		if (float(clock_val[val]) > clock_high):
			print("Stop condition detected at index:")
			print(val)


def print_binary():
	mybinary=[]
	for val in clock_high_index_list:
		if (float(data_val[val])>data_high):
			mybinary.append('1')
		else:
			mybinary.append('0')
	print(mybinary)


myfile.close()


detect_clock_high_low_index()
detect_data_high_low_index()
detect_start_condition()
detect_stop_condition()


