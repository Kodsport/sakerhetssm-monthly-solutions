# Jan 2021

Vi får två filer: `payload.py` och `traffic.pcapng`. I `payload.py` ser vi att koden först tar fram lite data, krypterar den och sedan skickar iväg den över TCP.

Genom att öppna `traffic.pcapng` i Wireshark kan vi få fram vad som skickades över nätverket. Vi får fram att det är den följande HEX-enkodade strängen:

```
f377f83b6834636b2d74684eb958bd670d1d5d17e9ff6f011a18400c1b1c475b04031d54040a045201195d1a030f0d460d0a41e0e43b58035411050d5e16e9ff74011e065a021959e01d1d
```

Så nu har vi det krypterade meddelandet. Nu är frågan vilken kryptering som användes.

```python
def encrypt(data, key):	return bytes([x ^ key[i % len(key)] for (i,x) in enumerate(data)])
```

Det ser ut som ett helt vanlig roterande XOR chiffer. Om man vet att det krypterade meddelandet består av engelsk eller svensk text kan man används frekvensanalys för att få fram meddelandet. Ett annat sätt att knäcka krypteringen är genom att man vet något del av meddelandet. Då det bara är XOR går det då att få fram delar av nyckeln.

I det här fallet ser vi att nyckeln kommer från ett command line argument (`bytearray(sys.argv[1], 'utf-8')`) och det känner vi inte till någon del av. Men själva meddelanden som krypteras ser ut så här: `pickle.dumps(exfil_data)`. Pickle är pythons inbyggda serialiseringsformat. Så man kan ge `pickle.dumps` en variabel och funktionen kommer att returnera en sträng med binär data som representerar den variabeln. Sedan kan datan även laddas in i python igen mha. `pickle,loads`.

Det är datan i `exfil_data` som vi inte känner till. Dock vet vi hur den ser ut ungefär. Så här:

```python
exfil_data = {
	'fqnd': "UNKNOWN",
	'username': "UNKNOWN"
}
```

När pickle ska spara den här variabeln till en binär sträng måste den representera det övergripande formatet för variabeln såväl som datan som vi inte känner till. Genom att själva använda pickle på en liknande variabeln kan vi nog därmed få fram ungefär hur meddelandet såg ut innan det krypterades:

```python
>>> exfil_data = {
...     'fqnd': 'UNKNOWN',
...     'username': 'UNKNOWN'
... }
>>> binascii.hexlify(pickle.dumps(exfil_data))
b'80049523000000000000007d94288c0466716e64948c07554e4b4e4f574e948c08757365726e616d65946802752e'
```

Om vi nu testar att XORa det vi just fick med det krypterade meddelandet borde vi få ut en del av nyckeln för chiffret. Detta går enkelt att göra med CyberChef eller python. Vi får då fram något som ungefär ser ut som en flagga! Om man snyggar till den lite manuellt och skickar in den så visar det sig att det är rätt!
