from zigpy.zgp import GreenPowerDeviceData
from zigpy.zgp.device import GreenPowerDevice
from zigpy.quirks import CustomGreenPowerDevice
import zigpy.profiles.zha
from zigpy.profiles.zgp import GREENPOWER_CLUSTER_ID
from zigpy.zcl.clusters.general import Basic, PowerConfiguration

from zhaquirks import PowerConfigurationCluster
from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    CLUSTER_ID,
    COMMAND,
    COMMAND_ID,
    COMMAND_NOTIFICATION,
    PARAMS,
    PRESSED,
    RELEASED,
)

class SWS200PowerConfiguration(PowerConfigurationCluster):
    """Common use power configuration cluster."""
    MIN_VOLTS = 2.2  # old 2.1
    MAX_VOLTS = 3.0  # old 3.2


# High matching priority because we are given a manufacturer and model ID in the pairing
class PhilipsSWS200(CustomGreenPowerDevice, priority=1):
    @classmethod
    def match(cls, device: GreenPowerDevice) -> bool:
        # behold, we actually have enough data to do something smart!
        return device.green_power_data.manufacturer_id == 0x100b and device.green_power_data.model_id == 0x0103
    
    def __init__(self, application, ext: GreenPowerDeviceData):
        super().__init__(application, ext)
        self.manufacturer = "Philips"
        self.model = "SWS200"
        ep = self.add_endpoint(1)
        ep.status = 1 # XXX: resolve circular imports
        ep.profile_id = zigpy.profiles.zha.PROFILE_ID
        ep.device_type = zigpy.profiles.zha.DeviceType.LEVEL_CONTROL_SWITCH
        
        ep.add_input_cluster(Basic.cluster_id)
        power_cluster = ep.add_input_cluster(PowerConfiguration.cluster_id, SWS200PowerConfiguration(ep, True))
        power_cluster.update_attribute(0x0034, 30) # 3V coin cell rated voltage

    
    device_automation_triggers = {
        (PRESSED, BUTTON_1): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x10}
        },
        (RELEASED, BUTTON_1): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x18}
        },

        (PRESSED, BUTTON_2): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x11}
        },
        (RELEASED, BUTTON_2): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x19}
        },

        (PRESSED, BUTTON_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x12}
        },
        (RELEASED, BUTTON_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x1A}
        },

        (PRESSED, BUTTON_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x22}
        },
        (RELEASED, BUTTON_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x23}
        },
    }
