import binascii

'''
The idea of the solution is to bruteforce p and q one bit at a time.
So we guess what the first bits of p and q are, when then calculate 
    n = p * q
and
    x = p ^ q
and then we check if this is correct with the given n and x.

After we have found the values of the first bits of p and q we continue with the second bits and so on.

'''

# modular inverse taken from: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def tobin(m, bits=1024):
    return bin(m)[2:].rjust(bits, '0')

n = 74540258648867040062863135858449322843178981369437130356619994744676050767691335794719045071046160143659401163604308690647054658900800612536222132590643956377882925214061788750188638751407616808331311431952102865495784918287042134422173560187179912122341458650851374087467623023709484258595871150821740305369
x = 2286195387303873326474632659024636248805908300189167320386146311621269136901708727023271258271908624399854208056747663456596820324612970530197261752350400
c = 48655092986640268454351773821903930541138115841722891611169914992117517968367859557001234186908412764159317416702962955997004484554857566553884305133693751118408595974542761346043695390620949940410236577126697080261136258162138208129194052268794849145338093089430828567620329156365371672505273855973511084355
e = 0x10001

pq_bits = 512 # p and q are at most 512 bits each

bit_options = [(0, 0), (1, 0), (0, 1), (1, 1)]
potential_pq = [(0, 0)]
for pos in range(pq_bits):
    new_potential_pq = []
    # all pos+1 first bits set to 1
    mask = (1 << (pos + 1)) - 1

    for (p, q) in potential_pq:
        for (dp, dq) in bit_options:
            new_p = p | (dp << pos)
            new_q = q | (dq << pos)
            
            new_n = (new_p * new_q) & mask
            new_x = new_p ^ new_q
            
            #print("newn", tobin(new_n & mask, mask), tobin(n & mask, mask))
            #print("newx", tobin(new_x, mask), tobin(x & mask, mask))
            #print()

            if n & mask == new_n and x & mask == new_x:
                #print("YES")
                new_potential_pq.append((new_p, new_q))

    potential_pq = new_potential_pq
    print("number of options:", len(potential_pq))

# find correct values
pp = 0
qq = 0
for (p, q) in potential_pq:        
    if p*q == n:
        print("Found correct p and q")
        pp = p
        qq = q
        break

# now we have everything we need to reverse the rsa.
d = modinv(e, (pp - 1)*(qq - 1))
m = pow(c, d, n)

print(binascii.unhexlify(hex(m)[2:]))
# And we get the flag, yay!

print("done")
