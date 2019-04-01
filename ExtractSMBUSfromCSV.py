#!/usr/bin/python
import csv
import sys
myfile = open(sys.argv[1],'rb')
#Get past the initial garbage
myfile.seek(700)
#read a line after that so that we start fresh from a newline.
myfile.readline()
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
	going_high=True
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
	going_high=True
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


start_condition_index_list=[]
def detect_start_condition():
	#Defined as Data line transition from high to low while clock line is high
	for val in data_falling_edge_index_list:
		if (float(clock_val[val]) > clock_high):
			start_condition_index_list.append(val)


stop_condition_index_list=[]
def detect_stop_condition():
	#Defined as Data line transition from low to high while clock line is high
	for val in data_rising_edge_index_list:
		if (float(clock_val[val]) > clock_high):
			stop_condition_index_list.append(val)


start_stop_condition_index_list=[]
def detect_start_stop_condition():
	#Defined as Data line transition from high to low while clock line is high
	for val in data_falling_edge_index_list:
		if (float(clock_val[val]) > clock_high):
			start_stop_condition_index_list.append(val)	
	#Defined as Data line transition from low to high while clock line is high
	for val in data_rising_edge_index_list:
		if (float(clock_val[val]) > clock_high):
			start_stop_condition_index_list.append(val)
	start_stop_condition_index_list.sort()


def remove_start_stop_from_clock_high_list():
#Start condition - find the clock falling edge immediately after the start condition and rising edge immediately prior to start condition-remove/assign the clock high indices which are in between these edges
#Go through the start_stop_condition_list - find the clock_low_indices - immediately prior and after each of the values - remove clock_high_indices - which fall between these low indices
	for val in start_stop_condition_index_list:
		for i,obj in enumerate(clock_low_index_list):
			if (clock_low_index_list[i-1]<val<obj):
				for high_val in clock_high_index_list:
					if (clock_low_index_list[i-1]<high_val<obj):
						clock_high_index_list.remove(high_val)

		
	
	
def print_binary():
	mybinary=[]
	count=1
	for val in clock_high_index_list:
		#check if this clock high index is after a start event
		if float(val)>float(start_condition_index_list[0]):
			#look at every 9th clock high signal - between a start and stop index
			#ACK = data line low
			#NACK = data line high
			if ((count%9) == 0):
				if (float(data_val[val])>data_high):
					mybinary.append('NACK')
					count+=1
				else:
					mybinary.append('ACK')
					count+=1
			else:
				if (float(data_val[val])>data_high):
					mybinary.append('1')
					count+=1
				else:
					mybinary.append('0')
					count+=1
	mybin={}
	myhex={}
	mydec={}
	mydata=[]
	myele=""
	mycount=0
	for ele in mybinary:
		if ((ele =="ACK") or (ele == "NACK")):
			mybin[mycount]=myele
			mydata.append(myele)
			myele=""
			mycount+=1
		else:
			myele+=ele
	print(mybin)
	mycount=0
	for ele in mydata:
		mydec[mycount]=int(ele,2)
		mycount+=1
	print(mydec)
	mycount=0
	for ele in mydata:
		myhex[mycount]=hex(int(ele,2))
		mycount+=1
	print(myhex)


	
	
myfile.close()


detect_clock_high_low_index()
detect_data_high_low_index()
detect_start_condition()
detect_stop_condition()
detect_start_stop_condition()
remove_start_stop_from_clock_high_list()
print_binary()


