import click
from importlib_metadata import version


"""
The beginning.
"""


@click.group()
@click.version_option(version=version("secure-image-report"))
@click.pass_context
def main(context):
    """
    It is a Python tool designed to generate XLS reports from vulnerability scan results of ECR (Elastic Container Registry) images on AWS.
    This tool facilitates the analysis and visualization of security data, enabling a more efficient approach to mitigating vulnerabilities
    in container environments.
    """
    print("oi")
