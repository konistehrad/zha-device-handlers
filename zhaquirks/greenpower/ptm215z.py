from zigpy.zgp import GreenPowerDeviceData, GPDeviceType, GPSecurityKeyType, GPSecurityLevel
from zigpy.zgp.device import GreenPowerDevice
from zigpy.quirks import CustomGreenPowerDevice
from zigpy.zcl.clusters.general import GreenPowerProxy
from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    BUTTON_1_AND_3,
    BUTTON_2_AND_4,
    CLUSTER_ID,
    COMMAND,
    COMMAND_ID,
    COMMAND_NOTIFICATION,
    ENERGY_BAR,
    PARAMS,
    PRESSED,
    RELEASED,
)

# Mid priority; sloppy match but not terrible as we can matching GPD ID
class EnoceanPTM215ZDevice(CustomGreenPowerDevice, priority=5):
    @classmethod
    def match(cls, device: GreenPowerDevice) -> bool:
        # First check simple security and type parameters
        if device.green_power_data.device_id != GPDeviceType.SWITCH_ON_OFF:
            return False
        if device.green_power_data.security_key_type != GPSecurityKeyType.IndividualKey:
            return False
        if device.green_power_data.security_level != GPSecurityLevel.FullFrameCounterAndMIC:
            return False
        # Finally match against GPD ID prefix
        return str(device.green_power_data.gpd_id).startswith("0x017")
    
    def __init__(self, application, ext: GreenPowerDeviceData):
        super().__init__(application, ext)
        self.manufacturer = "EnOcean"
        self.model = "PTM215Z"
    
    device_automation_triggers = {
        (PRESSED, BUTTON_1): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x10}
        },
        (RELEASED, BUTTON_1): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x14}
        },
        (PRESSED, BUTTON_2): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x11}
        },
        (RELEASED, BUTTON_2): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x15}
        },
        (PRESSED, BUTTON_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x13}
        },
        (RELEASED, BUTTON_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x17}
        },
        (PRESSED, BUTTON_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x12}
        },
        (RELEASED, BUTTON_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x16}
        },
        (PRESSED, BUTTON_1_AND_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x64}
        },
        (RELEASED, BUTTON_1_AND_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x65}
        },
        (PRESSED, BUTTON_2_AND_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x62}
        },
        (RELEASED, BUTTON_2_AND_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x63}
        },
        (PRESSED, ENERGY_BAR): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GreenPowerProxy.cluster_id,
            PARAMS: {COMMAND_ID: 0x22}
        },
    }
