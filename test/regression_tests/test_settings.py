import lal
import numpy as np
import pytest

from pyseobnr.generate_waveform import GenerateWaveform


@pytest.fixture
def basic_settings():
    m1 = 50.0
    m2 = 30.0
    params_dict = {
        "mass1": m1,
        "mass2": m2,
        "spin1x": 0,
        "spin1y": 0,
        "spin1z": 0.5,
        "spin2x": 0,
        "spin2y": 0,
        "spin2z": 0.1,
        "deltaT": 1 / 2048.0,
        "deltaF": 0.125,
        "f22_start": 0.0157 / ((m1 + m2) * np.pi * lal.MTSUN_SI),
        "phi_ref": 0.0,
        "distance": 1.0,
        "inclination": np.pi / 3.0,
        "f_max": 1024.0,
        "approximant": "SEOBNRv5HM",
        "postadiabatic": False,
    }
    return params_dict


def test_mode_arrays_settings(basic_settings):
    """Checks the behaviour wrt. mode_array setting"""

    # cannot accept both
    value_error = (
        r"Only one setting can be specified between .?ModeArray.? and .?mode_array.?."
    )

    with pytest.raises(
        ValueError,
        match=value_error,
    ):
        _ = GenerateWaveform(basic_settings | {"mode_array": [], "ModeArray": []})

    with pytest.raises(
        ValueError,
        match=value_error,
    ):
        _ = GenerateWaveform(
            basic_settings
            | {"approximant": "SEOBNRv5PHM", "mode_array": [], "ModeArray": []}
        )

    calls_to_check = (
        "generate_td_modes",
        "generate_td_polarizations",
        "generate_fd_polarizations",
    )

    # works with list and tuples
    for approximant in "SEOBNRv5HM", "SEOBNRv5PHM":
        wfm_gen = GenerateWaveform(
            basic_settings
            | {"approximant": approximant, "mode_array": [(2, 2), (3, 3)]}
        )

        for func in calls_to_check:
            _ = getattr(wfm_gen, func)()

        wfm_gen = GenerateWaveform(
            basic_settings
            | {"approximant": approximant, "mode_array": ((2, 2), (3, 3))}
        )

        for func in calls_to_check:
            _ = getattr(wfm_gen, func)()

        # incorrect mode array yields an error
        wfm_gen = GenerateWaveform(
            basic_settings | {"approximant": approximant, "mode_array": [2, 2, 3, 3]}
        )
        for func in calls_to_check:
            with pytest.raises(TypeError):
                _ = getattr(wfm_gen, func)()


def test_f_ref_behaviour(basic_settings):
    """When not set, f_ref should be set to f22_start"""

    assert "f_ref" not in basic_settings  # for this test to work

    approximants = "SEOBNRv5HM", "SEOBNRv5PHM"

    for approximant in approximants:
        wfm_gen = GenerateWaveform(
            basic_settings | {"approximant": approximant, "f_ref": 21, "f22_start": 20}
        )

        assert wfm_gen.parameters["f_ref"] == 21

    # takes value of f22_start if not specified
    for approximant in approximants:
        wfm_gen = GenerateWaveform(
            basic_settings | {"approximant": approximant, "f22_start": 21}
        )

        assert wfm_gen.parameters["f_ref"] == 21

    # inherit default value
    for approximant in approximants:
        new_settings = basic_settings | {"approximant": approximant}
        new_settings.pop("f22_start")
        wfm_gen = GenerateWaveform(new_settings)

        assert wfm_gen.parameters["f_ref"] == wfm_gen.parameters["f22_start"]

    # sanity check
    value_error = r"f_ref has to be positive!"
    with pytest.raises(
        ValueError,
        match=value_error,
    ):
        _ = GenerateWaveform(basic_settings | {"f_ref": -1})
