"""Client for Astral's Metromare arrivals."""

from asyncio import gather
from datetime import datetime
import ssl
from pathlib import Path

from aiohttp import ClientError, ClientSession, ClientTimeout

from .const import ARRIVALS_PER_DIRECTION, DIRECTIONS
from .timetable import AstralApiError, next_arrivals

BASE_URL = "https://gestionecorse.astralspa.it/api"


class AstralClient:
    """Access the same station and transit endpoints as the Astral website."""

    def __init__(self, session: ClientSession, ssl_context: ssl.SSLContext) -> None:
        self._session = session
        self._ssl_context = ssl_context

    async def _post(self, path: str, body: dict[str, str] | None = None) -> list:
        try:
            async with self._session.post(
                f"{BASE_URL}/{path}",
                json=body,
                ssl=self._ssl_context,
                timeout=ClientTimeout(total=15),
            ) as response:
                response.raise_for_status()
                data = await response.json(content_type=None)
        except (ClientError, TimeoutError, ValueError, ssl.SSLError) as exc:
            raise AstralApiError(f"Impossibile leggere i dati Astral: {exc}") from exc
        if not isinstance(data, list):
            raise AstralApiError("Risposta Astral non valida: elenco atteso")
        return data

    async def async_stations(self) -> dict[str, str]:
        """Return station codes and names offered by Metromare."""
        data = await self._post("fermate/RL_PSP-CC")
        stations: dict[str, str] = {}
        for item in data:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("codice"), str)
                or not isinstance(item.get("nomeFermata"), str)
            ):
                raise AstralApiError("Risposta Astral non valida: stazione")
            stations[item["codice"]] = item["nomeFermata"]
        if not stations:
            raise AstralApiError("Nessuna stazione Metromare disponibile")
        return stations

    async def async_arrivals(
        self, station: str, now: datetime
    ) -> dict[str, tuple[datetime | None, ...]]:
        """Read the next three non-cancelled trains in each direction."""
        results = await gather(
            *(
                self._post("transit", {"percorso": route, "fermata": station})
                for route in DIRECTIONS
            )
        )
        return {
            route: next_arrivals(records, now, ARRIVALS_PER_DIRECTION)
            for route, records in zip(DIRECTIONS, results, strict=True)
        }


def create_ssl_context() -> ssl.SSLContext:
    """Add Astral's omitted intermediate to the system trust store."""
    context = ssl.create_default_context()
    context.load_verify_locations(cafile=Path(__file__).with_name("sectigo_ov_r36.pem"))
    return context
