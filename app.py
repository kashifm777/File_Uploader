import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import docx2txt
from PIL import Image 
from PyPDF2 import PdfFileReader
import pdfplumber

def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

def read_pdf2(file):
	with pdfplumber.open(file) as pdf:
		page = pdf.pages[0]

	return page.extract_text()

@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img 

def main():
	st.title("File Upload")

	menu = ["Home","Dataset","DocumentFiles"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
		if image_file is not None:
			file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
			st.write(file_details)

			img = load_image(image_file)
			st.image(img,width=250,height=250)

	elif choice == "Dataset":
		st.subheader("Dataset")
		data_file = st.file_uploader("Upload CSV",type=['csv'])
		if st.button("Process"):
			if data_file is not None:
				file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
				st.write(file_details)

				df = pd.read_csv(data_file)
				st.dataframe(df)

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")
		docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
		if st.button("Process"):
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
				st.write(file_details)
				
				if docx_file.type == "text/plain":
					st.text(str(docx_file.read(),"utf-8"))
					raw_text = str(docx_file.read(),"utf-8")
					
					st.write(raw_text)
				elif docx_file.type == "application/pdf":
					try:
						with pdfplumber.open(docx_file) as pdf:
							page = pdf.pages[0]
							st.write(page.extract_text())
					except:
						st.write("None")
					    
					
				elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
					raw_text = docx2txt.process(docx_file)
					st.write(raw_text)

hide_st_style = """
    <style>
        MainMenu {visibility: hiden;}
        footer {visibility: hidden; }
        header {visibility: hidden; }
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

if __name__ == '__main__':
	main()