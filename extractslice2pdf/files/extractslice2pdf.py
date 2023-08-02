#---
import sys, os
import SimpleITK as sitk
import glob
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

### For local testng
#os.environ["WORKFLOW_DIR"] = "D:/ashish/work/projects/Kaapana/sampledata/dcm2nifti-210519201059552217" #"<your data directory>"
#os.environ["BATCH_NAME"] = "batch"
#os.environ["OPERATOR_IN_DIR"] = "dcm-converter"
#os.environ["OPERATOR_OUT_DIR"] = "output"

def image_to_pdf(image_path, pdf_path):
    try:
        img = Image.open(image_path)
        img.save(pdf_path, "PDF", resolution=100.0, save_all=True)
        print("Image converted to PDF successfully.")
    except Exception as e:
        print(f"Error converting image to PDF: {e}")

def add_image_and_text_to_pdf(pdf_path, image_path, text):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # List to hold the flowable elements
    elements = []

    # Add the image to the PDF
    img = Image(image_path, width=400, height=300)
    elements.append(img)

    # Add the text to the PDF
    p = Paragraph(text, styles["Normal"])
    elements.append(p)

    # Build the PDF with the image and text
    doc.build(elements)
    print("Image and text added to PDF successfully.")

def process_image(i_fname, o_fname):
    reader = sitk.ImageFileReader()
    reader.SetFileName (i_fname)
    image = reader.Execute()

    size = image.GetSize()
    slice = image[:,:,int(size[2]/2)]

    writer = sitk.ImageFileWriter()
    writer.SetFileName ( o_fname )
    writer.Execute ( slice )

#-----
os.makedirs("/output/", exist_ok=True) #create temp folder

batch_folders = [f for f in glob.glob(os.path.join('/', os.environ['WORKFLOW_DIR'], os.environ['BATCH_NAME'], '*'))]

for batch_element_dir in batch_folders:

    element_input_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_IN_DIR'])

    nifti_files = sorted(glob.glob(os.path.join(element_input_dir, "*.nii.gz*"), recursive=True))

    if len(nifti_files) == 0:
        print("No Nifti file found!")
        exit(1)
    else:
        print(("start creation of pdf: %s" % nifti_files))

        i_fname = nifti_files[0]
        o_fname = '/output/slice.png'
        process_image(i_fname,o_fname)

        print('slice extracted and written internally as png at path: ', o_fname)

        text_to_add = str(batch_element_dir) # for testing we add some text: batch_element_dir to pdf

        element_output_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_OUT_DIR'])
        if not os.path.exists(element_output_dir):
            os.makedirs(element_output_dir)

        pdf_file_path = os.path.join(element_output_dir, "{}.pdf".format(os.path.basename(batch_element_dir)))

        add_image_and_text_to_pdf(pdf_file_path,o_fname,text_to_add)
        print('pdf written successfully at path: ', pdf_file_path)

#---------
# i_fname = 'D:\\ashish\\work\\projects\\KaapanaStuff\\data\\brainvis_error\\F2\\2.16.840.1.114362.1.12066432.24920037488.604832326.447.1607\\relabel\\2.16.840.1.114362.1.12066432.24920037488.604832326.447.1607.nii.gz'
# o_fname = 'D:\\ashish\\work\\projects\\KaapanaStuff\\data\\brainvis_error\\F2\\2.16.840.1.114362.1.12066432.24920037488.604832326.447.1607\\relabel\\slice.png'
# pdf_fname = 'D:\\ashish\\work\\projects\\KaapanaStuff\\data\\brainvis_error\\F2\\2.16.840.1.114362.1.12066432.24920037488.604832326.447.1607\\relabel\\slice.pdf'
# text_to_add = 'blah'

# process_image(i_fname,o_fname)
# # image_to_pdf(o_fname,pdf_fname)
# add_image_and_text_to_pdf(pdf_fname,o_fname,text_to_add)