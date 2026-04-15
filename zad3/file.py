dane = input("Podaj adres IP i maskę (np. 192.168.1.10/24): ")
ip, prefix_str = dane.split('/')
prefix = int(prefix_str)

oktety = [int(x) for x in ip.split('.')]
ip_int = (oktety[0] << 24) | (oktety[1] << 16) | (oktety[2] << 8) | oktety[3]

mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
network_int = ip_int & mask_int
broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)

first_host = network_int + 1
last_host = broadcast_int - 1
num_hosts = (1 << (32 - prefix)) - 2

def formatuj(wartosc):
    p1, p2 = (wartosc >> 24) & 0xFF, (wartosc >> 16) & 0xFF
    p3, p4 = (wartosc >> 8) & 0xFF, wartosc & 0xFF
    return f"{p1}.{p2}.{p3}.{p4: <4} | {p1:08b}.{p2:08b}.{p3:08b}.{p4:08b}"

print(f"\nIP:        {formatuj(ip_int)}")
print(f"Maska:     {formatuj(mask_int)}")
print(f"Sieć:      {formatuj(network_int)}")
print(f"Host 1:    {formatuj(first_host)}")
print(f"Host ost:  {formatuj(last_host)}")
print(f"Broadcast: {formatuj(broadcast_int)}")
print(f"Hostów:    {num_hosts}")