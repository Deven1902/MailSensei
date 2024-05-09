from setuptools import setup, find_packages

setup(
    name='mailsensei',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license='MIT',
    description="""
    MailSensei is a Python package
    that uses the Hugging Face APIs
    and LLMs to summarize and simplify E-mails.,
    """
)
