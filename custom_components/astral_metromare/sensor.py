"""Next arrival sensors for both Metromare directions."""

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import ARRIVALS_PER_DIRECTION, CONF_STATION, CONF_STATION_NAME, DIRECTIONS, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create three timestamp sensors for each direction."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AstralArrivalSensor(coordinator, entry, route, destination, position)
        for route, destination in DIRECTIONS.items()
        for position in range(ARRIVALS_PER_DIRECTION)
    )


class AstralArrivalSensor(CoordinatorEntity, SensorEntity):
    """Upcoming arrival adjusted by the delay supplied by Astral."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        route: str,
        destination: str,
        position: int,
    ) -> None:
        super().__init__(coordinator)
        self._route = route
        self._position = position
        # Keep the existing first-train entity IDs and names stable.
        self._attr_name = (
            f"Direzione {destination}"
            if position == 0
            else f"Direzione {destination} - {position + 1}° treno"
        )
        self._attr_unique_id = (
            f"{entry.data[CONF_STATION]}_{route}"
            if position == 0
            else f"{entry.data[CONF_STATION]}_{route}_{position + 1}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data[CONF_STATION])},
            name=f"Metromare {entry.data[CONF_STATION_NAME]}",
            manufacturer="Astral",
        )

    @property
    def native_value(self) -> datetime | None:
        """Return this train's arrival, or unknown when no train remains."""
        return self.coordinator.data[self._route][self._position]
