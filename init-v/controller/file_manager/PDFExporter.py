from model.Session import Session
from controller.init_v_controll_logic.ExportOptions import ExportOptions
import logging

class PDFExporter:

    def export_pdf(self, output_path: str, session: Session, options: ExportOptions):
        """
        method to export graphs from the session.
        :param output_path: string to the output
        :param session: Session object containing the data
        :param options: ExportOptions object containing the parameters for the export.
        """
        # TODO implement
        logging.debug('exported as pdf report')
