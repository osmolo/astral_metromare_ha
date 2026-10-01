"""Station selection for Astral Metromare."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .api import AstralApiError, AstralClient, create_ssl_context
from .const import CONF_STATION, CONF_STATION_NAME, DOMAIN


class AstralMetromareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Offer stations retrieved from Astral."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Let the user select a Metromare station."""
        try:
            ssl_context = await self.hass.async_add_executor_job(create_ssl_context)
            stations = await AstralClient(
                async_get_clientsession(self.hass), ssl_context
            ).async_stations()
        except AstralApiError:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
                errors={"base": "cannot_connect"},
            )

        if user_input and CONF_STATION in user_input:
            station = user_input[CONF_STATION]
            if station not in stations:
                errors = {CONF_STATION: "invalid_station"}
            else:
                await self.async_set_unique_id(station)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Metromare {stations[station]}",
                    data={CONF_STATION: station, CONF_STATION_NAME: stations[station]},
                )
        else:
            errors = {}

        options = [
            selector.SelectOptionDict(value=code, label=name)
            for code, name in stations.items()
        ]
        return self.async_show_form(
            step_id="user",
            errors=errors,
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=options, mode=selector.SelectSelectorMode.DROPDOWN
                        )
                    )
                }
            ),
        )
