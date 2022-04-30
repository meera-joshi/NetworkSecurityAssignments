import time
from math import sqrt
import statistics

def linearCongruentailGenerator(n):
	modulus = 2**60
	seed = int(time.time())%modulus
	increment = 12345
	multiplier = 16807
	randoms = []
	randoms.append(seed)
	for i in range(n):
		randoms.append(int((randoms[-1]*multiplier+increment))%modulus)

	return randoms

def multiplyWithCarry(n):
	carry = []
	randoms = []
	base = 2**60
	multiplier = int(time.time())%base
	carry.append(1234)
	randoms.append(5679)
	for i in range(n+1):
		randoms.append(int((randoms[-1]*multiplier + carry[-1])%base))
		carry.append(int((randoms[-1]*multiplier + carry[-1])/base))

	randoms.pop(0)

	return randoms

def runsTest(randoms):
	runs, positives, negatives = 0, 0, 0
	median = statistics.median(randoms)
	
	# Checking for start of new run
	for i in range(len(randoms)):
		
		# number of runs
		if (randoms[i] >= median and randoms[i-1] < median) or \
				(randoms[i] < median and randoms[i-1] >= median):
			runs += 1
		
		# number of positive values
		if(randoms[i]) >= median:
			positives += 1
		
		# number of negative values
		else:
			negatives += 1

	runs_exp = ((2*positives*negatives)/(positives+negatives))+1
	stan_dev = sqrt((2*positives*negatives*(2*positives*negatives - positives - negatives))/ \
					(((positives+negatives)**2)*(positives+negatives-1)))

	z = abs(runs-runs_exp)/stan_dev

	return z

def ksTest(randoms):
	randoms.sort()

	D_plus =[]
	D_minus =[]

	N = len(randoms)

	# normalize random numbers to [0,1] by dividing by 2**60 (range)
	for i in range(N):
		randoms[i] = randoms[i]/(2**60)
	  
	# Calculate max(i/N-Ri)
	for i in range(1, N + 1):
	    x = i / N - randoms[i-1]
	    D_plus.append(x)
	  
	# Calculate max(Ri-((i-1)/N))
	for i in range(1, N + 1):
	    y = (i-1)/N
	    y = randoms[i-1]-y
	    D_minus.append(y)
	  
	# Calculate max(D+, D-)
	D = max(max(D_plus), max(D_minus))
	
	return D


def printResult(z_statistic, z_critical, prng, test):
	criteria = "D"
	critical = "D-alpha"
	if test=="Runs Test":
		criteria = "Z"
		critical = "z-critical"

	print(criteria, " value for the sample produced by "+prng+" = ", z_statistic)
	print("For 95% confidence, ", critical, " = ", z_critical)

	if(z_statistic < z_critical):
		print("The sample produced by "+ prng +" passes " + test + "\n")
	else:
		print("The sample produced by "+ prng +" fails " + test + "\n")


def testResult(prng, test, n):
	randoms = []

	if prng == "LCG":
		randoms = linearCongruentailGenerator(n)
	else:
		randoms = multiplyWithCarry(n)

	if test == "Runs Test":
		z_statistic = runsTest(randoms)
		z_critical = 1.96
		printResult(z_statistic, z_critical, prng, "Runs Test")

	else:
		z_statistic = ksTest(randoms)
		z_critical = 1.36/sqrt(n) # for n>=50
		printResult(z_statistic, z_critical, prng, "Kolmogorov-Smirnov Test")


def main():
	n = (int)(input("Enter number of random numbers to be generated and tested\n"))
	
	testResult("LCG", "Runs Test", n)
	testResult("MWC", "Runs Test", n)
	testResult("LCG", "KS Test", n)
	testResult("MWC", "KS Test", n)

if __name__ == '__main__':
    main()

