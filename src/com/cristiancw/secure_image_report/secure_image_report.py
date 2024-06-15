import click
from botocore.exceptions import ProfileNotFound, EndpointConnectionError
from importlib_metadata import version

from com.cristiancw.secure_image_report.aws.aws_ecr import AwsEcr
from com.cristiancw.secure_image_report.report.report_converter import ReportConverter
from com.cristiancw.secure_image_report.report.report_generator import ReportGenerator


@click.command()
@click.version_option(version=version("secure-image-report"))
@click.option("--profile", required=True,
              help="To choose the predefined profile in the awscli settings. E.g.: --profile my_aws_profile")
@click.option("--region", required=True, help="To choose the aws region. E.g.: --region sa-east-1")
def main(profile='', region=''):
    """
    It is tool designed to generate reports from vulnerability scan results of ECR images on AWS.
    This tool facilitates the analysis and visualization of security data, enabling a more efficient
    approach to mitigating vulnerabilities in container environments.
    """
    try:
        aws_ecr = AwsEcr(profile=profile, region=region)
        image_scan_results = aws_ecr.get_image_scan_results()

        report_content = ReportConverter.convert(image_scan_results)

        report_generator = ReportGenerator(report_content)
        report_generator.generate()
        report_generator.format()
    except (ProfileNotFound, EndpointConnectionError) as e:
        click.secho(e.args[0], err=True, fg='red')


"""
The beginning.
"""

if __name__ == '__main__':
    main()
