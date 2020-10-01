# Lösning September 2020
I textfilen vi får så ser vi några konstiga tecken högst upp. Det visar sig att dessa är emojis. Den tyska flaggan, svärd i kors och en abacus. Detta är en klurig hint som skulle syfta på "german war cipher".

Vi ser att vi får något `sq` och `tk` som vi inte vet vad de är. Vi ser också att vi har fått ett `c`. I krypto brukar detta ofta stå för det krypterade meddelandet (ciphertext) som vi måste knäcka. 

Vi kan se att `c` bara innehåller bokstäverna `adfgvx`. Då `x` och `v` är med kan vi veta att detta inte är en hex-enkodad sträng då den bara skulle innehålla `0-9a-f`. Detta skulle kunna vara en bas64-enkodad sträng, men då den inte innehåller några siffror så gissar vi att så inte är fallet. Man kan också testa att [bas64-dekoda strängen](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)&input=YWFkZGRnYWZkdmFkZGdnZmdmYXZkZ2dkZmdnZGFnZmZmZGR4YWF2Z2Z2Z2ZmZmRnZGR2YWFmZ2FmdmdnZGdkZGZkZmdkYWF4dmZ2ZHZ2ZmZhZmF2ZnZnYXZneHZhZ2dhZ2Z4ZA), men ser att det inte ger så mycket. Ofta (i CTF-sammanhang) när en chiffertext innehåller bokstäver och inte är hex-enkodad eller bas64-enkodad så är det något sorts klassiskt chiffer som har använts.

För att hitta vilket klassiskt chiffer det handlar om gäller det att bara leta, mycket. Ett sätt är att hitta en lista av klassiska chiffer och leta efter vilket som passar. Efter mycket letande kommer vi fram till att det handlar om chiffret [ADFGVX](https://en.wikipedia.org/wiki/ADFGVX_cipher). Att det var detta chiffer det handlade om släpptes även som en hint efter halva månaden.

När vi har läst Wikipedia-sidan om ADFGVX inser vi vad `sq` och `tk` är. `sq` är Polybius-kvadraten och `tk` är transpositions-nyckeln. För att kunna dechiffrera meddelandet behöver vi båda, men vi har ju tyvärr inte `tk`!

Så hur kan vi ta reda på `tk`? Bokstäverna i `tk` spelar ingen roll, bara transpositionen när man sorterar bokstäverna i alfabetsordning. Hur många olika `tk` kan det finnas? Om `tk` innehåller `n` tecken så finns det [`n!`](https://en.wikipedia.org/wiki/Factorial) olika möjliga `tk`. Fakultetsfunktionen växer väldigt snabbt och vi kan läsa på Wikipedia att "In practice, the transposition keys were about two dozen characters long."

`24!` är ungefär `10^23` stort vilket är alldeles för mycket för att testa alla `tk`. Men `12!` är ungefär `10^8`, så vi kan testa alla möjliga `tk` av längd mindre än eller lika med 12.

Sagt och gjort, vi implementerar vår egen dechiffreringskod och brute forcear över alla möjliga `tk` kortare än 13. För att kunna avgöra om en given dechiffrering är den rätta så gissar vi att den innehåller något vanligt engelskt ord så som `this`, `if` eller `we`.

Efter ett tag så hittar vi flaggan med en `tk` av längd 6.

## Disclaimer

Denna uppgift blev mycket svårare och mer oklar än det var tänkt. När jag (Mattias) skapade uppgiften läste jag inte så noga på Wikipedia och antog att `tk` alltid hade längd 6. Därför släppte vi att `tk` hade den längden som en hint senare under månaden. Ett annat oförutsett problem är att filtrera alla möljliga dechiffreringar efter den som faktiskt innehåller flaggan. Då måste man anta att flaggan är på svenska eller engelska för att sedan kunna filtrera baserade på vanliga ord i språket. Vanligtvis är flaggor också skrivna i l33tsp34k vilket inte heller gör det lättare.
