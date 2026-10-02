# Changelog

Le modifiche rilevanti di Astral Metromare sono documentate qui.

## 1.0.1 - 2026-10-02

- Ignorati i transiti per cui Astral restituisce `Invalid date` come orario,
  evitando che impediscano l'avvio dell'integrazione.

## 1.0.0 - 2026-10-01

- Prima versione dell'integrazione per Home Assistant, configurabile dall'interfaccia.
- Supporto per più stazioni, con una configurazione separata per ciascuna.
- Sei sensori timestamp per stazione: i prossimi tre arrivi verso Cristoforo
  Colombo e i prossimi tre verso Porta San Paolo.
- Aggiornamento ogni minuto degli orari previsti, con ritardi e corse soppresse
  considerati nella selezione dei treni.
- Metadati per l'installazione tramite HACS.
