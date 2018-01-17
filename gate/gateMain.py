from GateIO import GateIO
import json
import pprint as pp

gate = GateIO(
    '822FF026-1E61-47A7-92E0-780E0FD27268',
    'c7b250bc2ddec59a059f782495123e60b4264207cbe6304a00e9b5d840ae88a7'
)

coins = gate.get_coin_balance()
with open('gate/gate.json', 'w') as out:
    json.dump(coins, out)
