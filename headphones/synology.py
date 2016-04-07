#  This file is part of Headphones.
#
#  Headphones is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Headphones is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Headphones.  If not, see <http://www.gnu.org/licenses/>

import time
import json
import base64
import urlparse

from headphones import logger, request
import headphones

# This is a basic script to add torrents downloads to Synology DownloadStation, it can probably be improved
# The Synology DownloadStation API guide is available at http://global.download.synology.com/download/Document/DeveloperGuide/Synology_Download_Station_Web_API.pdf

def torrentAction(method, arguments):
    global _session_id
    host = headphones.CONFIG.SYNOLOGY_HOST
    username = headphones.CONFIG.SYNOLOGY_USERNAME
    password = headphones.CONFIG.SYNOLOGY_PASSWORD

    if not host.startswith('http'):
        host = 'http://' + host

    if host.endswith('/'):
        host = host[:-1]

    parts = list(urlparse.urlparse(host))

    if not parts[0] in ("http", "https"):
        parts[0] = "http"

    if not parts[2].endswith("/task.cgi"):
        parts[2] += "/webapi/DownloadStation/task.cgi"

    data = {'method': method, 'arguments': arguments}
