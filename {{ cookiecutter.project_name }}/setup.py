from setuptools import setup


with open('{{ cookiecutter.project_name }}/__init__.py') as f:
    info = {}
    for line in f:
        if line.startswith('version'):
            exec(line, info)
            break


setup_info = dict(
    name='{{ cookiecutter.project_name }}',
    version=info['version'],
    author='{{ cookiecutter.author_name }}',
    packages=['{{ cookiecutter.project_name }}']
)

setup(**setup_info)
