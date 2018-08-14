# ## Hard Way lol Tons thinking of conversions...
# # Create dictionary to convert to base64
# base64List = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',\ 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',\
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',\ 't', 'u', 'v', 'w', 'x', 'y', 'z',\
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9','+', '/']

# ## Helper to generate the dictionary
# # genBase64Table = [chr(x+40) for x in range(90)]

# # Generate dict from list 
# base64Table = {c: pos for pos,c in enumerate(base64List)}




# ## Convert each letter to a six bit repr
# four_six_bits  = []
# for f in frame:
# 	if not f== "=":
# 		temp = bin(base64Table[f])[2:]
# 	else:
# 		temp= "0"
# 	# Check length, append zeros to make 6 bits
# 	temp_len = len(temp)
# 	if(temp_len>5):
# 		four_six_bits.append(temp)
# 	else:
# 		pre = "0"* (6-temp_len)
# 		four_six_bits.append(pre + temp)


# bin_string = ''.join(four_six_bits)
# three_bytes = []
# temp =""


# # Parse bit string to create bytes
# for pos, x in enumerate(bin_string):
# 	if(pos%8 ==0):
# 		if(len(temp)==8):
# 			three_bytes.append(temp)	
# 		temp = x
# 	else:
# 		temp += x
# three_bytes.append(temp)

# ## Check the endings
# print(four_six_bits[-3:-1])
# print(three_bytes[-3:-1])

# ## Convert list of bytes as str into a byte array
# int_three_bytes = [int(s, 2) for s in three_bytes]
# byte_array = bytearray(int_three_bytes)



# Save png from byte array
# with open('ts{}.png'.format(time.strftime("%d-%b-%Y-%H.%M.%S ", time.gmtime())), 'wb') as f:
# 	f.write(byte_array)
# with open('ts.png', 'wb') as f:
#  	f.write(sec_byte_array)

# img = cv.imread('ts.png',1)
