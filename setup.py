import setuptools

distname = "nb_open_ipynb"

setuptools.setup(
    name=distname,
    packages=[distname],
    data_files=[
        ("share/jupyter/nbextensions/%s" % distname, 
            ["%s/static/index.js" % distname])
    ]
)
