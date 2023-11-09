from Crypto.Util.number import long_to_bytes

n = 12292225559518463295952584324346619329590218017074437402298252726204489005766878829079387769631422360454329180986004032078909946087654777105999904836768468399277329227803362004518000033485074570047290146974497896775532999622496567825274056580975669744020659849110455648458509218681009065444210365247109862786778075100263755211511296200484357114136681665699269888381879453819907843937748785419560022877982983981083860591706119247371670706284003978472088541834006201891239523711738833127462939547717331700331877472287055575407886192873159041027224622477831658587216373171313660641261081060483382315702239065176688758691
e = 31337
ct = 164736999379931698895807319237584245346948756955935005976504399393594370347746567320880285576316390349025052067734294596871433093260435969869238477728269462528756486082306441941383893401927335950626599710635506706055563428989868840970628546509744069485083971229883850898489759566926512735405254217525110277916371885534150154875709419630347984258079447112605017648629054394462720743409544836542178543340300911070422891092284623168541124873770953583884848868739926621199405711622172288937626579015908941619969899656605219146452918230933386636497055045614823150738553533980529881265404164045508428065832122703072743027
r = 10092903065421105839902780322676101494693663978322881480113710195199528032878266246765166025945038603407040266197900508048041106431248446109346229221545913573488013142609013791056662195901438194871777568774625045688965294165093469548928560421276409953443905443141138943573928521177849860921739289141868929
secret = 8841457815376043947860328204969900134519037317244113240549649227981831557063298438904084743929869790986825689898754433858349830944766530773353692084326079764622924574180560933279922032659853561952338068785691336041075332155772941149961670977439016191329695344352539982324303819779766747956659912344190462

K = GF(r)
PK.<x> = PolynomialRing(K)

def main():
    # p + q = secret (mod r)
    # p = secret - q (mod r)
    # p * q = n (mod r)
    
    ps = (x * (secret - x) - n).roots()
    assert len(ps) == 2

    pr = int(ps[0][0])

    for k in range(2 ** 14):
        p = pr + r * k
        if gcd(p, n) != 1:
            break

    q = n // p
    assert p * q == n

    d = pow(e, -1, (p - 1) * (q - 1))

    print(long_to_bytes(pow(ct, d, n)))


if __name__ == "__main__":
    main()
