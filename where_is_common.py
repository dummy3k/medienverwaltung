#!/usr/bin/env python
from pprint import pprint, pformat
import pkg_resources

#~ pprint(pkg_resources.require("pylons")
package = "medienverwaltungcommon"

#~ pprint(pkg_resources.require("medienverwaltung.common")[0])
print(pkg_resources.require(package)[0].location)
#~ print(type(pkg_resources.require("pylons")[0]))
