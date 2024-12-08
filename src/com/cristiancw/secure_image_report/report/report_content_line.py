class ReportContentLine:
    """
    Contains each line for the reports.
    """

    def __init__(self, repository_name: str = '', image_tag: str = '', image_were_scanned: str = '',
                 image_digest: str = '', arch: str = '', status: str = '', scan_completed_at: str = '',
                 finding_name: str = '', finding_description: str = '', finding_uri: str = '',
                 finding_severity: str = '', finding_cvss3_score: str = '', finding_cvss3_vector: str = '',
                 finding_remediation: str = '', finding_fix_available: str = '',
                 finding_exploit_available: str = '') -> None:
        self._repository_name = repository_name
        self._image_tag = image_tag
        self._image_were_scanned = image_were_scanned
        self._image_digest = image_digest
        self._arch = arch
        self._status = status
        self._scan_completed_at = scan_completed_at
        self._finding_name = finding_name
        self._finding_description = finding_description
        self._finding_uri = finding_uri
        self._finding_severity = finding_severity
        self._finding_cvss3_score = finding_cvss3_score
        self._finding_cvss3_vector = finding_cvss3_vector
        self._finding_remediation = finding_remediation
        self._finding_fix_available = finding_fix_available
        self._finding_exploit_available = finding_exploit_available

    @property
    def repository_name(self):
        return self._repository_name

    @repository_name.setter
    def repository_name(self, value):
        self._repository_name = value

    @property
    def image_tag(self):
        return self._image_tag

    @image_tag.setter
    def image_tag(self, value):
        self._image_tag = value

    @property
    def image_were_scanned(self):
        return self._image_were_scanned

    @image_were_scanned.setter
    def image_were_scanned(self, value):
        self._image_were_scanned = value

    @property
    def image_digest(self):
        return self._image_digest

    @image_digest.setter
    def image_digest(self, value):
        self._image_digest = value

    @property
    def arch(self):
        return self._arch

    @arch.setter
    def arch(self, value):
        self._arch = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def scan_completed_at(self):
        return self._scan_completed_at

    @scan_completed_at.setter
    def scan_completed_at(self, value):
        self._scan_completed_at = value

    @property
    def finding_name(self):
        return self._finding_name

    @finding_name.setter
    def finding_name(self, value):
        self._finding_name = value

    @property
    def finding_description(self):
        return self._finding_description

    @finding_description.setter
    def finding_description(self, value):
        self._finding_description = value

    @property
    def finding_uri(self):
        return self._finding_uri

    @finding_uri.setter
    def finding_uri(self, value):
        self._finding_uri = value

    @property
    def finding_severity(self):
        return self._finding_severity

    @finding_severity.setter
    def finding_severity(self, value):
        self._finding_severity = value

    @property
    def finding_cvss3_score(self):
        return self._finding_cvss3_score

    @finding_cvss3_score.setter
    def finding_cvss3_score(self, value):
        self._finding_cvss3_score = value

    @property
    def finding_cvss3_vector(self):
        return self._finding_cvss3_vector

    @finding_cvss3_vector.setter
    def finding_cvss3_vector(self, value):
        self._finding_cvss3_vector = value

    @property
    def finding_remediation(self):
        return self._finding_remediation

    @finding_remediation.setter
    def finding_remediation(self, value):
        self._finding_remediation = value

    @property
    def finding_fix_available(self):
        return self._finding_fix_available

    @finding_fix_available.setter
    def finding_fix_available(self, value):
        self._finding_fix_available = value

    @property
    def finding_exploit_available(self):
        return self._finding_exploit_available

    @finding_exploit_available.setter
    def finding_exploit_available(self, value):
        self._finding_exploit_available = value

    def __str__(self):
        return (
            f"Name: {self.repository_name}, "
            f"Tag: {self.image_tag}, "
            f"Severity: {self._finding_severity}, "
            f"Cvss3 score: {self._finding_cvss3_score}")
