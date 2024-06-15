class ReportContentLine:
    """
    Contains each line for the reports.
    """

    def __init__(self, repository_name=None, image_tag=None, image_were_scanned=None, image_digest=None,
                 scan_completed_at=None, finding_name=None, finding_description=None, finding_severity=None,
                 finding_cvss3_score=None, finding_cvss3_vector=None):
        self._repository_name = repository_name
        self._image_tag = image_tag
        self._image_were_scanned = image_were_scanned
        self._image_digest = image_digest
        self._scan_completed_at = scan_completed_at
        self._finding_name = finding_name
        self._finding_description = finding_description
        self._finding_severity = finding_severity
        self._finding_cvss3_score = finding_cvss3_score
        self._finding_cvss3_vector = finding_cvss3_vector

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

    def __str__(self):
        return (
            f"Name: {self.repository_name}, "
            f"Tag: {self.image_tag}, "
            f"Severity: {self._finding_severity}, "
            f"Cvss3 score: {self._finding_cvss3_score}")
