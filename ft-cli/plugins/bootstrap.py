#!/usr/bin/python -t
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Copyright 2006 Duke University 
# Written by Seth Vidal

"""
Classes for subcommands of the yum command line interface.
"""

from firmwaretools.trace_decorator import decorate, traceLog, getLog
import firmwaretools.plugins as plugins

import ftcommands

plugin_type = (plugins.TYPE_CLI,)
requires_api_version = "1.0"

moduleLog = getLog()

def config_hook(conduit, *args, **kargs):
    conduit.getOptParser().addEarlyParse("--bootstrap")
    conduit.getOptParser().add_option(
        "--bootstrap", help="List the bootstrap inventory", 
        action="store_const", const="bootstrap", dest="mode", default=None)
    conduit.getBase().registerCommand(BootstrapCommand())

class BootstrapCommand(ftcommands.YumCommand):
    decorate(traceLog())
    def getModes(self):
        return ['bootstrap']

    decorate(traceLog())
    def addSubOptions(self, base, mode, cmdline, processedArgs):
        # need to add bootstrap-specific options to optparser
        base.optparser.add_option("-u", "--up2date_mode", action="store_true", dest="comma_separated", default=False, help="Comma-separate values for use with up2date.")
        base.optparser.add_option("-a", "--apt_mode", action="store_true", dest="apt_mode", default=False, help="fixup names so that they are compatible with apt")

    decorate(traceLog())
    def doCommand(self, base, mode, cmdline, processedArgs):
        parse=str
        if base.opts.apt_mode:
            parse = debianCleanName

        out = ""
        for pkg in base.yieldBootstrap():
            if base.opts.comma_separated:
                out = out + ",%s" % parse(pkg.name)
            else:
                moduleLog.info("%s" % parse(pkg.name))
        
        # strip leading comma:
        out = out[1:]
        if out:
            moduleLog.info(out) 

        return [0, "Done"]


# used by bootstrap
decorate(traceLog())
def debianCleanName(s):
    s = s.replace('_', '-')
    s = s.replace('(', '-')
    s = s.replace(')', '')
    s = s.lower()
    return s
