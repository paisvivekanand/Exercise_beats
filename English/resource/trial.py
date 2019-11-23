import os

path='/home/ubuntu/headphones/resource'

fil= []

files=os.listdir(path)

for name in files:
	if '.wav' in name:
		fil.append(name)

print(fil)
