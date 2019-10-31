import os
import json
from notebook.utils import url_path_join, url_escape
from notebook.base.handlers import IPythonHandler
import shutil
from tornado.web import MissingArgumentError

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def _jupyter_server_extension_paths():
    return [{"module": "nb_open_ipynb"}]


def _jupyter_nbextension_paths():
    return [{
        "section": "tree",
        "src": "static",
        "dest": "nb_open_ipynb",
        "require": "nb_open_ipynb/index"
    }]


def fail(self, stat, msg):
    self.log.error(msg)
    self.set_status(stat)
    self.set_header("Content-Type", "application/json")
    self.finish(json.dumps(dict(message=msg)))


# path will be relative to the directory that the notebook
# server was started on
def redirect(self, name):
    url = url_path_join(self.base_url, "notebooks", url_escape(name))
    self.log.info("Saved notebook to %s, redirecting to %s" % (name, url))
    self.redirect(url)

def makedirs(name, path):
    if path is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, name)
    return name

class OpenFile(IPythonHandler):
    def get(self):
        try:
            file = self.get_argument("file")
        except MissingArgumentError:
            return fail(self, 400, "parameter 'file' is required")
        path = self.get_argument("path", default=None)
        if not os.path.exists(file):
            return fail(self, 400, "file not found: %s" % path)
        name = file.split("/")[-1]

        try:
            name = makedirs(name, path)
        except Exception as e:
            return fail(self, 500, str(e))

        try:
            shutil.copyfile(file, name)
        except Exception as e:
            return fail(self, 500, str(e))

        redirect(self, name)


class OpenURL(IPythonHandler):
    def get(self):
        try:
            url = self.get_argument("url")
        except MissingArgumentError:
            return fail(self, 400, "parameter 'url' is required")
        path = self.get_argument("path", default=None)
        name = url.split("/")[-1]
   
        try:
            name = makedirs(name, path)
        except Exception as e:
            return fail(self, 500, str(e))

        try:
            urlretrieve(url, name)
        except Exception as e:
            return fail(self, 500, str(e))

        redirect(self, name)


def load_jupyter_server_extension(nb_app):
    host_pattern = ".*$"
    base_url = nb_app.web_app.settings["base_url"]
    nb_app.web_app.add_handlers(host_pattern, [
        (url_path_join(base_url, r"/openurl"), OpenURL),
        (url_path_join(base_url, r"/openfile"), OpenFile)
    ])
