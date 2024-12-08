from datetime import datetime
from typing import List, Optional

from com.cristiancw.secure_image_report.aws.aws_scan_result import AwsScanResult


class AwsImage:
    """
    Contains some details about the image and a list of the scan findings.
    """

    def __init__(self, repository_name: str = '', image_tag: str = '', image_digest: str = '',
                 arch: str = '', status: str = '', scan_completed_at: Optional[datetime] = None) -> None:
        self._repository_name = repository_name
        self._image_tag = image_tag
        self._image_digest = image_digest
        self._arch = arch
        self._status = status
        self._scan_completed_at = scan_completed_at
        self._findings: List[AwsScanResult] = []

    @property
    def repository_name(self) -> str:
        return self._repository_name

    @repository_name.setter
    def repository_name(self, value: str) -> None:
        self._repository_name = value

    @property
    def image_tag(self) -> str:
        return self._image_tag

    @image_tag.setter
    def image_tag(self, value: str) -> None:
        self._image_tag = value

    @property
    def image_digest(self) -> str:
        return self._image_digest

    @image_digest.setter
    def image_digest(self, value: str) -> None:
        self._image_digest = value

    @property
    def arch(self) -> str:
        return self._arch

    @arch.setter
    def arch(self, value: str) -> None:
        self._arch = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    @property
    def scan_completed_at(self) -> datetime:
        return self._scan_completed_at

    @scan_completed_at.setter
    def scan_completed_at(self, value: datetime) -> None:
        if isinstance(value, datetime) or value is None:
            self._scan_completed_at = value
        else:
            raise ValueError("The field 'scan_completed_at' must be a datetime object or None")

    @property
    def findings(self) -> List[AwsScanResult]:
        return self._findings

    def add_finding(self, finding: AwsScanResult) -> None:
        if isinstance(finding, AwsScanResult):
            self._findings.append(finding)
        else:
            raise ValueError("Only instances of class AwsFinding can be added")
