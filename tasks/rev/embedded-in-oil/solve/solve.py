import binascii
import z3


def main():
    f = [z3.BitVec(f"f{i}", 64) for i in range(40)] 
    
    solv = z3.Solver()

    solv.add((f[33] ^ f[11]) == 3993904924) 
    solv.add((f[21] ^ f[11]) == 3993904924)
    solv.add((f[33] - f[36]) == -3573828811)
    solv.add((f[22] - f[19]) == 0)
    solv.add((f[24] & f[8]) == 1778394112)
    solv.add((f[27] ^ f[34]) == 2237993320)
    solv.add((f[10] ^ f[33]) == 2181600067)
    solv.add((f[27] & f[22]) == 4026533409)
    solv.add((f[4] + f[22]) == 8261548867)
    solv.add((f[29] + f[2]) == 2492158100)
    solv.add((f[8] & f[10]) == 144515136)
    solv.add((f[0] ^ f[33]) == 476850158)
    solv.add((f[21] ^ f[7]) == 1802188404)
    solv.add((f[11] & f[15]) == 3767769105)
    solv.add((f[14] - f[9]) == 3744099574)
    solv.add((f[37] + f[3]) == 1955367038)
    solv.add((f[39] + f[34]) == 6148140167)
    solv.add((f[19] + f[6]) == 4560608320)
    solv.add((f[13] ^ f[28]) == 1886049409)
    solv.add((f[19] + f[39]) == 8434139985)
    solv.add((f[16] ^ f[33]) == 124632075)
    solv.add((f[5] ^ f[16]) == 2680151207)
    solv.add((f[29] ^ f[0]) == 453090277)
    solv.add((f[1] ^ f[32]) == 2211691337)
    solv.add((f[13] ^ f[2]) == 2237993320)
    solv.add((f[28] & f[26]) == 2164524689)
    solv.add((f[2] - f[34]) == 85244949)
    solv.add((f[36] - f[33]) == 3573828811)
    solv.add((f[3] & f[14]) == 33555969)
    solv.add((f[15] - f[9]) == 3454140390)
    solv.add((f[18] - f[24]) == -1968102295)
    solv.add((f[3] - f[39]) == -4126998123)
    solv.add((f[29] - f[2]) == -1494959692)
    solv.add((f[9] & f[13]) == 311695368)
    solv.add((f[17] + f[23]) == 2339039567)
    solv.add((f[23] & f[37]) == 76564620)
    solv.add((f[17] - f[26]) == -2253223958)
    solv.add((f[19] - f[3]) == 4081485668)
    solv.add((f[32] - f[8]) == -1678087953)
    solv.add((f[2] - f[15]) == -1910795685)
    solv.add((f[30] & f[22]) == 4060086784)
    solv.add((f[6] - f[34]) == -1542019392)
    solv.add((f[27] & f[5]) == 2147719171)
    solv.add((f[19] - f[1]) == 1955987613)
    solv.add((f[10] ^ f[38]) == 1812378719)
    solv.add((f[12] ^ f[17]) == 453090277)
    solv.add((f[17] ^ f[18]) == 2181616719)
    solv.add((f[1] + f[10]) == 4802957300)
    solv.add((f[39] - f[28]) == 2027556499)
    solv.add((f[9] & f[11]) == 282171427)
    solv.add((f[16] ^ f[14]) == 3887604481)
    solv.add((f[32] ^ f[26]) == 2344519702)
    solv.add((f[16] ^ f[14]) == 3887604481)
    solv.add((f[15] & f[29]) == 145752324)
    solv.add((f[34] - f[35]) == -303955774)
    solv.add((f[37] & f[30]) == 1636976664)
    solv.add((f[36] & f[32]) == 110625984)
    solv.add((f[39] & f[10]) == 2559838252)
    solv.add((f[1] ^ f[30]) == 1994162064)
    solv.add((f[7] - f[20]) == 1795485850)
    solv.add((f[17] + f[2]) == 2106386993)
    solv.add((f[0] & f[24]) == 33555969)
    solv.add((f[11] & f[21]) == 282171427)
    solv.add((f[13] & f[39]) == 4038465544)
    solv.add(f[25] - f[35] == -369730780)
    solv.add(f[31] + f[13] == 4587413308)

    assert solv.check() == z3.sat

    f = [solv.model()[i].as_long() for i in f]

    flag = [None] * len(f)

    for i in range(len(flag)):
        for c in map(chr, range(256)):
            if (binascii.crc32(c.encode("utf-8")) + 1337) ^ 31337 == f[i]:
                flag[i] = c
                break
    print(''.join(flag))

    pass

if __name__ == "__main__":
    main()
