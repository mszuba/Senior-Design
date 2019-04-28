gps_data = []

f = open("rx_test.text","r")
f_out = open("output_log_test.text","a")

raw_data = f.readline()

print(str(raw_data))
raw_data = raw_data.replace(" ", "!")
raw_data = raw_data.replace("=","!")
raw_data = raw_data.replace(",","!")
data = raw_data.split('!')
print(data)

n=0
value = 0
while n <len(data):
    try:
        value = float(data[n])
        gps_data.append(value)
    except:
        pass
    n+=1
print(gps_data)

n = 0
while n < len(gps_data):
    f_out.write(str(gps_data[n]))
    f_out.write(',')
    n+=1
f.close()
f_out.close()

