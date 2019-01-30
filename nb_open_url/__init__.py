import os
from notebook.utils import url_path_join, url_escape
from notebook.base.handlers import IPythonHandler
from notebook.notebook.handlers import get_custom_frontend_exporters

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def _jupyter_server_extension_paths():
    return [{"module": "nb_open_url"}]


def _jupyter_nbextension_paths():
    return [{
        "section": "tree",
        "src": "static",
        "dest": "nb_open_url",
        "require": "nb_open_url/index"
    }]


class OpenExternalHandler(IPythonHandler):
    def get(self, url):
        filename = url.split("/")[-1]
        name,_ = os.path.splitext(filename)
        urlretrieve(url, filename)
        url = url_path_join(self.base_url, "notebooks", url_escape(filename))
        self.log.info("Saved notebook to %s, redirecting to %s" % (filename, url))
        self.redirect(url)


def load_jupyter_server_extension(nb_app):
    host_pattern = ".*$"
    base_url = nb_app.web_app.settings["base_url"]
    nb_app.web_app.add_handlers(host_pattern, [
        (url_path_join(base_url, r"/fromurl/(.+)"), OpenExternalHandler)
    ])
