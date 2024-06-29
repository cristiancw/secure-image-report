from datetime import datetime
from typing import Dict, Optional

import boto3
import click
import numpy
from botocore.config import Config
from botocore.exceptions import ClientError

from com.cristiancw.secure_image_report.aws.aws_image import AwsImage
from com.cristiancw.secure_image_report.aws.aws_scan_result import AwsScanResult


class AwsEcr:
    """
    Class that accesses the AWS screen to list all repositories in a
    region and get the result of the most recent scan of the image.
    """

    def __init__(self, profile: str = '', region: str = '') -> None:
        """
        Main constructor.
        :param profile: to use the aws profile
        :param region: to use the aws region
        """
        aws_config = Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            },
            connect_timeout=5,
            read_timeout=60
        )

        session = boto3.Session(
            profile_name=profile,
            region_name=region)

        self._ecr_client = session.client('ecr', config=aws_config)

    @staticmethod
    def __get_attribute(attribute_name: str = '', attributes: list = ()) -> str:
        for attr in attributes:
            if attr['key'] == attribute_name:
                return attr['value']
        return ''

    @staticmethod
    def __update_latest_image(latest_image: Optional[Dict[str, datetime]], image: Dict[str, datetime]) -> (
            Dict)[str, datetime]:
        if latest_image is None or image['imagePushedAt'] > latest_image['imagePushedAt']:
            return image
        return latest_image

    def get_image_scan_results(self) -> list[AwsImage]:
        """
        Get the findings of the last image from all the repositories that the profile and the region get access.
        :return: a list of scan image results
        """
        repositories = self.__get_repositories()

        repositories = ["tasy/tasyemr", "tws/patient-service"]

        aws_images = []
        for repository in repositories:
            click.echo(f"Getting the last image from: {repository}")
            tag, pushed_at = self.__get_latest_image(repository)
            if tag and pushed_at:
                click.echo(f"  Found tag: {tag}, published on: {pushed_at.strftime("%Y/%m/%d %H:%M:%S")}")
                scan_findings = self.__get_scan_findings(repository, tag)
                aws_images.append(scan_findings)
            else:
                click.echo('  No tag found')
        return aws_images

    def __get_repositories(self) -> list[str]:
        response = self._ecr_client.describe_repositories()
        return [repo['repositoryName'] for repo in response['repositories']]

    def __get_latest_image(self, repository_name: str = '') -> [str, datetime]:
        latest_image = None

        describe_images = self._ecr_client.describe_images(repositoryName=repository_name)
        for image in describe_images['imageDetails']:
            latest_image = self.__update_latest_image(latest_image, image)

        while 'nextToken' in describe_images:
            describe_images = self._ecr_client.describe_images(repositoryName=repository_name,
                                                               nextToken=describe_images['nextToken'])
            for image in describe_images['imageDetails']:
                latest_image = self.__update_latest_image(latest_image, image)

        if latest_image:
            tag = latest_image['imageTags'] if 'imageTags' in latest_image else None
            pushed_at = latest_image['imagePushedAt']
            return tag, pushed_at

        return None, None

    def __get_scan_findings(self, repository_name: str = '', tag: str = '') -> AwsImage:
        aws_image = AwsImage()
        aws_image.repository_name = repository_name
        aws_image.image_tag = tag

        try:
            response = self._ecr_client.describe_image_scan_findings(repositoryName=repository_name,
                                                                     imageId={'imageTag': tag})
            aws_image.image_digest = response['imageId']['imageDigest']
            aws_image.status = response['imageScanStatus']['status']
            aws_image.scan_completed_at = response['imageScanFindings']['imageScanCompletedAt']

            for finding in response['imageScanFindings']['findings']:
                aws_scan_result = AwsScanResult()
                aws_scan_result.name = finding['name']
                aws_scan_result.description = finding['description']
                aws_scan_result.uri = finding['uri']
                aws_scan_result.severity = finding['severity']
                cvss3_score = AwsEcr.__get_attribute('CVSS3_SCORE', finding['attributes'])
                if cvss3_score:
                    aws_scan_result.cvss3_score = float(cvss3_score)
                else:
                    aws_scan_result.cvss3_score = numpy.nan
                aws_scan_result.cvss3_vector = AwsEcr.__get_attribute('CVSS3_VECTOR', finding['attributes'])
                aws_image.add_finding(aws_scan_result)

            click.secho("  Image vulnerability scan was found", fg='green')
        except ClientError as e:
            click.secho("  Image vulnerability scan was NOT found", err=True, fg='red')

        return aws_image
