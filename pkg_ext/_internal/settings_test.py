from pkg_ext._internal.settings import PkgSettings


def test_dev_suffix(settings: PkgSettings):
    assert settings.public_groups_path.name == ".groups.yaml"
    settings.dev_mode = True
    assert settings.public_groups_path.name == ".groups-dev.yaml"
