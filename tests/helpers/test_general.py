"""Test ev_smart_charging/helpers/general.py"""

from datetime import datetime
from homeassistant.core import State

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ev_smart_charging.const import (
    CONF_MIN_SOC,
    CONF_PCT_PER_HOUR,
    CONF_READY_HOUR,
)
from custom_components.ev_smart_charging.helpers.general import (
    Validator,
    get_parameter,
)

from .const import MOCK_CONFIG_DATA, MOCK_CONFIG_OPTIONS

# We can pass fixtures as defined in conftest.py to tell pytest to use the fixture
# for a given test. We can also leverage fixtures and mocks that are available in
# Home Assistant using the pytest_homeassistant_custom_component plugin.
# Assertions allow you to verify that the return value of whatever is on the left
# side of the assertion matches with the right side.

# pylint: disable=unused-argument
async def test_is_float(hass):
    """Test is_float"""

    assert isinstance(Validator.is_float("0"), bool)
    assert Validator.is_float("0") is True
    assert Validator.is_float("56.4") is True
    assert Validator.is_float("-34.3") is True
    assert Validator.is_float("a") is False
    assert Validator.is_float(None) is False
    assert Validator.is_float("") is False


async def test_is_soc_state(hass):
    """Test is_soc_state"""

    assert Validator.is_soc_state(None) is False
    soc_state = State(entity_id="sensor.test", state="unavailable")
    assert Validator.is_soc_state(soc_state) is False
    soc_state = State(entity_id="sensor.test", state="")
    assert Validator.is_soc_state(soc_state) is False
    soc_state = State(entity_id="sensor.test", state="0.0")
    assert Validator.is_soc_state(soc_state) is True
    soc_state = State(entity_id="sensor.test", state="100.0")
    assert Validator.is_soc_state(soc_state) is True
    soc_state = State(entity_id="sensor.test", state="-0.1")
    assert Validator.is_soc_state(soc_state) is False
    soc_state = State(entity_id="sensor.test", state="100.1")
    assert Validator.is_soc_state(soc_state) is False


async def test_is_price_state(hass):
    """Test is_price_state"""

    assert Validator.is_price_state(None) is False
    price_state = State(entity_id="sensor.test", state="unavailable")
    assert Validator.is_price_state(price_state) is False
    price_state = State(entity_id="sensor.test", state="12.1")
    assert Validator.is_price_state(price_state) is False
    price_state = State(
        entity_id="sensor.test", state="12.1", attributes={"current_price": 12.1}
    )
    assert Validator.is_price_state(price_state) is False
    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": 12.1, "raw_today": None},
    )
    assert Validator.is_price_state(price_state) is False
    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": 12.1, "raw_today": 12.1},
    )
    assert Validator.is_price_state(price_state) is False
    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": 12.1, "raw_today": []},
    )
    assert Validator.is_price_state(price_state) is False

    one_list = [
        {
            "value": 0.0,
            "start": datetime(2022, 10, 1, 14),
            "stop": datetime(2022, 10, 1, 15),
        }
    ]

    thirteen_list = [
        {
            "value": 1.0,
            "start": datetime(2022, 10, 1, 1),
            "stop": datetime(2022, 10, 1, 2),
        },
        {
            "value": 2.0,
            "start": datetime(2022, 10, 1, 2),
            "stop": datetime(2022, 10, 1, 3),
        },
        {
            "value": 3.0,
            "start": datetime(2022, 10, 1, 3),
            "stop": datetime(2022, 10, 1, 4),
        },
        {
            "value": 4.0,
            "start": datetime(2022, 10, 1, 4),
            "stop": datetime(2022, 10, 1, 5),
        },
        {
            "value": 5.0,
            "start": datetime(2022, 10, 1, 5),
            "stop": datetime(2022, 10, 1, 6),
        },
        {
            "value": 6.0,
            "start": datetime(2022, 10, 1, 6),
            "stop": datetime(2022, 10, 1, 7),
        },
        {
            "value": 7.0,
            "start": datetime(2022, 10, 1, 7),
            "stop": datetime(2022, 10, 1, 8),
        },
        {
            "value": 8.0,
            "start": datetime(2022, 10, 1, 8),
            "stop": datetime(2022, 10, 1, 9),
        },
        {
            "value": 9.0,
            "start": datetime(2022, 10, 1, 9),
            "stop": datetime(2022, 10, 1, 10),
        },
        {
            "value": 10.0,
            "start": datetime(2022, 10, 1, 10),
            "stop": datetime(2022, 10, 1, 11),
        },
        {
            "value": 11.0,
            "start": datetime(2022, 10, 1, 11),
            "stop": datetime(2022, 10, 1, 12),
        },
        {
            "value": 12.0,
            "start": datetime(2022, 10, 1, 12),
            "stop": datetime(2022, 10, 1, 13),
        },
        {
            "value": 13.0,
            "start": datetime(2022, 10, 1, 13),
            "stop": datetime(2022, 10, 1, 14),
        },
    ]

    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": 12.1, "raw_today": one_list},
    )
    assert Validator.is_price_state(price_state) is False

    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": None, "raw_today": one_list},
    )
    assert Validator.is_price_state(price_state) is False

    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": 12.1, "raw_today": thirteen_list},
    )
    assert Validator.is_price_state(price_state) is True

    price_state = State(
        entity_id="sensor.test",
        state="12.1",
        attributes={"current_price": None, "raw_today": thirteen_list},
    )
    assert Validator.is_price_state(price_state) is False


async def test_get_parameter(hass):
    """Test get_parameter"""

    config_entry = MockConfigEntry(data=MOCK_CONFIG_DATA, options=MOCK_CONFIG_OPTIONS)
    assert get_parameter(config_entry, CONF_PCT_PER_HOUR) == 8.0
    assert get_parameter(config_entry, CONF_MIN_SOC) == 30.0
    assert get_parameter(config_entry, CONF_READY_HOUR) is None
    assert get_parameter(config_entry, CONF_READY_HOUR, 12) == 12
