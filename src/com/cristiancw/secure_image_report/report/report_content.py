from openpyxl.styles import Font

from com.cristiancw.secure_image_report.report.report_content_line import ReportContentLine


class ReportContent:
    """
    Contains the values and structure of the report.
    """

    def __init__(self):
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
            'C': 15,
            'D': 20,
            'E': 18,
            'F': 15,
            'G': 12,
            'H': 45,
            'I': 200,
            'J': 75
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
            'Image Scanned': [item.image_were_scanned for item in self._lines],  # 'C'
            'Scan Completed At': [item.scan_completed_at for item in self._lines],  # 'D'
            'Issue Name': [item.finding_name for item in self._lines],  # 'E'
            'Issue Severity': [item.finding_severity for item in self._lines],  # 'F'
            'Issue Score': [item.finding_cvss3_score for item in self._lines],  # 'G'
            'Issue Vector': [item.finding_cvss3_vector for item in self._lines],  # 'H'
            'Issue Description': [item.finding_description for item in self._lines],  # 'I'
            'Image Digest': [item.image_digest for item in self._lines],  # 'J'
        }
