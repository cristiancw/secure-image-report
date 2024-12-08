from openpyxl.styles import Font

from com.cristiancw.secure_image_report.report.report_content_line import ReportContentLine


class ReportContent:
    """
    Contains the values and structure of the report.
    """

    def __init__(self) -> None:
        self._lines = list[ReportContentLine]()

    @staticmethod
    def get_column_sizes() -> dict:
        """
        A dict with the size of the cells.
        :return: dict with the size of the cells
        """
        return {
            'A': 30,
            'B': 30,
            'C': 75,
            'D': 15,
            'E': 20,
            'F': 15,
            'G': 15,
            'H': 18,
            'I': 15,
            'J': 12,
            'K': 45,
            'L': 40,
            'M': 20,
            'N': 20,
            'O': 200,
        }

    @staticmethod
    def get_cel_style() -> dict:
        """
        A dict with the style of the severity cells
        :return: dict with the style of the severity cells
        """
        return {
            'CRITICAL': {'font': Font(color='FF0000', bold=True)},
            'HIGH': {'font': Font(color='FF0000')},
            'MEDIUM': {'font': Font(color='E66100')},
            'LOW': {'font': Font(color='F5C211')},
            'INFORMATIONAL': {'font': Font(color='1C71D8')},
            'UNDEFINED': {'font': Font(color='77767B')},
        }

    def get_lines(self):
        return self._lines

    def add_line(self, item):
        self._lines.append(item)

    def get_values(self) -> dict:
        """
        Convert the content lines in a dict to create the report.
        :return: a dict to create the report.
        """
        return {
            'Repository Name': [item.repository_name for item in self._lines],  # 'A'
            'Image Tag': [item.image_tag for item in self._lines],  # 'B'
            'Image Digest': [item.image_digest for item in self._lines],  # 'C'
            'Image Scanned': ['YES' if item.image_were_scanned else 'NO' for item in self._lines],  # 'D'
            'Scan Completed At': [item.scan_completed_at for item in self._lines],  # 'E'
            'Architecture': [item.arch for item in self._lines],  # 'F'
            'Status': [item.status for item in self._lines],  # 'G'
            'Issue Name': [item.finding_name for item in self._lines],  # 'H'
            'Issue Severity': [item.finding_severity for item in self._lines],  # 'I'
            'Issue Score': [item.finding_cvss3_score for item in self._lines],  # 'J'
            'Issue Vector': [item.finding_cvss3_vector for item in self._lines],  # 'K'
            'Remediation': [item.finding_remediation for item in self._lines],  # 'L'
            'Fix Available': [item.finding_fix_available for item in self._lines],  # 'M'
            'Exploit Available': [item.finding_exploit_available for item in self._lines],  # 'N'
            'Issue Description': [item.finding_description for item in self._lines],  # 'O'
        }
