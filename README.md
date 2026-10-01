# Astral Metromare

![Logo Astral Metromare: treno stilizzato](custom_components/astral_metromare/brand/logo.png)

Integrazione personalizzata per Home Assistant che mostra i prossimi arrivi
della [Metromare pubblicati da Astral](https://infomobilita.astralspa.it/#!/prossimiArrivi).
Scegli una stazione e consulta i primi tre treni in entrambe le direzioni:
**Cristoforo Colombo** e **Porta San Paolo**.

## Installazione

### Tramite HACS

Se il progetto è disponibile in un repository GitHub pubblico:

1. Apri **HACS** in Home Assistant.
2. Dal menu con i tre puntini scegli **Repository personalizzati**.
3. Inserisci l'URL del repository GitHub e seleziona **Integrazione** come categoria.
4. Aggiungi il repository, cerca **Astral Metromare** in HACS e scaricalo.
5. Riavvia Home Assistant.

### Manuale

1. Copia la cartella `custom_components/astral_metromare` del progetto in
   `<config>/custom_components/astral_metromare` nella tua installazione di
   Home Assistant. Se la cartella `custom_components` non esiste, creala.
2. Riavvia Home Assistant.

## Configurazione

1. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**.
2. Cerca **Astral Metromare** e scegli una stazione dall'elenco.

Per aggiungere un'altra stazione, apri **Impostazioni → Dispositivi e servizi**,
seleziona l'integrazione **Astral Metromare** e usa **Aggiungi servizio**
(*Add service*). Scegli quindi la nuova stazione: ogni stazione ha una
configurazione separata. La stessa stazione non può essere aggiunta due volte.

## Sensori

Per ogni stazione configurata vengono creati **sei sensori**: il prossimo
arrivo, il secondo e il terzo treno verso Cristoforo Colombo e gli stessi tre
arrivi verso Porta San Paolo. I sensori sono raggruppati sotto il dispositivo
**Metromare [nome stazione]**.

Ogni sensore mostra la **data e l'ora previste di arrivo** del relativo treno,
non i minuti rimanenti. Home Assistant può usarli anche nelle dashboard e
nelle automazioni. Gli orari vengono aggiornati ogni minuto, tengono conto
dei ritardi comunicati da Astral ed escludono le corse soppresse.

Se non sono disponibili abbastanza treni futuri, i sensori senza un arrivo
mostrano `unknown`. Se i dati di Astral non sono raggiungibili, i sensori
mostrano `unavailable` fino al successivo aggiornamento riuscito.

## Licenza e versioni

Il progetto è distribuito con [licenza MIT](./LICENSE). Le novità delle
versioni sono elencate nel [changelog](./CHANGELOG.md).
