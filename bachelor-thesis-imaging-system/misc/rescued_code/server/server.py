#!/usr/bin/python
import os
import sys
from socket import *
import shutil

# Set configuration variables
server_host = ""
server_port = 24
server_buffer_size = 4096


# Initiating UDP Server Socket

UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind((server_host, server_port))



def create_image(descr):

	new_id = str(sorted(map(int, os.listdir("images")))[-1] + 1)
	print "Creatin new image", new_id
	os.mkdir("images/" + new_id)
	open("images/" + new_id + "/info", "w").write(descr)

#def execute_command(command):
	print "Command:"+command
	if command == "exit":
		exit()
	elif command == "create image":
		create_image("generic desc")




# Server initialisation
print "Starting Image Server"
print "Loadin images...."
for image in  os.listdir("images"):
	print "ID " + image, ":", open("images/"+image+"/info").read()

# Run forever
while 1:
	data,addr = UDPSock.recvfrom(server_buffer_size)
	data = data[:-1]
	# Get command and send response
	if data == "LIST":
		print "List"
		# Get ID of image or list all images
		requested_id, addr = UDPSock.recvfrom(server_buffer_size)
		requested_id = requested_id[:-1]
		if requested_id == "0":
			images = os.listdir("images")
			# Send number of images
			UDPSock.sendto(str(len(images)) + "\n", addr)
			# Send desription for each image
			for image in images:
				UDPSock.sendto(image + "\n", addr)
				#UDPSock.sendto(open("images/"+image+"/info").read(),addr)
				devices = os.listdir("images/" + image)
				
				UDPSock.sendto(str(len(devices)-1) + "\n", addr)
				for device in devices:
					if device != "info":
						UDPSock.sendto(device + "\n", addr)
						
						versions  = os.listdir("images/" + image + "/" + device)

						UDPSock.sendto(str(len(versions)) + "\n", addr)
						for version in versions:
							
							UDPSock.sendto(version + "\n", addr)
		else:
			# Send description for requested image
			UDPSock.sendto("1", addr)
			UDPSock.sendto(requested_id, addr)
			UDPSock.sendto(open("images/"+requested_id+"/info").read(), addr)

	elif data == "CREATE":
		print "Create"
		
		image_description, addr = UDPSock.recvfrom(server_buffer_size)
		image_description = image_description[:-1]

		image_dev, addr = UDPSock.recvfrom(server_buffer_size)
		image_dev= image_dev[:-1]

		new_id = str(sorted(map(int, os.listdir("images")))[-1] + 1)
		print "Creatin new image", new_id
		os.mkdir("images/" + new_id)
		open("images/" + new_id + "/info", "w").write(image_description)
		os.mkdir("images/" + new_id + "/" + image_dev)
		os.mkdir("images/" + new_id + "/" + image_dev + "/1")
		
		#launching udp-receiver
		os.system("udp-receiver --file images/" + new_id + "/" + image_dev + "/1/" + image_dev)


	elif data == "UPDATE":
		print "Update"
	elif data == "DELETE":
		print "Delete"
		image_id, addr = UDPSock.recvfrom(server_buffer_size)
		image_id = image_id[:-1]
		image_dev, addr = UDPSock.recvfrom(server_buffer_size)
		image_dev = image_dev[:-1]
		image_version, addr = UDPSock.recvfrom(server_buffer_size)
		image_version = image_version[:-1]
		if image_dev == "0":
			shutil.rmtree("images/" + image_id)
		else:
			if image_version == "0":
				shutil.rmtree("images/" + image_id + "/" + image_dev)
			else:
				shutil.rmtree("images/" + image_id + "/" + image_dev + "/" + image_version)
		

	elif data == "REQUEST":
		print "Request"

		image_id, addr = UDPSock.recvfrom(server_buffer_size)
		image_id = image_id[:-1]
		image_dev, addr = UDPSock.recvfrom(server_buffer_size)
		image_dev = image_dev[:-1]
		image_version, addr = UDPSock.recvfrom(server_buffer_size)
		image_version = image_version[:-1]


		#launching udp-receiver
		os.system("udp-sender --file images/" + image_id + "/" + image_dev + "/" + image_version + "/" + image_dev)
	


exit()

# Simple CLI
while 1:
	print ">>",
	input_data = sys.stdin.readline()
	print "Executing " + input_data[:-1] + "."
	execute_command(input_data[:-1])
