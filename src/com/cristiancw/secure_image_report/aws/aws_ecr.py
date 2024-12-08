import json
from datetime import datetime
from typing import Any

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

    def __init__(self, profile: str = None, region: str = None) -> None:
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
    def __update_latest_image(latest_image: dict[str, datetime] = None,
                              image: dict[str, datetime] = None) -> dict[str, datetime]:
        if latest_image is None or image['imagePushedAt'] > latest_image['imagePushedAt']:
            return image
        return latest_image

    @staticmethod
    def __get_arch_by_digest(image_digest: str = None, architectures: dict[{str, str}] = None) -> str | None:
        if architectures:
            for entry in architectures:
                if entry['image_digest'] == image_digest:
                    return entry['arch']
        return None

    def get_image_scan_results(self, repository_list: str = None) -> list[AwsImage]:
        """
        Get the findings of the last image from all the repositories that the profile and the region get access.
        :param repository_list: a list of repos names provided by the user
        :return: a list of scan image results
        """
        if repository_list is None:
            repository_list = self.__get_repositories()

        aws_images_list = []
        for repository in repository_list:
            click.echo(f"Getting the last image from: {repository}")
            latest_image = self.__get_latest_image(repository)
            if latest_image:
                image_tag = latest_image['imageTags'][0]
                pushed_at = latest_image['imagePushedAt']

                image_list_by_arch = self._get_image_by_arch(repository, latest_image)
                for image_by_arch in image_list_by_arch:
                    architecture = image_by_arch['architecture']
                    image_digest = image_by_arch['image']['imageId']['imageDigest'] \
                        if 'imageId' in image_by_arch['image'] else image_by_arch['image']['imageDigest']

                    click.echo(
                        f"  Found tag: {image_tag}, "
                        f"for arch {architecture}, "
                        f"with digest {image_digest}, "
                        f"published on: {pushed_at.strftime("%Y/%m/%d %H:%M:%S")}"
                    )
                    scan_findings = self.__get_scan_findings(repository, image_tag, image_digest, architecture)
                    if scan_findings:
                        aws_images_list.append(scan_findings)
            else:
                click.echo('  No tag found')
        return aws_images_list

    def __get_repositories(self) -> list[str]:
        repositories = []
        describe_repositories = self._ecr_client.get_paginator('describe_repositories')
        for page in describe_repositories.paginate():
            repositories.extend(page['repositories'])
        return [repo['repositoryName'] for repo in repositories]

    def __get_latest_image(self, repository: str = None) -> dict[str, any] | None:
        latest_image = None
        describe_images = self._ecr_client.describe_images(repositoryName=repository)

        for image in describe_images['imageDetails']:
            if 'imageTags' in image:  # remove the '-'
                latest_image = self.__update_latest_image(latest_image, image)

        while 'nextToken' in describe_images:
            describe_images = self._ecr_client.describe_images(repositoryName=repository,
                                                               nextToken=describe_images['nextToken'])
            for image in describe_images['imageDetails']:
                if 'imageTags' in image:  # remove the '-'
                    latest_image = self.__update_latest_image(latest_image, image)

        if latest_image:
            return latest_image

        return None

    def _get_image_by_arch(self, repository: str = None,
                           latest_image: dict[str, any] = None) -> list[dict[str, Any]]:
        image_digest = latest_image['imageDigest'] if 'imageDigest' in latest_image else None
        image_details = self._ecr_client.batch_get_image(
            repositoryName=repository, imageIds=[{'imageDigest': image_digest}]
        )
        image_manifest_list = json.loads(image_details['images'][0]['imageManifest'])

        image_by_arch = []
        if 'manifests' in image_manifest_list:
            for image_manifest in image_manifest_list['manifests']:
                manifest_digest = image_manifest['digest']
                manifest_architecture = image_manifest['platform']['architecture']
                image = self._ecr_client.batch_get_image(
                    repositoryName=repository, imageIds=[{'imageDigest': manifest_digest}]
                )
                image_by_arch.append({'architecture': manifest_architecture, 'image': image['images'][0]})
        else:  # if it does not the manifest (index) is a regular non-multi arch image
            image_by_arch.append({'architecture': 'amd64', 'image': latest_image})

        return image_by_arch

    def __get_images_and_index(self, repository_name: str = None,
                               registry_id: str = None,
                               image_digest: str = None) -> list[dict] | None:
        describe_images = self._ecr_client.describe_images(registryId=registry_id,
                                                           repositoryName=repository_name,
                                                           imageIds=[{'imageDigest': image_digest}])
        if describe_images:
            describe_images['imageDetails'].sort(key=lambda x: x['imagePushedAt'], reverse=True)  # index first
            return describe_images['imageDetails']
        return None

    def __get_scan_findings(self, repository_name: str = '', tag: str = '', image_digest: str = '',
                            arch: str = '') -> AwsImage | None:
        aws_image = AwsImage()
        aws_image.repository_name = repository_name
        aws_image.image_tag = tag
        aws_image.image_digest = image_digest
        aws_image.arch = arch

        try:
            response = self._ecr_client.describe_image_scan_findings(repositoryName=repository_name,
                                                                     imageId={'imageDigest': image_digest})
            aws_image.status = response['imageScanStatus']['status']
            if aws_image.status in ['COMPLETE', 'ACTIVE'] and 'imageScanCompletedAt' in response['imageScanFindings']:
                aws_image.scan_completed_at = response['imageScanFindings']['imageScanCompletedAt']

                if 'findings' in response['imageScanFindings']:
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
                elif 'enhancedFindings' in response['imageScanFindings']:
                    for finding in response['imageScanFindings']['enhancedFindings']:
                        aws_scan_result = AwsScanResult()
                        aws_scan_result.name = finding['title']  # okay
                        aws_scan_result.description = finding['description']  # okay
                        aws_scan_result.severity = finding['severity']  # okay
                        aws_scan_result.cvss3_score = finding['score']  # okay
                        aws_scan_result.cvss3_vector = finding['scoreDetails']['cvss'][
                            'scoringVector'] if 'scoreDetails' in finding else ''  # okay
                        if 'remediation' in finding:
                            if len(finding['remediation']) == 1:
                                aws_scan_result.remediation = finding['remediation']['recommendation']['text']
                            else:
                                aws_scan_result.remediation = ''
                                # for remediation in finding['remediation']:
                                #     aws_scan_result.remediation += remediation['recommendation'] + '\n'
                        aws_scan_result.fix_available = finding['fixAvailable']
                        aws_scan_result.exploit_available = finding['exploitAvailable']
                        aws_image.add_finding(aws_scan_result)
                else:
                    click.secho("  Unsupported scan type", err=True, fg='red')
            else:
                click.secho("  Image vulnerability scan was found but no findings", fg='yellow')
                return None

            click.secho("  Image vulnerability scan was found", fg='green')
            return aws_image
        except ClientError as e:
            click.secho("  Image vulnerability scan was NOT found", err=True, fg='red')
        return None
