from pyqvrpro.client import Client as qvrpro
from pyqvrpro.client import AuthenticationError
import pytest
import vcr


def _get_instance():
    return qvrpro('pyqvruser', '!pyqvrtest123', '10.7.7.100')


@vcr.use_cassette('fixtures/vcr_cassettes/login.yaml')
def test_login():
    """Test connection to QVR"""

    instance = _get_instance()

    assert instance.authenticated is True

@vcr.use_cassette('fixtures/vcr_cassettes/invalid_auth.yaml')
def test_invalid_auth():
    """Test invalid auth"""

    with pytest.raises(AuthenticationError):
        qvrpro('pyqvruser', 'invalidpw', '10.7.7.100')



@vcr.use_cassette('fixtures/vcr_cassettes/camera_list.yaml')
def test_camera_list():
    instance = _get_instance()

    response = instance.list_cameras()

    assert len(response['datas']) == 3
    assert response['total_channel_num'] == 3
    assert bool(response['success']) is True


@vcr.use_cassette('fixtures/vcr_cassettes/camera_snapshot.yaml')
def test_get_snapshot():
    instance = _get_instance()

    camera_list = instance.list_cameras()

    guid = camera_list['datas'][0]['guid']

    response = instance.get_snapshot(guid)

    assert isinstance(response, bytes)


@vcr.use_cassette('fixtures/vcr_cassettes/camera_capability.yaml')
def test_get_camera_capability():
    instance = _get_instance()

    response = instance.get_capability(ptz=True)

    expected_keys = ['camera_motion', 'motion_manual', 'alarm_input',
                     'alarm_input_manual', 'alarm_pir', 'alarm_pir_manual',
                     'alarm_output', 'iva_crossline_manual',
                     'iva_audio_detected_manual',
                     'iva_tampering_detected_manual', 'iva_intrusion_detected',
                     'iva_intrusion_detected_manual',
                     'iva_digital_autotrack_manual', 'cameraControl']

    assert set(expected_keys).issubset(response.keys())


@vcr.use_cassette('fixtures/vcr_cassettes/event_capability.yaml')
def test_get_event_capability():
    instance = _get_instance()

    response = instance.get_capability()

    expected_keys = ['camera_motion', 'motion_manual',
                     'alarm_input', 'alarm_input_manual',
                     'alarm_pir', 'alarm_pir_manual',
                     'alarm_output', 'iva_crossline_manual',
                     'iva_audio_detected_manual',
                     'iva_tampering_detected_manual',
                     'iva_intrusion_detected',
                     'iva_intrusion_detected_manual',
                     'iva_digital_autotrack_manual']

    assert set(expected_keys).issubset(response.keys())


@vcr.use_cassette('fixtures/vcr_cassettes/channel_list.yaml')
def test_get_channel_list():
    instance = _get_instance()

    response = instance.get_channel_list()

    expected_keys = ['respType', 'total_channel_num', 'used_channel_num',
                     'channels']

    assert set(expected_keys).issubset(response.keys())


@vcr.use_cassette('fixtures/vcr_cassettes/channel_streams.yaml')
def test_get_channel_streams():
    instance = _get_instance()

    channels = instance.get_channel_list()

    guid = channels['channels'][0]['guid']

    response = instance.get_channel_streams(guid)

    expected_keys = ['respType', 'channelIndex', 'guid', 'streams']

    assert set(expected_keys).issubset(response.keys())
    assert response['guid'] == guid


@vcr.use_cassette('fixtures/vcr_cassettes/channel_live_stream_rtsp.yaml')
def test_get_channel_live_stream():
    instance = _get_instance()

    channels = instance.get_channel_list()

    guid = channels['channels'][0]['guid']

    response = instance.get_channel_live_stream(guid, protocol='rtsp')

    expected_keys = ['respType', 'channelIndex', 'guid', 'stream', 'potocol',
                     'resourceUris']

    assert set(expected_keys).issubset(response.keys())
    assert response['guid'] == guid
