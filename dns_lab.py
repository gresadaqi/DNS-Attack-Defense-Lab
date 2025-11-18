from enum import Enum, auto
import time
import random

# ===================== NGJYRAT ============================
R = "\033[91m"   # red
G = "\033[92m"   # green
Y = "\033[93m"   # yellow
C = "\033[96m"   # cyan
W = "\033[0m"    # reset


# ===================== MODI I SIGURISË =====================

class SecurityMode(Enum):
    INSECURE = auto()
    SECURE = auto()


# ===================== HELPERA ============================

def slow_print(text, delay=0.7):
    """Print + sleep pak, që me pas kohë me shpjegu."""
    print(text)
    time.sleep(delay)


def pause():
    input(C + "\n→ Vazhdo me ENTER..." + W)


def print_topology():
    print(C + r"""
                      SKENARI: WIFI DNS SPOOFING

                            [   KLIENDI (viktima)   ]
                                       |
                                       |
                             [  WiFi Router DNS  ]
                                   (resolver)
                                  /          \
                                 /            \
                       [ SULMUESI ]        [ AUTH DNS SERVER ]
    """ + W)


# ===================== MODEL I PAKETËS =====================

class Packet:
    def __init__(self, src_ip, dst_ip, src_port, dst_port,
                 dns_id, qname, answer_ip=None, is_response=False, note=""):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.dns_id = dns_id
        self.qname = qname
        self.answer_ip = answer_ip
        self.is_response = is_response
        self.note = note

    def pretty_print(self):
        print(Y + "------------------------------ PACKET --------------------------------" + W)
        print(f"[NET ] SRC IP: {self.src_ip}  →  DST IP: {self.dst_ip}")
        print(f"[UDP ] SRC PORT: {self.src_port} → DST PORT: {self.dst_port}")
        qr = "Response" if self.is_response else "Query"
        print(f"[DNS ] ID: 0x{self.dns_id:04X}   {qr}   QNAME: {self.qname}")
        if self.answer_ip:
            print(f"[DATA] ANSWER: {self.qname} → {self.answer_ip}")
        if self.note:
            print(f"[INFO] {self.note}")
        print(Y + "------------------------------------------------------------------------" + W)


# ===================== FAQJA FAKE E BANKËS =================

def fake_login_page(domain, fake_ip):
    print(R + """
=================== BANKA E KOSOVËS (FAKE) ===================

  Welcome to Online Banking Secure Login


    Username: [______________]
    Password: [______________]

  SERVER IP  : http://""" + fake_ip + """
  REAL SITE  : https://""" + domain + """

  Kjo faqe DUKET e sigurt,
  por në të vërtetë kontrollohet nga sulmuesi.

===============================================================""" + W)


# ===================== TIMELINE – INSECURE =================

def explain_attack_timeline_insecure():
    print(Y + "\n[ATTACK TIMELINE - INSECURE MODE]" + W)
    slow_print("1) Viktima hap: https://bankaeKosoves.com")
    slow_print("2) WiFi router pyet DNS: 'Cila është IP e kësaj banke?'")
    slow_print("3) Sulmuesi në të njëjtin WiFi e sheh DNS kërkesën.")
    slow_print("4) Sulmuesi dërgon I PARI një përgjigje të rreme: IP = 6.6.6.6")
    slow_print("5) Routeri e beson përgjigjen e rreme dhe e ruan në cache.")
    slow_print("6) Viktima ridrejtohet në faqen FALSE të bankës.")
    slow_print("7) Kredencialet mund të vidhen në atë moment.")
    pause()


# ===================== TIMELINE – SECURE ===================

def explain_timeline_secure():
    print(G + "\n[DEFENSE TIMELINE - SECURE MODE]" + W)
    slow_print("1) Viktima hap: https://bankaeKosoves.com")
    slow_print("2) WiFi router gjeneron DNS ID random + port random.")
    slow_print("3) Sulmuesi tenton të dërgojë përgjigje të rreme.")
    slow_print("4) Resolveri kontrollon: ID, port dhe nënshkrimin (DNSSEC-like).")
    slow_print("5) Përgjigjja e sulmuesit nuk kalon kontrollet → DROPPED.")
    slow_print("6) Vjen përgjigjja e vërtetë nga serveri autoritativ.")
    slow_print("7) Vetëm ajo përgjigje pranohet dhe ruhet në cache.")
    pause()


# ===================== EXPLAIN LIKE I'M 5 ==================

def explain_like_5():
    print_topology()
    print(C + "EXPLAIN LIKE I'M 5 – ÇKA PO NDODH KËTU?\n" + W)

    slow_print("Imagjino që do me gjet rrugën për te Banka e Kosovës.")
    slow_print("Ti pyet: 'Kush ma tregon adresën e bankës?' → ky është DNS serveri.")
    slow_print("Zakonisht DNS të tregon rrugën e SAKTË.\n")

    slow_print(R + "Por në rrugë ka një mashtrues (sulmuesi)..." + W)
    slow_print(R + "Ai bërtet më shpejt: 'Ej, banka është te shtëpia ime, hajde këtu!'" + W)
    slow_print("Ti nuk e din që ai po rren, sepse nuk e verifikon kush po flet.")
    slow_print("Kështu funksionon DNS spoofing në rrjetet publike WiFi.\n")

    slow_print(G + "Si e rregullojmë këtë problem?" + W)
    slow_print("Ne i japim DNS serverit disa superfuqi të reja:")
    slow_print("  • Një kod sekret (Transaction ID) 16-bit.")
    slow_print("  • Një derë të fshehur (random UDP port).")
    slow_print("  • Një nënshkrim dixhital (DNSSEC-like signature).\n")

    slow_print("Kur mashtruesi flet, DNS pyet:")
    slow_print('  "A e ke ID-në e saktë? A e ke portin e saktë? A e ke nënshkrimin?"')
    slow_print(R + "Sulmuesi: 'Jo...' → përgjigjja hidhet në mbeturina.\n" + W)

    slow_print(G + "Vetëm serveri i vërtetë i bankës i plotëson të tre kushtet." + W)
    slow_print("Prandaj viktima përfundon në faqen ORIGJINALE, jo në phishing.")
    pause()


# ===================== SKENARI 1 – INSECURE ===============

def scenario_insecure():
    domain = "bankaeKosoves.com"
    real_ip = "93.184.216.34"
    fake_ip = "6.6.6.6"

    print_topology()
    print(R + "========== INSECURE DNS SCENARIO ==========\n" + W)

    dns_id = random.randint(0, 0xFFFF)

    slow_print(Y + "=============== CLIENT MAKES DNS QUERY ===============" + W, 0.8)
    print("[CLIENT] Asking for:", domain, "\n")

    q = Packet("192.168.0.10", "192.168.0.1", 53000, 53, dns_id, domain,
               note="Client → Resolver")
    q.pretty_print()
    time.sleep(0.7)

    print(R + "[ATTACKER] Saw query for", domain, "→ sending SPOOF!" + W)
    forged = Packet("8.8.8.8", "192.168.0.1", 53, 53000, dns_id, domain,
                    answer_ip=fake_ip,
                    is_response=True,
                    note="FORGED malicious redirection")
    time.sleep(0.7)
    forged.pretty_print()

    print(C + "\n===== RESOLVER VALIDATION (INSECURE) =====" + W)
    slow_print(R + "[FORGED] Resolver ACCEPTS forged answer (pa kontrolle shtesë)." + W, 1.0)

    fake_login_page(domain, fake_ip)
    explain_attack_timeline_insecure()


# ===================== SKENARI 2 – SECURE =================

def scenario_secure():
    domain = "bankaeKosoves.com"
    real_ip = "93.184.216.34"
    fake_ip = "6.6.6.6"

    print_topology()
    print(G + "========== SECURE DNS SCENARIO (DNSSEC-like) ==========\n" + W)

    dns_id = random.randint(0, 0xFFFF)
    client_port = random.randint(1024, 65535)

    slow_print(Y + "=============== CLIENT MAKES DNS QUERY ===============" + W, 0.8)
    print("[CLIENT] Asking for:", domain, "\n")

    q = Packet("192.168.0.10", "192.168.0.1", client_port, 53, dns_id, domain,
               note="Client → Resolver")
    q.pretty_print()
    time.sleep(0.7)

    print(R + "[ATTACKER] Saw query for", domain, "→ sending SPOOF!" + W)
    forged = Packet("8.8.8.8", "192.168.0.1", 53, client_port, dns_id, domain,
                    answer_ip=fake_ip,
                    is_response=True,
                    note="FORGED malicious redirection")
    time.sleep(0.7)
    forged.pretty_print()

    print(C + "\n===== RESOLVER VALIDATION (SECURE) =====" + W)
    slow_print("1) Kontrollon nëse ka query aktiv me këtë ID dhe port...")
    slow_print("2) Kontrollon nënshkrimin DNSSEC (këtu e simulojmë thjesht).")
    slow_print(R + "→ Përgjigja e sulmuesit NUK ka nënshkrim të vlefshëm." + W)
    slow_print(R + "[DROP] Forged response është HEDHUR." + W, 1.0)

    print(G + "\n== AUTH SERVER: SENDING REAL RESPONSE ==" + W)
    real = Packet("8.8.8.8", "192.168.0.1", 53, client_port, dns_id, domain,
                  answer_ip=real_ip,
                  is_response=True,
                  note="Real authoritative answer with valid signature.")
    time.sleep(0.8)
    real.pretty_print()

    print(G + "\n===== RESOLVER VALIDATION (SECURE) CONT. =====" + W)
    slow_print(G + "[ACCEPT] ID OK, port OK, signature OK → response ACCEPTED." + W)
    slow_print(G + "Resolver cache updated:", 0.4)
    print(G + f"  {domain} → {real_ip}" + W)

    explain_timeline_secure()


# ===================== STEP BY STEP – LAYERS ==============

def scenario_step_by_step():
    print_topology()
    print(C + "========== STEP BY STEP – Mbrojtja në çdo shtresë ==========\n" + W)

    slow_print("HAPI 1/5 – NETWORK LAYER (IP & routing)")
    print(" - Këtu shohim vetëm adresat IP dhe se kush po flet me kë.")
    print(" - Sulmuesi mund të SPOOF-ojë IP burimore (spoofed source IP).")
    pause()

    slow_print("HAPI 2/5 – TRANSPORT LAYER (UDP Ports)")
    print(" - DNS përdor UDP port 53.")
    print(" - Në sistemin e vjetër, porta e klientit shpesh është e parashikueshme.")
    print(" - Kjo e bën më të lehtë të gjesh kombinimin e saktë për sulm.")
    pause()

    slow_print("HAPI 3/5 – APPLICATION LAYER (DNS protokolli)")
    print(" - Këtu kemi ID-në e transaksionit dhe emrin e domain-it.")
    print(" - Sulmuesi duhet të gjejë ID-në e saktë + portin e klientit.")
    print(" - Nëse i gjen, mund të fusë një përgjigje të rreme në cache.")
    pause()

    slow_print("HAPI 4/5 – DNS CACHE POISONING")
    print(" - Pasi përgjigja e rreme pranohet, routeri ruan IP-në e sulmuesit.")
    print(" - Të gjithë përdoruesit tjerë në atë WiFi shkojnë te IP e rreme.")
    print(" - Ky është problemi kryesor që po simulojmë në këtë projekt.")
    pause()

    slow_print("HAPI 5/5 – MASAT MBROJTËSE (Defense)")
    print(" - Randomizim i porteve UDP.")
    print(" - ID e paparashikueshme për çdo query.")
    print(" - DNSSEC (nënshkrime dixhitale mbi zonën DNS).")
    print(" - Monitorim i trafikut anormal në rrjet (IDS/IPS).")
    pause()


# ===================== MENU KRYESORE ======================

def main_menu():
    while True:
        print(C + "\n========== DNS ATTACK LAB ==========" + W)
        print("1) Skenari 1 – Insecure DNS (sulm i suksesshëm)")
        print("2) Skenari 2 – Secure DNS (mbrojtje DNSSEC-like)")
        print("3) Mbrojtja hap-pas-hapi (Step by step)")
        print("4) Explain Like I'm 5 (shpjegim i thjeshtë)")
        print("0) Dalje")
        choice = input("Zgjedh një opsion: ").strip()

        if choice == "1":
            scenario_insecure()
        elif choice == "2":
            scenario_secure()
        elif choice == "3":
            scenario_step_by_step()
        elif choice == "4":
            explain_like_5()
        elif choice == "0":
            print("Dalje...")
            break
        else:
            print(R + "Opsion i pavlefshëm." + W)


if __name__ == "__main__":
    random.seed()
    main_menu()
