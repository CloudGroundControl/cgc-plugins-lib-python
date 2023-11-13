from dataclasses import dataclass
import json
from typing import List, Optional
from cgcpluginlib import IStream, IStreamType


@dataclass(repr=False)
class IStreamBattery(IStream):
    '''
    IStreamBattery is the battery data received from the vehicle.
    '''
    percent: int = 0
    voltage: Optional[int] = None
    current: Optional[int] = None
    cellVoltages: Optional[List[int]] = None
    numberOfDischarges: Optional[int] = None
    fullChargeCapacity: Optional[List[int]] = None
    designCapacity: Optional[int] = None
    temperature: Optional[int] = None

    def __post_init__(self):
        self.iStreamType = IStreamType.BATTERY


def parse_IStreamBattery(file: str):
    '''
    Parse the IStreamBattery file.

    Parameters:
    - file: The IStreamBattery file.
    '''
    with open(file) as f:
        data = json.load(f)

        iStreamType = data.get('iStreamType', None)
        vehicleId = data.get('vehicleId', None)
        channelId = data.get('channelId', None)
        time = data.get('time', None)

        percent = data.get('percent', None)
        voltage = data.get('voltage', None)
        current = data.get('current', None)
        cellVoltages = data.get('cellVoltages', None)
        numberOfDischarges = data.get('numberOfDischarges', None)
        fullChargeCapacity = data.get('fullChargeCapacity', None)
        designCapacity = data.get('designCapacity', None)
        temperature = data.get('temperature', None)

        istream_battery = IStreamBattery(
            iStreamType=iStreamType,
            vehicleId=vehicleId,
            channelId=channelId,
            time=time,
            percent=percent,
            voltage=voltage,
            current=current,
            cellVoltages=cellVoltages,
            numberOfDischarges=numberOfDischarges,
            fullChargeCapacity=fullChargeCapacity,
            designCapacity=designCapacity,
            temperature=temperature
        )

        return istream_battery
