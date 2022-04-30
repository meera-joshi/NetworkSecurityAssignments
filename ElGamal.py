import random
from math import gcd

'''
We take large numbers to be in the range 10^30
to 10^50
'''

def moduloExponent(base, power, modulo):
	if power == 0:
		return base%modulo

	t = moduloExponent(base, power//2, modulo)

	if power%2 == 0:
		return t*t % modulo

	return ((t*t)%modulo)*(base%modulo) % modulo


'''
A utility function that takes a large number q
and generates the key as a large random number 
in the  modulo group of q, whose gcd with q is 1.
'''
def generateKey(q):
	key = random.randint(10**30, q)

	while gcd(key, q) != 1:
		key = random.randint(10**30, q)

	return key


'''
Encrypt Function takes the message and the 
public key as:
	- q (prime of the cyclic group F)
	- g (generator of the cyclic group F)
	- g^a, where a is the private key of receiver

And returns the encrypted message and g^sender_key
'''

def encrypt(message, q, g_power_a, generator):
	# Sender selects its private key from F
	sender_key = generateKey(q)

	# Obtain g^(ak) using h = g^a in the cyclic group of q
	g_power_ak = moduloExponent(g_power_a, sender_key, q)

	#obtain g^k in cyclic group of q
	g_power_k = moduloExponent(generator, sender_key, q)

	#multiply each character in message by g^ak
	encrypted_message = []

	for i in message:
		encrypted_message.append(g_power_ak * ord(i))


	print("\nEncrypted message is: ", encrypted_message)
	print("g^k: ", g_power_k)
	print("g^ak: ", g_power_ak)

	return encrypted_message, g_power_k


'''
Decrypt function takes encrypted message, g^k, receiver key a, q
and calculates g^ak, since a is the private key of sender and is
available to her, divides each value in encrypted message by g^ak 
to obtaine the original message
'''

def decrypt(encrypted_message, g_power_k, receiver_key, q):
	g_power_ak = moduloExponent(g_power_k, receiver_key, q)
	decrypted_message = []

	for item in encrypted_message:
		decrypted_message.append((chr)(item//g_power_ak))

	decrypted_message = ''.join(decrypted_message)

	return decrypted_message

def main():
	q = random.randint(10**30, 10**50)
	receiver_key = generateKey(q)
	generator = random.randint(2,q)

	message = input("Enter original message: ");

	g_power_a = moduloExponent(generator, receiver_key, q)

	encrypted_message, g_power_k = encrypt(message, q, g_power_a, generator)

	decrypted_message = decrypt(encrypted_message, g_power_k, receiver_key, q)

	print("\nDecrypted message is: ", decrypted_message)


if __name__ == '__main__':
    main()
