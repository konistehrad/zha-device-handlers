from zigpy.zgp import GreenPowerDeviceData, GPDeviceType, GPSecurityKeyType, GPSecurityLevel
from zigpy.zgp.device import GreenPowerDevice
from zigpy.quirks import CustomGreenPowerDevice
from zigpy.profiles.zgp import GREENPOWER_CLUSTER_ID
from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    CLUSTER_ID,
    COMMAND,
    COMMAND_ID,
    COMMAND_NOTIFICATION,
    PARAMS,
    PRESSED,
)

# Extremely low priority since we can't sniff the gpd id
class TuyaSelfPoweredSwitch(CustomGreenPowerDevice, priority=25):
    @classmethod
    def match(cls, device: GreenPowerDevice) -> bool:
        if device.green_power_data.device_id is not GPDeviceType.SWITCH_ON_OFF:
            return False
        if device.green_power_data.security_level is not GPSecurityLevel.Encrypted:
            return False
        if device.green_power_data.security_key_type is not GPSecurityKeyType.IndividualKey:
            return False

        # This thing has a mutable GPD ID, which is miserable.
        # It is, however, the only device which posts an Encrypted
        # security level, so we can at least use that to our advantage in
        # combination with the device_id
        return True
    
    def __init__(self, application, ext: GreenPowerDeviceData):
        super().__init__(application, ext)
        self.manufacturer = "TuYa"
        self.model = "Self-Powered Switch"
    
    device_automation_triggers = {
        (PRESSED, BUTTON_1): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x20}
        },
        (PRESSED, BUTTON_2): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GREENPOWER_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x21}
        },
    }
    