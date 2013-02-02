#!/usr/bin/python
# Imaging System Client

import os
import sys
import re
from socket import *
from subprocess import call

# Set configuration variables
server_host = "localhost"
server_port = 24
server_buffer_size = 4096
server_addr = (server_host, server_port)

# Initiating UDP Server Socket

UDPSock = socket(AF_INET,SOCK_DGRAM)


def list_images():


	print "Listing images"
	UDPSock.sendto("LIST" + "\n", server_addr)
	UDPSock.sendto("0" + "\n", server_addr)
	image_no, addr = UDPSock.recvfrom(server_buffer_size)
	image_no = image_no[:-1]
	print "There are ", image_no, "images  on server"
	for i in range(int(image_no)):
		image_id, addr = UDPSock.recvfrom(server_buffer_size)
		image_id = image_id[:-1]
		print "ID:", image_id
		#image_desc, addr = UDPSock.recvfrom(server_buffer_size)
		#print "Description:"
		#print image_desc
		image_devices, addr = UDPSock.recvfrom(server_buffer_size)
		image_devices = image_devices[:-1]
		print "Devices:"
		for j in range(int(image_devices)):
			
			image_device, addr = UDPSock.recvfrom(server_buffer_size)
			image_device = image_device[:-1]
			print " *", image_device, "with following versions:"
			image_versions, addr = UDPSock.recvfrom(server_buffer_size)
			image_versions = image_versions[:-1]
			for k in range(int(image_versions)):
				image_version, addr = UDPSock.recvfrom(server_buffer_size)
				image_version = image_version[:-1]
				print "   -", image_version

			

# Procedure for creating system images (uploading to server)
def create_image():
	print "Creating image"

	# Searching local disks and partitions
	disks =  filter(re.compile("[sh]d.$").search, os.listdir("/dev"))
	print "Available disks:"
	for disk in disks:
		print "*", disk
		partitions =  filter(re.compile(disk + ".+$").search, os.listdir("/dev"))
		for partition in partitions:
			print "   -", partition

	# Description for image
	print "Fill in description for the image (press CTRL-D to finish reading input)"
	image_description = sys.stdin.readline()
	print "Select device to copy"
	image_dev = sys.stdin.readline()[:-1]

	# Upload to server
	print "Start transfer to server (it might take a long time)?[y/n]"
	response = sys.stdin.readline()[:-1]
	if response == "y":
		UDPSock.sendto("CREATE" + "\n", server_addr)

		UDPSock.sendto(image_description + "\n", server_addr)

		UDPSock.sendto(image_dev + "\n", server_addr)

		#launching udp-sender
		os.system("udp-sender --autostart 10 --file /dev/" + image_dev)

#		disks =  filter(re.compile("[sh]d.$").search, os.listdir("/dev"))
#		UDPSock.sendto(str(len(disks)), server_addr)
#
#		for disk in disks:
#			print "Uploading", disk, "to server"
#			UDPSock.sendto(disk, server_addr)
#			
#			partitions =  filter(re.compile(disk + ".+$").search, os.listdir("/dev"))
#			UDPSock.sendto(str(len(partitions)), server_addr)
#			
#			for partition in partitions:
#				print "Uploading", partition, "to server"
#				UDPSock.sendto(partition, server_addr)


def update_image():
	print "Updating image"
	print "Select image ID"
	image_id = sys.stdin.readline()[:-1]
	print "Select device for image"
	image_dev = sys.stdin.readline()[:-1]
	print "Updating Image", image_id, "with device", image_dev
	print "Start transfer to server (it might take a long time)?[y/n]"
	response = sys.stdin.readline()
	if response[:-1] == "y":
		UDPSock.sendto("UPDATE" + "\n", server_addr)
		UDPSock.sendto(image_id + "\n", server_addr)
		UDPSock.sendto(image_dev + "\n", server_addr)
		#launching udp-sender
		os.system("udp-sender --autostart 10 --file /dev/" + image_dev)

def delete_image():
	print "Deleting image"
	print "Select image ID"
	image_id = sys.stdin.readline()[:-1]
	print "Select device for deletion (0 for all devices)"
	image_dev = sys.stdin.readline()[:-1]
	print "Select version for deletion (0 for all version)"
	image_version = sys.stdin.readline()[:-1]
	print "Deleting from  Image", image_id, "version", image_version, "of device", image_dev

	UDPSock.sendto("DELETE" + "\n", server_addr)
	UDPSock.sendto(image_id + "\n", server_addr)
	UDPSock.sendto(image_dev + "\n", server_addr)
	UDPSock.sendto(image_version + "\n", server_addr)

def request_image():
	print "Requesting image"
	print "Select image ID"
	image_id = sys.stdin.readline()[:-1]
	print "Select device"
	image_dev = sys.stdin.readline()[:-1]
	print "Select version"
	image_version = sys.stdin.readline()[:-1]
	print "Requesting from  Image", image_id, "version", image_version, "of device", image_dev
	print "Start transfer from server (it might take a long time)?[y/n]"
	response = sys.stdin.readline()
	if response[:-1] == "y":
		UDPSock.sendto("REQUEST" + "\n", server_addr)
		UDPSock.sendto(image_id + "\n", server_addr)
		UDPSock.sendto(image_dev + "\n", server_addr)
		UDPSock.sendto(image_version + "\n", server_addr)
		
		#launching udp-receiver
		os.system("udp-receiver --file /tmp/" + image_dev)


# Start Program

print "**************************************"
print "*Welcome to the Imaging System Client*"
print "**************************************"
print


while 1:
	print "Available commands:"
	print "l: list images on servers"
	print "c: create image"
	print "u: update image"
	print "d: delete image"
	print "r: request image"
	print "x: exit client"
	print ">>",
	input_data = sys.stdin.readline()
	command = input_data[:-1]
	if command == "l":
		list_images()
	elif command == "c":
		create_image()
	elif command == "u":
		update_image()
	elif command == "d":
		delete_image()
	elif command == "r":
		request_image()
	elif command == "x":
		exit(0)
