from dataclasses import dataclass
import json
import os
from typing import Optional
from .jsonobject import JsonObject


@dataclass()
class TelemetryFeeds(JsonObject):
    """
    A TelemetryFeeds object represents the telemetry feeds.
    """
    cameraFeedsImageFolders: list[str]
    cameraFeedsVideoFolders: list[str]
    gimbalsFolder: list[str]
    geolocationFolder: Optional[str] = None
    signalStrengthFolder: Optional[str] = None
    batteryFolder: Optional[str] = None


@dataclass()
class Channel(JsonObject):
    """
    A Channel object represents a channel.
    """
    id: str = ""
    jsonFolder: str = ""


@dataclass()
class PluginRequest(JsonObject):
    """
    A PluginRequest object represents the plugin request file.
    """
    telemetryFeeds: list[TelemetryFeeds]
    inputChannels: list[Channel]
    outputChannels: list[Channel]
    id: str = ""
    orgProfileFile: str = ""
    jobParamFile: str = ""
    userProfileFile: str = ""

    def inputChannelFolder(self, idx: int):
        id = str(idx)
        channel = next(
            (channel for channel in self.inputChannels if channel.id == id), None)
        if channel is None:
            raise Exception(f"Input channel {id} not found")
        return channel.jsonFolder

    def outputChannelFolder(self, idx: int):
        id = str(idx)
        channel = next(
            (channel for channel in self.outputChannels if channel.id == id), None)
        if channel is None:
            raise Exception(f"Output channel {id} not found")
        return channel.jsonFolder


def parse_plugin_request(plugin_request_file: str):
    """
    Parse the plugin request file.

    Parameters:
    - plugin_request_file: The plugin request file.
    """
    with open(plugin_request_file) as f:
        data = json.load(f)

        # Convert the data dictionary to TelemetryData objects
        telemetryFeeds = [TelemetryFeeds(**feed_data)
                          for feed_data in data["telemetryFeeds"]]
        inputChannels = [Channel(**channel_data)
                         for channel_data in data["inputChannels"]]
        outputChannels = [Channel(**channel_data)
                          for channel_data in data["outputChannels"]]

        telemetry_data = PluginRequest(
            id=data["id"],
            orgProfileFile=data["orgProfileFile"],
            jobParamFile=data["jobParamFile"],
            userProfileFile=data["userProfileFile"],
            telemetryFeeds=telemetryFeeds,
            inputChannels=inputChannels,
            outputChannels=outputChannels
        )
    return telemetry_data


def initialise_folders(folders: list[str]):
    """
    Check if the folders exist and create them if they do not exist.
    """
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
