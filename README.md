DNS Attack & Defense Lab – README

Author: Gresa Daqi
Educational Cybersecurity Simulation Project

1. Overview

Ky projekt simulon një skenar real të një sulmi DNS Cache Poisoning dhe mënyrën se si DNSSEC e parandalon atë.
Laboratori është zhvilluar në Python dhe vizualizon hap pas hapi procesin e rezolucionit DNS, përfshirë:

Klienti që kërkon IP për një domain.

Resolver-i që e përcjell kërkesën.

Serveri autoritativ që kthen IP reale.

Sulmuesi që dërgon përgjigje të falsifikuara.

Kontrollimi i paketave deri në momentin që përgjigjja falso pranohet ose refuzohet nga DNSSEC.

2. Features

Simulim i plotë i DNS Cache Poisoning.

Funksionim me dhe pa DNSSEC.

Modelim i paketave DNS (Query, Response).

Validim i Transaction ID, source port dhe firmave DNSSEC.

Topologji e vizualizuar e rrjetit.

Simulim i një faqeje phishing kur sulmi arrin sukses.

3. Projektimi dhe Arkitektura

Strukturë e thjeshtuar e komponentëve kryesorë:

resolver.py – DNS Resolver që ruan cache dhe pranon përgjigje.

dns_server.py – Server autoritativ i cili gjithmonë jep IP reale.

attacker.py – Gjeneron përgjigje të falsifikuara me ID dhe port të rastësishëm.

dnssec_module.py – Kontrollon nënshkrimet DNSSEC.

visuals.py – Diagramet ASCII dhe printimet e animuara.

main.py – Ekzekutimi i të gjithë laboratorit.

4. Kërkesat e instalimit

Instalimi i varësive:

pip install -r requirements.txt


Startimi i laboratorit:

python main.py

5. Komandat kryesore të përdorimit
Startimi i simulimit normal (pa DNSSEC)
python main.py --no-dnssec

Startimi i simulimit me DNSSEC të aktivizuar
python main.py --dnssec

Pastrimi i cache të resolver-it
python main.py --clear-cache

Ekzekutimi i skenarit vetëm për sulmin
python main.py --attack

6. Si funksionon simulimi

Klienti dërgon DNS Query për një domain.

Resolver-i kontrollon cache-in.

Nëse nuk ka cache, kërkesa dërgohet te serveri autoritativ.

Sulmuesi nis disa përgjigje të falsifikuara:

Me ID të ndryshme

Me port të ndryshëm

Resolver-i pranon vetëm përgjigjen e parë që ka:

Transaction ID të saktë

Port të saktë

Nëse DNSSEC është aktiv: kërkon edhe nënshkrimin valid.

Nëse përgjigja e sulmuesit pranohet:

Resolver-i e cache-on IP-në e rreme.

Klienti ridrejtohet në një faqe phishing.

Nëse DNSSEC është aktiv:

Përgjigjet e sulmuara refuzohen.

Kthehet vetëm përgjigja reale e serverit autoritativ.

7. Skenarët e laboratorit
Skenari 1: Pa DNSSEC

Tregohet sa lehtë mund të injektohet një IP false në cache.

Skenari 2: Me DNSSEC

Resolver-i verifikon nënshkrimet dhe refuzon çdo përgjigje të falsifikuar.

Skenari 3: Retry Attack

Sulmuesi tenton derisa të gjejë ID e duhur.

8. Rezultatet e pritshme

Pa DNSSEC: sulmi zakonisht arrin sukses pas disa tentimeve.

Me DNSSEC: sulmi dështon në çdo tentim.

9. Qëllimi edukativ

Ky laborator synon të:

Sqarojë pse DNS është i cenueshëm pa DNSSEC.

Demonstrojë sulmet e manipulimit të trafikut përmes DNS.

Shpjegojë rëndësinë e validimit kriptografik në rrjetet moderne.

Rrisë kuptimin praktik të funksionimit të DNS-it.
