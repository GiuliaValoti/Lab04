import csv

# ==========================================
# CLASSI PER GLI STAND
# ==========================================

class Stand:
    def __init__(self, codice: str, superficie: float, padiglione: int, prezzo_base: float):
        self._codice = codice
        self._superficie = superficie
        self._padiglione = padiglione
        self._prezzo_base = prezzo_base
        self._espositore = None

    @property
    def codice(self) -> str:
        return self._codice

    @property
    def superficie(self) -> float:
        return self._superficie

    @property
    def padiglione(self) -> int:
        return self._padiglione

    @property
    def prezzo_base(self) -> float:
        return self._prezzo_base

    @property
    def espositore(self):
        return self._espositore

    @espositore.setter
    def espositore(self, espositore):
        self._espositore = espositore

    @property
    def disponibile(self) -> bool:
        return self._espositore is None

    def calcola_prezzo(self) -> float:
        return self._prezzo_base

    def __eq__(self, other):
        if not isinstance(other, Stand):
            return False
        return self._codice == other.codice

    def __lt__(self, other):
        if not isinstance(other, Stand):
            return NotImplemented
        return self.calcola_prezzo() < other.calcola_prezzo()

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self._espositore.codice}"
        return f"{self._codice}: Standard | {self._superficie} mq - Padiglione {self._padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"


class StandPreseExtra(Stand):
    def __init__(self, codice: str, superficie: float, padiglione: int, prezzo_base: float, numero_prese: int):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self._numero_prese = numero_prese

    @property
    def numero_prese(self) -> int:
        return self._numero_prese

    def calcola_prezzo(self) -> float:
        return self._prezzo_base * (1 + 0.07 * self._numero_prese)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self._espositore.codice}"
        return f"{self._codice}: Prese Extra | {self._superficie} mq - Padiglione {self._padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self._numero_prese} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice: str, superficie: float, padiglione: int, prezzo_base: float, posizione: str):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self._posizione = posizione

    @property
    def posizione(self) -> str:
        return self._posizione

    def calcola_prezzo(self) -> float:
        return self._prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self._espositore.codice}"
        return f"{self._codice}: Premium ({self._posizione}) | {self._superficie} mq - Padiglione {self._padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"


# ==========================================
# CLASSE PER GLI ESPOSITORI
# ==========================================

class Espositore:
    def __init__(self, codice: str, nome: str, cognome: str):
        self._codice = codice
        self._nome = nome
        self._cognome = cognome
        self._stand = None

    @property
    def codice(self) -> str:
        return self._codice

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cognome(self) -> str:
        return self._cognome

    @property
    def stand(self):
        return self._stand

    @stand.setter
    def stand(self, stand):
        self._stand = stand

    def __eq__(self, other):
        if not isinstance(other, Espositore):
            return False
        return self._codice == other.codice

    def __str__(self):
        info_stand = f"Stand: {self._stand.codice}" if self._stand else "Nessuno stand assegnato"
        return f"{self._codice} - {self._nome} {self._cognome} ({info_stand})"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome_centro = nome
        self.stand_list = []
        self.espositori_list = []

    """Aggiungere setter e getter se necessari"""

    def get_nome(self):
        return self.nome_centro

    def set_nome(self, nuovo_nome):
        self.nome_centro = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        import csv
        self.stand_list.clear()
        self.espositori_list.clear()

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                        continue

                    codice = row[0].strip()

                    if codice.startswith("ST"):
                        superficie = float(row[1])
                        padiglione = int(row[2])
                        prezzo_base = float(row[3])

                        if len(row) == 4:
                            s = Stand(codice, superficie, padiglione, prezzo_base)
                        elif len(row) == 5:
                            extra = row[4].strip()
                            if extra.isdigit():
                                s = StandPreseExtra(codice, superficie, padiglione, prezzo_base, int(extra))
                            else:
                                s = StandPremium(codice, superficie, padiglione, prezzo_base, extra)
                        self.stand_list.append(s)

                    elif codice.startswith("ES"):
                        nome_esp = row[1].strip()
                        cognome_esp = row[2].strip()
                        e = Espositore(codice, nome_esp, cognome_esp)
                        self.espositori_list.append(e)

        except FileNotFoundError:
            raise FileNotFoundError("File non trovato.")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand_trovato = None
        for s in self.stand_list:
            if s.codice == codice_stand:
                stand_trovato = s
                break

        espositore_trovato = None
        for e in self.espositori_list:
            if e.codice == codice_espositore:
                espositore_trovato = e
                break

        if not stand_trovato:
            raise ValueError(f"Stand {codice_stand} non trovato.")
        if not espositore_trovato:
            raise ValueError(f"Espositore {codice_espositore} non trovato.")
        if not stand_trovato.disponibile:
            raise ValueError(f"Lo stand {codice_stand} è già assegnato.")
        if espositore_trovato.stand is not None:
            raise ValueError(f"L'espositore {codice_espositore} ha già uno stand assegnato.")

        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        if not self.espositori_list:
            print("Nessun espositore presente.")
            return
        for e in self.espositori_list:
            print(e)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand_list)

