from urllib.request import build_opener

from pyxsdata import __version__

opener = build_opener()
opener.addheaders = [("User-agent", f"xsdata/{__version__}")]
