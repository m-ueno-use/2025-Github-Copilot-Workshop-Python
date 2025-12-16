from config import Config


def test_default_work_duration_is_25_minutes():
    assert Config.WORK_DURATION == 25 * 60
