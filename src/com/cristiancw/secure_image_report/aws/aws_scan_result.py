class AwsScanResult:
    """
    Contains the findings of the image scan.
    """

    def __init__(self, name: str = '', description: str = '', uri: str = '', severity: str = '',
                 cvss3_score: float = '', cvss3_vector: str = '', remediation: str = '', fix_available: str = '',
                 exploit_available: str = '', ) -> None:
        self._name = name
        self._description = description
        self._uri = uri
        self._severity = severity
        self._cvss3_score = cvss3_score
        self._cvss3_vector = cvss3_vector
        self._remediation = remediation
        self._fix_available = fix_available
        self._exploit_available = exploit_available

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def uri(self) -> str:
        return self._uri

    @uri.setter
    def uri(self, value: str) -> None:
        self._uri = value

    @property
    def severity(self) -> str:
        return self._severity

    @severity.setter
    def severity(self, value: str) -> None:
        self._severity = value

    @property
    def cvss3_score(self) -> float:
        return self._cvss3_score

    @cvss3_score.setter
    def cvss3_score(self, value: float) -> None:
        if isinstance(value, float):
            self._cvss3_score = value
        else:
            raise ValueError("The field 'cvss3_score' must be a float")

    @property
    def cvss3_vector(self) -> str:
        return self._cvss3_vector

    @cvss3_vector.setter
    def cvss3_vector(self, value: str) -> None:
        self._cvss3_vector = value

    @property
    def remediation(self) -> str:
        return self._remediation

    @remediation.setter
    def remediation(self, value: str) -> None:
        self._remediation = value

    @property
    def fix_available(self) -> str:
        return self._fix_available

    @fix_available.setter
    def fix_available(self, value: str) -> None:
        self._fix_available = value

    @property
    def exploit_available(self) -> str:
        return self._exploit_available

    @exploit_available.setter
    def exploit_available(self, value: str) -> None:
        self._exploit_available = value
