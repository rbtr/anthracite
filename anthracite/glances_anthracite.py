import json
import os
from mcstatus import MinecraftServer
from glances.logger import logger
from glances.amps.glances_amp import GlancesAmp


class Amp(GlancesAmp):
    """Glances' Minecraft AMP."""

    NAME = 'Anthracite'
    VERSION = '1.0'
    DESCRIPTION = 'Get Minecraft Server status'
    AUTHOR = 'rbtr'

    def update(self, _):
        """Update the AMP"""
        # Get the minecraft server(s) status
        wd = os.path.dirname(os.path.realpath(__file__))
        logger.debug('{0}: Reading mc servers.cfg in directory {1}'.format(self.NAME, wd))
        with open(wd + '/servers.cfg') as cfg_file:
            cfg = json.load(cfg_file)

        default_port = cfg["default"]["port"]
        servers_arr = cfg["servers"]

        result = ''
        for server in servers_arr:
            name = server["name"]
            addr = server["address"]
            port = server["port"]

            if port == "default" or port == "":
                port = default_port

            try:
                status = MinecraftServer(addr, port).status()
                result += "{0} is up with {1} players online [ping {2}, version {3}]\n".format(name, status.players.online, status.latency, status.version.name)
            except:
                result += "{0} is DOWN!\n".format(name)
            self.set_result(result)
            return self.result()