import csv


def carica_da_file(file_path):
    """
    Legge il file CSV e mette i libri in una lista di dizionari.
    """
    biblioteca = []

    # Prova ad aprire il file per la lettura
    try:
        with open(file_path, 'r', newline="", encoding="utf-8") as file_biblioteca:

            # Legge il file usando la virgola come separatore
            reader = csv.reader(file_biblioteca, delimiter=',')

            for row in reader:
                try:
                    # Crea un dizionario per il libro, convertendo i numeri
                    record = {
                        'Titolo': row[0],
                        'Autore': row[1],
                        'Pubblicazione': int(row[2]),
                        'Pagine': int(row[3]),
                        'Sezione': int(row[4]),
                    }
                    biblioteca.append(record)

                except IndexError:
                    # Se la riga ha troppi pochi dati
                    print(f"Attenzione: riga incompleta, saltata.")
                except ValueError:
                    # Se anno, pagine o sezione non sono numeri
                    print(f"Attenzione: riga contiene valori non validi (non numerici).")

    except FileNotFoundError:
        # Se il file non esiste
        print(f"Errore: il file {file_path} non esiste.")
    except Exception as e:
        # Per qualsiasi altro errore
        print(f"Errore imprevisto durante il caricamento.")

    return biblioteca


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """
    Aggiunge un nuovo libro al file se non è già nel catalogo.
    """

    # Controlla se il titolo esiste già
    for dizionario in biblioteca:
        if dizionario['Titolo'].lower() == titolo.lower():
            return None  # Libro duplicato

    # Prepara la riga da scrivere
    nuova_riga = [titolo, autore, anno, pagine, sezione]

    # Apre il file in modalità 'append' (aggiungi in fondo)
    with open(file_path, mode="a", newline="", encoding="utf-8") as file_biblioteca:
        writer = csv.writer(file_biblioteca, delimiter=',')
        writer.writerow(nuova_riga)  # Scrive la riga nel file
        return True  # Aggiunta riuscita


def cerca_libro(biblioteca, titolo):
    """
    Cerca un libro nel catalogo tramite il titolo.
    """
    # Scorre tutti i libri
    for dizionario in biblioteca:
        # Confronta i titoli (ignora maiuscole/minuscole)
        if dizionario['Titolo'].lower() == titolo.lower():
            return dizionario  # Restituisce il libro trovato


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """
    Trova i libri di una certa sezione e li ordina per anno di pubblicazione.
    """
    lista_da_ordinare = []

    # Filtra: prende solo i libri con la sezione richiesta
    for dizionario in biblioteca:
        if dizionario['Sezione'] == sezione:
            lista_da_ordinare.append(dizionario)

    # Ordina la lista basandosi sull'anno ('Pubblicazione')
    lista_da_ordinare.sort(key=lambda x: x['Pubblicazione'])

    return lista_da_ordinare


def main():
    """
    Gestisce il menu del programma.
    """
    file_path = "biblioteca.csv"
    biblioteca = carica_da_file(file_path)  # Carica i dati all'avvio

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Visualizza dati caricati")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            print(biblioteca)  # Stampa l'intera lista

        elif scelta == "2":
            # Controlla che i dati siano stati caricati
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()  # Chiede il titolo
            autore = input("Autore: ").strip()  # Chiede l'autore

            try:  # Chiede e converte i numeri (gestisce l'errore se non sono numeri)
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)

            if libro == True:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro (forse è già presente).")

        elif scelta == "3":
            # Cerca un libro
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)

            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            # Ordina per sezione
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:  # Chiede il numero di sezione
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)

            if titoli:
                print(f'\nSezione {sezione} ordinata:')
                # Stampa solo i titoli
                print("\n".join([f"- {item['Titolo']}" for item in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break

        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()