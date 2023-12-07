import sys
import binascii

# TARGET = [112828097,
#  2238326152,
#  1993558896,
#  112828097,
#  4067235102,
#  2181552515,
#  366294555,
#  1908313947,
#  1790916050,
#  450214191,
#  2564631148,
#  4108033587,
#  498599204,
#  4088814104,
#  4194313765,
#  3904354581,
#  498599204,
#  112828097,
#  2226211470,
#  4194313765,
#  112828097,
#  450214191,
#  4194313765,
#  2226211470,
#  4194313765,
#  1842538941,
#  2366052055,
#  4108033587,
#  2212269721,
#  498599204,
#  4088814104,
#  498599204,
#  112828097,
#  450214191,
#  1908313947,
#  2212269721,
#  4024043002,
#  1842538941,
#  4108033587,
#  4239826220]

def main():
    if len(sys.argv) != 2:
        print("fail")
        sys.exit(1)

    f = [c ^ 31337 for c in [ c + 1337 for c in [binascii.crc32(c.encode("utf-8")) for c in sys.argv[1]]]]

    # if f != TARGET:
    #     print("fail")
    #     sys.exit(1)

    if f[33] ^ f[11] != 3993904924:
        print("fail")
        sys.exit(4)
    if f[21] ^ f[11] != 3993904924:
        print("fail")
        sys.exit(4)
    if f[33] - f[36] != -3573828811:
        print("fail")
        sys.exit(4)
    if f[22] - f[19] != 0:
        print("fail")
        sys.exit(4)
    if f[24] & f[8] != 1778394112:
        print("fail")
        sys.exit(4)
    if f[27] ^ f[34] != 2237993320:
        print("fail")
        sys.exit(4)
    if f[10] ^ f[33] != 2181600067:
        print("fail")
        sys.exit(4)
    if f[27] & f[22] != 4026533409:
        print("fail")
        sys.exit(4)
    if f[4] + f[22] != 8261548867:
        print("fail")
        sys.exit(4)
    if f[29] + f[2] != 2492158100:
        print("fail")
        sys.exit(4)
    if f[8] & f[10] != 144515136:
        print("fail")
        sys.exit(4)
    if f[0] ^ f[33] != 476850158:
        print("fail")
        sys.exit(4)
    if f[21] ^ f[7] != 1802188404:
        print("fail")
        sys.exit(4)
    if f[11] & f[15] != 3767769105:
        print("fail")
        sys.exit(4)
    if f[14] - f[9] != 3744099574:
        print("fail")
        sys.exit(4)
    if f[37] + f[3] != 1955367038:
        print("fail")
        sys.exit(4)
    if f[39] + f[34] != 6148140167:
        print("fail")
        sys.exit(4)
    if f[19] + f[6] != 4560608320:
        print("fail")
        sys.exit(4)
    if f[13] ^ f[28] != 1886049409:
        print("fail")
        sys.exit(4)
    if f[19] + f[39] != 8434139985:
        print("fail")
        sys.exit(4)
    if f[16] ^ f[33] != 124632075:
        print("fail")
        sys.exit(4)
    if f[5] ^ f[16] != 2680151207:
        print("fail")
        sys.exit(4)
    if f[29] ^ f[0] != 453090277:
        print("fail")
        sys.exit(4)
    if f[1] ^ f[32] != 2211691337:
        print("fail")
        sys.exit(4)
    if f[13] ^ f[2] != 2237993320:
        print("fail")
        sys.exit(4)
    if f[28] & f[26] != 2164524689:
        print("fail")
        sys.exit(4)
    if f[2] - f[34] != 85244949:
        print("fail")
        sys.exit(4)
    if f[36] - f[33] != 3573828811:
        print("fail")
        sys.exit(4)
    if f[3] & f[14] != 33555969:
        print("fail")
        sys.exit(4)
    if f[15] - f[9] != 3454140390:
        print("fail")
        sys.exit(4)
    if f[18] - f[24] != -1968102295:
        print("fail")
        sys.exit(4)
    if f[3] - f[39] != -4126998123:
        print("fail")
        sys.exit(4)
    if f[29] - f[2] != -1494959692:
        print("fail")
        sys.exit(4)
    if f[9] & f[13] != 311695368:
        print("fail")
        sys.exit(4)
    if f[17] + f[23] != 2339039567:
        print("fail")
        sys.exit(4)
    if f[23] & f[37] != 76564620:
        print("fail")
        sys.exit(4)
    if f[17] - f[26] != -2253223958:
        print("fail")
        sys.exit(4)
    if f[19] - f[3] != 4081485668:
        print("fail")
        sys.exit(4)
    if f[32] - f[8] != -1678087953:
        print("fail")
        sys.exit(4)
    if f[2] - f[15] != -1910795685:
        print("fail")
        sys.exit(4)
    if f[30] & f[22] != 4060086784:
        print("fail")
        sys.exit(4)
    if f[6] - f[34] != -1542019392:
        print("fail")
        sys.exit(4)
    if f[27] & f[5] != 2147719171:
        print("fail")
        sys.exit(4)
    if f[19] - f[1] != 1955987613:
        print("fail")
        sys.exit(4)
    if f[10] ^ f[38] != 1812378719:
        print("fail")
        sys.exit(4)
    if f[12] ^ f[17] != 453090277:
        print("fail")
        sys.exit(4)
    if f[17] ^ f[18] != 2181616719:
        print("fail")
        sys.exit(4)
    if f[1] + f[10] != 4802957300:
        print("fail")
        sys.exit(4)
    if f[39] - f[28] != 2027556499:
        print("fail")
        sys.exit(4)
    if f[9] & f[11] != 282171427:
        print("fail")
        sys.exit(4)
    if f[16] ^ f[14] != 3887604481:
        print("fail")
        sys.exit(4)
    if f[32] ^ f[26] != 2344519702:
        print("fail")
        sys.exit(4)
    if f[16] ^ f[14] != 3887604481:
        print("fail")
        sys.exit(4)
    if f[15] & f[29] != 145752324:
        print("fail")
        sys.exit(4)
    if f[34] - f[35] != -303955774:
        print("fail")
        sys.exit(4)
    if f[37] & f[30] != 1636976664:
        print("fail")
        sys.exit(4)
    if f[36] & f[32] != 110625984:
        print("fail")
        sys.exit(4)
    if f[39] & f[10] != 2559838252:
        print("fail")
        sys.exit(4)
    if f[1] ^ f[30] != 1994162064:
        print("fail")
        sys.exit(4)
    if f[7] - f[20] != 1795485850:
        print("fail")
        sys.exit(4)
    if f[17] + f[2] != 2106386993:
        print("fail")
        sys.exit(4)
    if f[0] & f[24] != 33555969:
        print("fail")
        sys.exit(4)
    if f[25] - f[35] != -369730780:
        print("fail")
        sys.exit(4)
    if f[31] + f[13] != 4587413308:
        print("fail")
        sys.exit(4)

    print("success")


if __name__ == "__main__":
    main()
