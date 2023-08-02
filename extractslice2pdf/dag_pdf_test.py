from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from datetime import timedelta, datetime
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from extractslice2pdf.ExtractSlice2PdfOperator import ExtractSlice2PdfOperator
from kaapana.operators.Pdf2DcmOperator import Pdf2DcmOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator

log = LoggingMixin().log

ui_forms = {
    "workflow_form": {
        "type": "object",
        "properties": {
            "single_execution": {
                "title": "single execution",
                "description": "Should each series be processed separately?",
                "type": "boolean",
                "default": True,
                "readOnly": False,
            }
        }
    }
}

args = {
    'ui_visible': True,
    'ui_forms': ui_forms,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 0,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    dag_id='pdftest',
    default_args=args,
    schedule_interval=None
    )


get_input = LocalGetInputDataOperator(dag=dag)
T12nii = DcmConverterOperator(dag=dag, input_operator=get_input, output_format='nii.gz')
extract_pdf_slice = ExtractSlice2PdfOperator(dag=dag,input_operator=T12nii,task_id="slice_extract_as_pdf")

pdf2dcm = Pdf2DcmOperator(
    dag=dag,
    input_operator=extract_pdf_slice,
    dicom_operator=get_input,
    pdf_title=f"PDF Test {datetime.now().strftime('%d.%m.%Y %H:%M')}",
    delete_input_on_success=False
)

send_pdf = DcmSendOperator(
    dag=dag,
    input_operator=pdf2dcm,
    task_id="dcm_send_pdf"
)

put_pdf_report_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[extract_pdf_slice], file_white_tuples=('.pdf'),task_id="put_pdf_report_to_minio")

clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

get_input >> T12nii >> extract_pdf_slice >> pdf2dcm >> send_pdf >> clean
extract_pdf_slice >> put_pdf_report_to_minio >> clean


