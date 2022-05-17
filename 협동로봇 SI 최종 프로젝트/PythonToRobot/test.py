from indy_utils import indydcp_client as client

indy = client.IndyDCPClient("192.168.0.11", "NRMK-Indy7")
indy.connect()
for i in range(len(indy.get_di())):
    indy.set_do(i, 1)
    print(f"{i}: ", indy.get_do()[i])
for i in range(len(indy.get_di())):
    print(f"{i}: ", indy.get_di()[i])
indy.disconnect()
