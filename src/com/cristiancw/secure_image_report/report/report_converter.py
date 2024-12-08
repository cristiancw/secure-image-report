import numpy

from com.cristiancw.secure_image_report.aws.aws_image import AwsImage
from com.cristiancw.secure_image_report.report.report_content import ReportContent
from com.cristiancw.secure_image_report.report.report_content_line import ReportContentLine


class ReportConverter:
    """
    Converts the aws object into an object that can be listed in a xls report.
    """

    @staticmethod
    def convert(aws_image_list: list[AwsImage] = ()) -> ReportContent:
        """
        Convert the AwsImage objects in the ReportContent.
        :param aws_image_list: with AwsImage objects
        :return: a list with ReportContent objects
        """
        content = ReportContent()
        for image in aws_image_list:
            is_scanned = False
            scan_completed_at = numpy.nan
            if image.image_digest:
                is_scanned = True
                scan_completed_at = image.scan_completed_at.strftime("%Y/%m/%d %H:%M:%S")

            if not image.findings:
                line = ReportContentLine()
                line.repository_name = image.repository_name
                line.image_tag = image.image_tag
                line.arch = image.arch
                line.status = image.status
                line.image_were_scanned = is_scanned
                line.image_digest = image.image_digest
                line.scan_completed_at = scan_completed_at
                line.finding_name = numpy.nan
                line.finding_description = numpy.nan
                line.finding_uri = numpy.nan
                line.finding_severity = numpy.nan
                line.finding_cvss3_score = numpy.nan
                line.finding_cvss3_vector = numpy.nan
                line.finding_remediation = numpy.nan
                line.finding_fix_available = numpy.nan
                line.finding_exploit_available = numpy.nan
                content.add_line(line)
            else:
                for finding in image.findings:
                    line = ReportContentLine()
                    line.repository_name = image.repository_name
                    line.image_tag = image.image_tag
                    line.arch = image.arch
                    line.status = image.status
                    line.image_were_scanned = is_scanned
                    line.image_digest = image.image_digest
                    line.scan_completed_at = scan_completed_at
                    line.finding_name = finding.name
                    line.finding_description = finding.description
                    line.finding_uri = finding.uri
                    line.finding_severity = finding.severity
                    line.finding_cvss3_score = finding.cvss3_score
                    line.finding_cvss3_vector = finding.cvss3_vector
                    line.finding_remediation = finding.remediation
                    line.finding_fix_available = finding.fix_available
                    line.finding_exploit_available = finding.exploit_available
                    content.add_line(line)

        return content
