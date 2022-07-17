from flask import Flask,flash,request,redirect,send_file,render_template

import re
import os
import io
import math
import json
import nltk
import spacy
import string
import gensim
import sparknlp
import pyinflect
import wordcloud
import unicodedata
import en_core_web_sm
import language_check
import language_tool_python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyspark.sql.functions as F
from os import fdopen, remove
from spacy import displacy
from shutil import move, copymode
from tempfile import mkstemp
from newspaper import Article
from nltk.parse import CoreNLPParser
from pyspark.ml import Pipeline
from nltk.corpus import wordnet
from pyspark.sql import SparkSession
from sparknlp.base import *
from sklearn.metrics import classification_report, accuracy_score
from nltk.stem.porter import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
from tensorflow.keras.utils import get_file
from sklearn.model_selection import train_test_split

try:
    # path = get_file('GoogleNews-vectors-negative300.bin.gz', origin='https://s3.amazonaws.com/dl4j-distribution/' + 'GoogleNews-vectors-negative300.bin.gz')
    # path = get_file('GoogleNews-vectors-negative300.bin.gz', origin='https://github.com/mmihaltz/word2vec-GoogleNews-vectors/blob/master/GoogleNews-vectors-negative300.bin.gz')
    # path = get_file('archive.zip', origin='D:\DATA\Data Science Reasearch\Yahya 2016\AutomaticGenerateQuestion\archive.zip')
    path = "GoogleNews-vectors-negative300.bin"
except:
    print('Error downloading')
    raise
model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
nlp = spacy.load('en_core_web_md')
tool = language_check.LanguageTool('en-US')
tool2 = language_tool_python.LanguageTool('en-US')

listLabel = []
listLabel.append("CC")
listLabel.append("CD")
listLabel.append("DT")
listLabel.append("EX")
listLabel.append("FW")
listLabel.append("IN")
listLabel.append("JJ")
listLabel.append("JJR")
listLabel.append("JJS")
listLabel.append("LS")
listLabel.append("MD")
listLabel.append("NN")
listLabel.append("NNS")
listLabel.append("NNP")
listLabel.append("NNPS")
listLabel.append("PDT")
listLabel.append("POS")
listLabel.append("PRP")
listLabel.append("PRP$")
listLabel.append("RB")
listLabel.append("RBR")
listLabel.append("RBS") 
listLabel.append("RP")
listLabel.append("SYM")
listLabel.append("TO")
listLabel.append("UH")
listLabel.append("VB")
listLabel.append("VBD")
listLabel.append("VBG")
listLabel.append("VBN")
listLabel.append("VBP")
listLabel.append("VBZ")
listLabel.append("WDT")
listLabel.append("WP")
listLabel.append("WP$")
listLabel.append("WRB")

nilaiLabel = []
nilaiLabel.append(1)
nilaiLabel.append(2)
nilaiLabel.append(3)
nilaiLabel.append(4)
nilaiLabel.append(5)
nilaiLabel.append(6)
nilaiLabel.append(7)
nilaiLabel.append(8)
nilaiLabel.append(9)
nilaiLabel.append(10)
nilaiLabel.append(11)
nilaiLabel.append(12)
nilaiLabel.append(13)
nilaiLabel.append(14)
nilaiLabel.append(15)
nilaiLabel.append(16)
nilaiLabel.append(17)
nilaiLabel.append(18)
nilaiLabel.append(19)
nilaiLabel.append(20)
nilaiLabel.append(21)
nilaiLabel.append(22)
nilaiLabel.append(23)
nilaiLabel.append(24)
nilaiLabel.append(25)
nilaiLabel.append(26)
nilaiLabel.append(27)
nilaiLabel.append(28)
nilaiLabel.append(29)
nilaiLabel.append(30)
nilaiLabel.append(31)
nilaiLabel.append(32)
nilaiLabel.append(33)
nilaiLabel.append(34)
nilaiLabel.append(35)
nilaiLabel.append(36)

# Variabel global
eses_tanda = []
eses_awal = []
eses_kalimat = []

gs_kalimat = []
gs_kalimat_awal = []
gs_tipe = []
gs_pertanyaan = []
gs_jawab = []
gs_aturan = []
gs_seqcoarse = []
gs_sctext = []

cp_pertanyaan = []
cp_pertanyaan_tanda = []
cp_kalimat_awal = []
cp_kalimat = []
cp_jawab = []
cp_pronoun = []
cp_seqcoarse = []
cp_sctext = []

kn_pt_b_pertanyaan = []
kn_pt_posttag = []
kn_pt_b_posttag = []
kn_nilai_tag = []
kn_numerik = []

pj_jarak_all = []
pj_cocok_all = []
pj_jarak = []
pj_cocok = []

srt_jarak = []
srt_cocok = []
srt_kalimat_awal = []
srt_kalimat = []
srt_pertanyaan = []
srt_jawab = []

snm_pertanyaan = []
snm_tanda = []

grammar = []

clear_srt_cocok = []
clear_srt_jarak = []
clear_srt_jawab = []
clear_srt_kalimat = []
clear_srt_kalimat_awal = []
clear_srt_pertanyaan = []
clear_snm_pertanyaan = []
clear_snm_tanda = []
clear_grammar = []

hasil_pertanyaan = []
hasil_jawaban = []

app = Flask(__name__)

@app.route('/')
def index():
	isi = []
	pronoun = []
	rTeks = "data/pronoun/pronoun.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		pronoun.append(i.replace("\n", ""))
	file.close
	len_pronoun = 0
	len_pronoun = len(pronoun)

	isi = []
	question = []
	rTeks = "data/question/pertanyaan.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		question.append(i.replace("\n", ""))
	file.close
	len_question = 0
	len_question = len(question)

	len_generate = 0
	isi = []
	article = []
	rTeks = "data/article/status_generate.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article.append(i.replace("\n", ""))
		if (str(i.replace("\n", "")) == "1") :
			len_generate += 1
	file.close
	len_article = 0
	len_article = len(article)

	return render_template(
		"page_ielts/index.html", 
		len_pronoun = len_pronoun, 
		len_question = len_question, 
		len_article = len_article, 
		len_generate = len_generate
		)

@app.route('/home')
def home():
	isi = []
	pronoun = []
	rTeks = "data/pronoun/pronoun.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		pronoun.append(i.replace("\n", ""))
	file.close
	len_pronoun = 0
	len_pronoun = len(pronoun)

	isi = []
	question = []
	rTeks = "data/question/pertanyaan.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		question.append(i.replace("\n", ""))
	file.close
	len_question = 0
	len_question = len(question)

	len_generate = 0
	isi = []
	article = []
	rTeks = "data/article/status_generate.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article.append(i.replace("\n", ""))
		if (str(i.replace("\n", "")) == "1") :
			len_generate += 1
	file.close
	len_article = 0
	len_article = len(article)
	
	return render_template(
		"page_ielts/index.html", 
		len_pronoun = len_pronoun, 
		len_question = len_question, 
		len_article = len_article, 
		len_generate = len_generate
		)

@app.route('/signin')
def page_login():
	return render_template("page_ielts/login.html")

@app.route('/signup')
def page_register():
	return render_template("page_ielts/register.html")

@app.route('/demo')
def page_demo():
	return render_template("page_ielts/demo.html")

@app.route('/cbt')
def page_cbt():
	return render_template("page_ielts/cbt.html")

@app.route('/cbt_test')
def page_cbt_test():
	return render_template("page_ielts/cbt_test.html")

@app.route('/cbt_createtest')
def page_cbt_createtest():
	return render_template("page_ielts/cbt_createtest.html")

@app.route('/test_collection')
def page_test_collection():
	return render_template("page_ielts/test_collection.html")

@app.route('/generate')
def page_generate_index():
	return render_template("page_ielts/generate.html")

@app.route('/pronoun_collection')
def page_pronoun():
	isi = []
	pronoun = []
	rTeks = "data/pronoun/pronoun.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		pronoun.append(i.replace("\n", ""))
	file.close

	len_pronoun = 0
	len_pronoun = len(pronoun)

	return render_template("page_ielts/pronoun_collection.html", len_pronoun = len_pronoun, list_pronoun = pronoun)

@app.route('/pronoun_collection/add', methods=["POST"])
def page_pronoun_add():
	if request.method == 'POST':
		word_pronoun = request.form['example-input2-group2']

		with open("data/pronoun/pronoun.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write(word_pronoun)

		isi = []
		pronoun = []
		rTeks = "data/pronoun/pronoun.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			pronoun.append(i.replace("\n", ""))
		file.close

		len_pronoun = 0
		len_pronoun = len(pronoun)

	return render_template("page_ielts/pronoun_collection.html", len_pronoun = len_pronoun, list_pronoun = pronoun)

@app.route('/pronoun_collection/delete', methods=["POST"])
def page_pronoun_delete():
	if request.method == 'POST':
		id_pronoun = request.form['id_pronoun']

		with open("data/pronoun/pronoun.txt", "r") as f :
			lines = f.readlines()
		with open("data/pronoun/pronoun.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_pronoun)) :
					f.write(line)
				index += 1

		isi = []
		pronoun = []
		rTeks = "data/pronoun/pronoun.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			pronoun.append(i.replace("\n", ""))
		file.close

		len_pronoun = 0
		len_pronoun = len(pronoun)

	return render_template("page_ielts/pronoun_collection.html", len_pronoun = len_pronoun, list_pronoun = pronoun)

@app.route('/question_collection')
def page_question():
	isi = []
	question = []
	rTeks = "data/question/pertanyaan.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		question.append(i.replace("\n", ""))
	file.close

	len_question = 0
	len_question = len(question)

	return render_template("page_ielts/question_collection.html", len_question = len_question, list_question = question)

@app.route('/question_collection/add', methods=["POST"])
def page_question_add():
	if request.method == 'POST':
		sentence = request.form['example-input2-group2']
		numeric = konversi_numerik_koleksi_pertanyaan(sentence)

		with open("data/question/pertanyaan.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write(sentence)

		with open("data/question/numerik_pertanyaan.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write(numeric)

		isi = []
		question = []
		rTeks = "data/question/pertanyaan.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			question.append(i.replace("\n", ""))
		file.close

		len_question = 0
		len_question = len(question)

	return render_template("page_ielts/question_collection.html", len_question = len_question, list_question = question)

@app.route('/question_collection/delete', methods=["POST"])
def page_question_delete():
	if request.method == 'POST':
		id_question = request.form['id_question']

		with open("data/question/pertanyaan.txt", "r") as f :
			lines = f.readlines()
		with open("data/question/pertanyaan.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_question)) :
					f.write(line)
				index += 1

		with open("data/question/numerik_pertanyaan.txt", "r") as f :
			lines = f.readlines()
		with open("data/question/numerik_pertanyaan.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_question)) :
					f.write(line)
				index += 1

		isi = []
		question = []
		rTeks = "data/question/pertanyaan.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			question.append(i.replace("\n", ""))
		file.close

		len_question = 0
		len_question = len(question)

	return render_template("page_ielts/question_collection.html", len_question = len_question, list_question = question)

@app.route('/article')
def page_article():
	isi = []
	article_title = []
	rTeks = "data/article/judul.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article_title.append(i.replace("\n", ""))
	file.close

	isi = []
	article_name = []
	rTeks = "data/article/nama_file.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article_name.append(i.replace("\n", ""))
	file.close

	isi = []
	article_status = []
	rTeks = "data/article/status_generate.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article_status.append(i.replace("\n", ""))
	file.close

	len_article = 0
	len_article = len(article_title)

	return render_template(
		"page_ielts/article.html", 
		len_article = len_article, 
		list_article_title = article_title, 
		list_article_name = article_name, 
		list_article_status = article_status
		)

@app.route('/article/add', methods=["POST"])
def page_article_add():
	if request.method == 'POST':
		metode = request.form['metode']
		titleFile = request.form['titleFile']

		isi = []
		article_index = []
		rTeks = "data/article/index.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_index.append(i.replace("\n", ""))
		file.close

		if (metode == "link") :
			link_article = request.form['link']
			article = Article(link_article)
			article.download()
			article.html
			article.parse()

			nameFile = ""
			nameFile = "text_" + str(int(article_index[len(article_index)-1])+1) + ".txt"
			with open("data/teks_artikel/" + nameFile, 'w') as file:
				file.write(str(article.text))
		elif (metode == "file") :
			file_article = request.files['textFile']
			nameFile = ""
			nameFile = "text_" + str(int(article_index[len(article_index)-1])+1) + ".txt"
			file_article.save(os.path.join("data/teks_artikel/", nameFile))

		with open("data/article/index.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write(str(int(article_index[len(article_index)-1])+1))

		with open("data/article/judul.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write(titleFile.replace("\n", ""))

		with open("data/article/nama_file.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write(nameFile.replace("\n", ""))

		with open("data/article/status_generate.txt", "a+") as file_object :
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
			file_object.write("0")

		isi = []
		article_title = []
		rTeks = "data/article/judul.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_title.append(i.replace("\n", ""))
		file.close

		isi = []
		article_name = []
		rTeks = "data/article/nama_file.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_name.append(i.replace("\n", ""))
		file.close

		isi = []
		article_status = []
		rTeks = "data/article/status_generate.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_status.append(i.replace("\n", ""))
		file.close

		len_article = 0
		len_article = len(article_title)

	return render_template(
		"page_ielts/article.html", 
		len_article = len_article, 
		list_article_title = article_title, 
		list_article_name = article_name, 
		list_article_status = article_status
		)

@app.route('/article/delete', methods=["POST"])
def page_article_delete():
	if request.method == 'POST':
		id_article = request.form['id_article']

		with open("data/article/index.txt", "r") as f :
			lines = f.readlines()
		with open("data/article/index.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_article)) :
					f.write(line)
				index += 1

		with open("data/article/judul.txt", "r") as f :
			lines = f.readlines()
		with open("data/article/judul.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_article)) :
					f.write(line)
				index += 1

		namaFile = ""
		with open("data/article/nama_file.txt", "r") as f :
			lines = f.readlines()
		with open("data/article/nama_file.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_article)) :
					f.write(line)
				else :
					namaFile = line.replace("\n", "")
				index += 1

		with open("data/article/status_generate.txt", "r") as f :
			lines = f.readlines()
		with open("data/article/status_generate.txt", "w") as f :
			index = 0
			for line in lines :
				if (index != int(id_article)) :
					f.write(line)
				index += 1

		if os.path.exists("data/teks_artikel/" + namaFile):
			os.remove("data/teks_artikel/" + namaFile)
		else:
			print("The file does not exist")

		isi = []
		article_title = []
		rTeks = "data/article/judul.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_title.append(i.replace("\n", ""))
		file.close

		isi = []
		article_name = []
		rTeks = "data/article/nama_file.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_name.append(i.replace("\n", ""))
		file.close

		isi = []
		article_status = []
		rTeks = "data/article/status_generate.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_status.append(str(i.replace("\n", "")))
		file.close

		len_article = 0
		len_article = len(article_title)

	return render_template(
		"page_ielts/article.html", 
		len_article = len_article, 
		list_article_title = article_title, 
		list_article_name = article_name, 
		list_article_status = article_status
		)

@app.route('/generate_question')
def page_generate():
	isi = []
	article_title = []
	rTeks = "data/article/judul.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article_title.append(i.replace("\n", ""))
	file.close

	isi = []
	article_name = []
	rTeks = "data/article/nama_file.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article_name.append(i.replace("\n", ""))
	file.close

	isi = []
	article_status = []
	rTeks = "data/article/status_generate.txt"
	file = open(rTeks, "r")
	isi = file.readlines()
	for i in isi :
		article_status.append(str(i.replace("\n", "")))
	file.close

	len_article = 0
	len_article = len(article_title)

	return render_template(
		"page_ielts/generate_question.html", 
		len_article = len_article, 
		list_article_title = article_title, 
		list_article_name = article_name, 
		list_article_status = article_status,
		generate = 0
		)

@app.route('/user_guide')
def page_user_guide():
	return render_template("page_ielts/user_guide.html")

@app.route('/about')
def page_about():
	return render_template("page_ielts/about.html")

def replace(file_path, index):
	fh, abs_path = mkstemp()
	with fdopen(fh,'w') as new_file :
		with open(file_path) as old_file :
			for i, line in enumerate(old_file) :
				if (i == index) :
					new_file.write("1\n")
				else :
					new_file.write(line)
	copymode(file_path, abs_path)
	remove(file_path)
	move(abs_path, file_path)

	return "done"

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = "data\\hasil\\" + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route('/generate_question/process', methods=["POST"])
def page_generate_question_process():
	if request.method == 'POST':
		chooseArticle = request.form['chooseArticle']
		isi = []
		article_name = []
		rTeks = "data/article/nama_file.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		count = 0
		indexArticle = -1
		for i in isi :
			article_name.append(i.replace("\n", ""))
			if (i.replace("\n", "") == chooseArticle) :
				indexArticle = count
			count += 1
		file.close

		vTemp = ""
		vTemp = replace("data/article/status_generate.txt", indexArticle)

		eses_tanda = []
		eses_awal = []
		eses_kalimat = []

		gs_kalimat = []
		gs_kalimat_awal = []
		gs_tipe = []
		gs_pertanyaan = []
		gs_jawab = []
		gs_aturan = []
		gs_seqcoarse = []
		gs_sctext = []

		cp_pertanyaan = []
		cp_pertanyaan_tanda = []
		cp_kalimat_awal = []
		cp_kalimat = []
		cp_jawab = []
		cp_pronoun = []
		cp_seqcoarse = []
		cp_sctext = []

		kn_pt_b_pertanyaan = []
		kn_pt_posttag = []
		kn_pt_b_posttag = []
		kn_nilai_tag = []
		kn_numerik = []

		pj_jarak_all = []
		pj_cocok_all = []
		pj_jarak = []
		pj_cocok = []

		srt_jarak = []
		srt_cocok = []
		srt_kalimat_awal = []
		srt_kalimat = []
		srt_pertanyaan = []
		srt_jawab = []

		snm_pertanyaan = []
		snm_tanda = []

		grammar = []

		clear_srt_cocok = []
		clear_srt_jarak = []
		clear_srt_jawab = []
		clear_srt_kalimat = []
		clear_srt_kalimat_awal = []
		clear_srt_pertanyaan = []
		clear_snm_pertanyaan = []
		clear_snm_tanda = []
		clear_grammar = []

		hasil_pertanyaan = []
		hasil_jawaban = []

		maxQuestion = ""
		chooseArticle = ""

		maxQuestion = request.form['max']
		chooseArticle = request.form['chooseArticle']

		########################################## Baca file artikel
		isi = []
		teks_artikel = ""
		rTeks = "data/teks_artikel/"+chooseArticle
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			teks_artikel += i.replace("\n", "")
		file.close


		########################################## Tokenization
		hasil_token = []
		hasil_token = tokenization(chooseArticle)


		########################################## Konversi ke tree
		hasil_tree = []
		hasil_tree = konversi_tree(hasil_token)


		########################################## Esktraksi kalimat sederhana
		(eses_kalimat, eses_awal, eses_tanda) = eses(hasil_token, hasil_tree)


		########################################## Generate soal
		(gs_pertanyaan, gs_jawab, gs_kalimat, gs_kalimat_awal, gs_tipe, gs_aturan, gs_seqcoarse, gs_sctext) = generate_soal()


		########################################## Clear pronoun
		(cp_pertanyaan, cp_pertanyaan_tanda, cp_kalimat_awal, cp_kalimat, cp_jawab, cp_pronoun, cp_seqcoarse, cp_sctext) = clear_pronoun()


		########################################## Konversi ke tree kalimat soal
		hasil_tree_kalimat_soal = []
		hasil_tree_kalimat_soal = konversi_tree_kalimat_soal(cp_pertanyaan)


		########################################## Konversi ke numerik
		(kn_pt_posttag, kn_pt_b_posttag, kn_nilai_tag, kn_numerik) = konversi_numerik(hasil_tree_kalimat_soal)


		########################################## Penentuan jarak
		(pj_jarak_all, pj_cocok_all, pj_jarak, pj_cocok, srt_jarak, srt_cocok, srt_kalimat_awal, srt_kalimat, srt_pertanyaan, srt_jawab) = penentuan_jarak(cp_pertanyaan, kn_numerik, cp_kalimat_awal, cp_kalimat, cp_jawab)


		########################################## Sinonim
		(snm_pertanyaan, snm_tanda) = sinonim()


		########################################## Grammar
		grammar = fgrammar(snm_pertanyaan)


		########################################## Clear duplicate
		tTxt1 = []
		tTxt2 = []
		tTxt3 = []
		tTxt4 = []
		tTxt5 = []
		tTxt6 = []
		tTxt7 = []
		tTxt8 = []
		tTxt9 = []

		for i in srt_cocok :
			tTxt1.append(i)

		for i in srt_jarak :
			tTxt2.append(i)

		for i in srt_jawab :
			tTxt3.append(i)

		for i in srt_kalimat :
			tTxt4.append(i)

		for i in srt_kalimat_awal :
			tTxt5.append(i)

		for i in srt_pertanyaan :
			tTxt6.append(i)

		for i in snm_pertanyaan :
			tTxt7.append(i)

		for i in snm_tanda :
			tTxt8.append(i)

		for i in grammar :
			tTxt9.append(i)

		(hasil_pertanyaan, hasil_jawaban) = clear_duplicate(tTxt1, tTxt2, tTxt3, tTxt4, tTxt5, tTxt6, tTxt7, tTxt8, tTxt9)

		rTeks = "data/hasil/"+chooseArticle
		file = open(rTeks, "w")

		file.write(teks_artikel.replace("\n", ""))

		file.write("\n\nQuestions 1 – " + str(maxQuestion) + "\n")
		file.write("Choose NO MORE THAN THREE WORDS AND/OR A NUMBER from the text for each answer\n")
		file.write("Write your answers in boxes 1-" + str(maxQuestion) + " on your answer sheet.\n")
		j = 1
		for i in hasil_pertanyaan :
			file.write(str(j) + ". " + i.replace("\n", ""))
			file.write("\n")
			j += 1

		file.write("\nAnswer :\n")
		j = 1
		for i in hasil_jawaban :
			file.write(str(j) + ". " + i.replace("\n", ""))
			file.write("\n")
			j += 1

		file.close

		isi = []
		article_title = []
		rTeks = "data/article/judul.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_title.append(i.replace("\n", ""))
		file.close

		isi = []
		article_status = []
		rTeks = "data/article/status_generate.txt"
		file = open(rTeks, "r")
		isi = file.readlines()
		for i in isi :
			article_status.append(str(i.replace("\n", "")))
		file.close

		len_article = 0
		len_article = len(article_title)
			
	return render_template(
		"page_ielts/generate_question.html",
		link = chooseArticle, 
		article = teks_artikel, 
		max_question = maxQuestion, 
		result_token = hasil_token, 
		result_tree = hasil_tree, 
		result_eses = eses_kalimat, 
		result_pertanyaan = gs_pertanyaan, 
		result_jawaban = gs_jawab, 
		result_cp_pertanyaan = cp_pertanyaan, 
		result_cp_jawaban = cp_jawab, 
		result_tree_kalimat_soal = hasil_tree_kalimat_soal,
		result_numerik = kn_numerik,
		result_penentuan_jarak_jarak = srt_jarak,
		result_penentuan_jarak_pertanyaan = srt_pertanyaan,
		result_sinonim = snm_pertanyaan,
		result_grammar = grammar,
		result_clear_duplicate = hasil_pertanyaan,
		result_final_question = hasil_pertanyaan,
		result_final_answer = hasil_jawaban,
		len_question = len(hasil_pertanyaan),
		len_answer = len(hasil_jawaban),
		len_article = len_article, 
		list_article_title = article_title, 
		list_article_name = article_name, 
		list_article_status = article_status,
		generate = 1
		)

def tokenization(text) :
	isi = []

	rTeks = "data/teks_artikel/"+text
	file = open(rTeks, "r")
	isi = file.readlines()
	file.close

	# isi.append(text)
	# tamp2 = []
	# for i, x in enumerate(isi) :
	# 	doc = nlp(x)
	# 	for sent in doc.sents:
	# 		tamp2.append(sent)

	tamp2 = []
	cek = ""
	for i, x in enumerate(isi) :
		kalimat = ""
		stat = 0
		for y, w in enumerate(x) :
			if (stat == 0 and w.isupper() == True) :
				stat = 1
			if (w != ".") :
				if (stat == 1) :
					kalimat += w
					cek = w
			elif (w == "." and stat == 1) :
				if (cek.isnumeric() and x[y+1].isnumeric()) :
					if (stat == 1) :
						kalimat += w
						cek = w
				else :
					tamp2.append(kalimat)
					kalimat = ""
					stat = 0

	hasil_token = []
	for i in tamp2 :
		tamp3 = ""
		tamp3 = re.sub(r"^\s+|\s+$", "", i)
		tamp3 = tamp3.translate(str.maketrans("","",",[!”#$%’'()-*+/:;<=>?@[\]^_`{|}~]"))
		tamp3 = tamp3.translate(str.maketrans("","",'"'))
		tamp3 = re.sub(r' +', ' ', tamp3)
		hasil_token.append(tamp3)

	hasil_token = []
	for i in tamp2 :
		tamp3 = ""
		tamp3 = str(i)
		tamp3 = tamp3.translate(str.maketrans("","",",[!”#$%’'()-*+/:;<=>?@[\]^_`{|}~]"))
		tamp3 = tamp3.translate(str.maketrans("","",'"'))
		tamp3 = re.sub(r' +', ' ', tamp3)
		hasil_token.append(tamp3)

	return hasil_token

def konversi_tree(hasil_token) :
	parser = CoreNLPParser(url='http://localhost:9000')

	hasil_tree = []
	for index, i in enumerate(hasil_token) :
		temp = str (list(parser.raw_parse(i)))
		temp = temp.replace('Tree(', '(')
		temp2 = temp.translate(str.maketrans("","","[,']"))
		hasil_tree.append(temp2)

	return hasil_tree

def eses(hasil_token, hasil_tree) :
	sentence = []
	sentencetag = []

	"""## GetFile"""
	sentence = hasil_token
	sentencetag = hasil_tree

	"""## Proses"""
	sentenceComplex = []
	sentenceChoose = []
	arrSE = []
	arrAwalSE = []
	arrTandaSE = []
	indsen = []
	for k, i in enumerate(sentencetag) :
		count = 0
		for j in i.split() :
			if (j == "(S") :
				count += 1
		if (count > 1) :
			sentenceComplex.append(i)
			sentenceChoose.append(sentence[k])
			indsen.append(k)
		elif (count == 1) :
			arrSE.append(sentence[k])
			arrAwalSE.append(sentence[k])
			arrTandaSE.append("Sama")

	for index in range(len(sentenceComplex)) :
		arrNP = []
		arrscopeNP = []
		arrurutNP = []
		arrVP = []
		arrscopeVP = []
		arrurutVP = []
		struktur = ""
		depthS = -1
		countkrgS = []
		arrDepth = []
		statS = 0
		urut = 0
		statV = 0
		indV = 0
		lewat = 0
		statVBZ = 0
		for j, i in enumerate(sentenceComplex[index]) :
			countkurung = 0
			struktur = ""
			count = 0
			if (i == "(" and sentenceComplex[index][j+1] == "S" and sentenceComplex[index][j+2] == " ") :
				statS = 1
				depthS += 1
				countkrgS.append(0)
				arrDepth.append(0)
				arrDepth[depthS] += 1
			if (statS == 1) :
				if (i == "(") :
					for m in range(depthS+1) :
						countkrgS[m] += 1
				elif (i == ")") :
					for m in range(depthS+1) :
						countkrgS[m] -= 1
				if (len(countkrgS) == depthS) :
					if (countkrgS[depthS] == 0) :
						depthS -= 1
			if (i == "(" and sentenceComplex[index][j+1] == "N" and sentenceComplex[index][j+2] == "P" and sentenceComplex[index][j+3] == " ") :
				urut += 1
			if (indV == j-1) :
				statV = 0
			if (i == "(" and sentenceComplex[index][j+1] == "V" and sentenceComplex[index][j+2] == "P" and sentenceComplex[index][j+3] == " ") :
				count = j+4
				if (statV == 0 and sentenceComplex[index][count] == "(" and sentenceComplex[index][count+1] == "V" and sentenceComplex[index][count+2] == "B" and sentenceComplex[index][count+3] == "Z" and sentenceComplex[index][count+4] == " ") :
					statV = 1
					statVBZ = 1
				elif (statV == 0 and sentenceComplex[index][count] == "(" and sentenceComplex[index][count+1] == "M" and sentenceComplex[index][count+2] == "D" and sentenceComplex[index][count+3] == " ") :
					statV = 1
					statVBZ = 0
				else :
					statVBZ = 0
				struktur += i+sentenceComplex[index][j+1]+sentenceComplex[index][j+2]
				count = j+3
				countkurung = 1
				urut += 1
				lewat = 0
				if (indV < j) :
					while countkurung != 0 and count < len(sentenceComplex[index]):
						if (sentenceComplex[index][count] == "(") :
							countkurung += 1
						elif (sentenceComplex[index][count] == ")") :
							countkurung -= 1
						if (count < len(sentenceComplex[index])-3) :
							if (sentenceComplex[index][count] == "(" and sentenceComplex[index][count+1] == "S" and sentenceComplex[index][count+2] == "B" and sentenceComplex[index][count+3] == "A" and sentenceComplex[index][count+4] == "R") :
								if (sentenceComplex[index][count+6] == "(" and sentenceComplex[index][count+7] == "S" and sentenceComplex[index][count+10] == "V" and sentenceComplex[index][count+11] == "P") :
									if (sentenceComplex[index][count+14] == "T" and sentenceComplex[index][count+15] == "O") :
										lewat = 0
									else :
										lewat += 1
								elif (sentenceComplex[index][count+6] == "(" and sentenceComplex[index][count+7] == "I" and sentenceComplex[index][count+8] == "N") :
									lewat = 0
								else :
									if (statVBZ == 0) :
										lewat += 1
									else :
										lewat = 0
						if (lewat > 0 and sentenceComplex[index][count] == "(") :
							lewat += 1
						elif (lewat > 0 and sentenceComplex[index][count] == ")") :
							lewat -= 1
						if (lewat == 0) :
							struktur += sentenceComplex[index][count]
						count += 1
					if (statV == 1):
						indV = count
					arrVP.append(struktur)
					struktur = ""
					for m in range(depthS+1) :
						struktur += str(arrDepth[m])
					arrscopeVP.append(struktur)
					arrurutVP.append(urut)

		stat = 0
		countkurung = 0
		depthS = -1
		countkrgS = []
		arrDepth = []
		statS = 0
		urut = 0
		for j, i in enumerate(sentenceComplex[index]) :
			struktur = ""
			count = 0
			if (i == "(" and sentenceComplex[index][j+1] == "V" and sentenceComplex[index][j+2] == "P" and sentenceComplex[index][j+3] == " ") :
				urut += 1
				stat = 1
				countkurung = 1
			if (stat == 1) :
				if (i == "(") :
					countkurung += 1
				elif (i == ")") :
					countkurung -= 1
			if (countkurung == 0) :
				stat = 0

			if (i == "(" and sentenceComplex[index][j+1] == "S" and sentenceComplex[index][j+2] == " ") :
				statS = 1
				depthS += 1
				countkrgS.append(0)
				arrDepth.append(0)
				arrDepth[depthS] += 1
			if (statS == 1) :
				if (i == "(") :
					for m in range(depthS+1) :
						countkrgS[m] += 1
				elif (i == ")") :
					for m in range(depthS+1) :
						countkrgS[m] -= 1
				if (len(countkrgS) == depthS) :
					if (countkrgS[depthS] == 0) :
						depthS -= 1

			if (i == "(" and sentenceComplex[index][j+1] == "N" and sentenceComplex[index][j+2] == "P" and sentenceComplex[index][j+3] == " ") :
				urut += 1

			if (stat == 0) :
				if (i == "(" and sentenceComplex[index][j+1] == "N" and sentenceComplex[index][j+2] == "P" and sentenceComplex[index][j+3] == " ") :
					struktur += i+sentenceComplex[index][j+1]+sentenceComplex[index][j+2]
					count = j+3
					countkurung = 1
					while countkurung != 0 and count < len(sentenceComplex[index]):
						struktur += sentencetag[indsen[index]][count]
						if (sentenceComplex[index][count] == "(") :
							countkurung += 1
						elif (sentenceComplex[index][count] == ")") :
							countkurung -= 1
						count += 1
					arrNP.append(struktur)
					struktur = ""
					for m in range(depthS+1) :
						struktur += str(arrDepth[m])
					arrscopeNP.append(struktur)
					arrurutNP.append(urut)

		indexhapusNP = []
		for j, i in enumerate(arrNP) :
			count = 0
			while count < len(i) :
				if (i[count] == "(" and i[count+1] == "V" and i[count+2] == "P") :
					indexhapusNP.append(i)
					break
				if (i[count] == "(" and i[count+1] == "C" and i[count+2] == "C" and i[count+3] == " " and i[count+4] == "a" and i[count+5] == "n" and i[count+6] == "d") :
					indexhapusNP.append(i)
					break
				count += 1

		indexhapusVP = []
		for j, i in enumerate(arrVP) :
			count = 0
			stat = 0
			countkurung = 0
			struktur = ""
			while count < len(i) :
				if (i[count] == "(" and i[count+1] == "C" and i[count+2] == "C" and i[count+3] == " " and i[count+4] == "a" and i[count+5] == "n" and i[count+6] == "d") :
					indexhapusVP.append(i)
					stat = 0
					break
				if (count == 0 and i[count] == "(" and i[count+1] == "V" and i[count+2] == "P" and i[count+4] == "(" and i[count+5] == "T" and i[count+6] == "O") :
					indexhapusVP.append(i)
					stat = 0
					break
				if (i[count] == "(" and i[count+1] == "V" and i[count+2] == "B" and i[count+3] == "Z") :
					stat = 1
				elif (i[count] == "(" and i[count+1] == "V" and i[count+2] == "B" and i[count+3] == "D") :
					stat = 1
				elif (i[count] == "(" and i[count+1] == "M" and i[count+2] == "D" and i[count+3] == " ") :
					stat = 1
				if (stat == 1 and i[count] == "(" and i[count+1] == "V" and i[count+2] == "P" and i[count+3] == " ") :
					stat = 2
				if (i[count] == "(") :
					countkurung += 1
				elif (i[count] == ")") :
					countkurung -= 1
				if (countkurung != 0 and stat == 2) :
					struktur += i[count]
				count += 1
			if (stat == 2) :
				indexhapusVP.append(struktur)

		if (len(arrVP) > 1) :
			for j, i in enumerate(indexhapusVP) :
				for l, k in enumerate(arrVP) :
					if (i == k) :
						arrVP.pop(l)
						arrscopeVP.pop(l)
						arrurutVP.pop(l)

		for j, i in enumerate(indexhapusNP) :
			for l, k in enumerate(arrNP) :
				if (i == k) :
					arrNP.pop(l)
					arrscopeNP.pop(l)
					arrurutNP.pop(l)

		indexhapusVP = []
		for j, i in enumerate(arrVP) :
			struktur = ""
			struktur = i
			for l, k in enumerate(sentenceChoose[index].split()) :
				struktur = struktur.replace(k, "*")
			count = 0
			for k in struktur :
				if (k == '*') :
					count += 1
			if (count <= 1) :
				indexhapusVP.append(i)

		for j, i in enumerate(indexhapusVP) :
			for l, k in enumerate(arrVP) :
				if (i == k) :
					arrVP.pop(l)
					arrscopeVP.pop(l)
					arrurutVP.pop(l)

		vmax = 0
		for i in arrscopeNP :
			if (len(i) > vmax) :
					vmax = len(i)
		for i in arrscopeVP :
			if (len(i) > vmax) :
					vmax = len(i)
		if (vmax == 1):
			vmax += 1

		for k, i in enumerate(arrscopeNP) :
			if (len(i) < vmax) :
				count = vmax - len(i)
				for j in range(count) :
					arrscopeNP[k] += "0"
		for k, i in enumerate(arrscopeVP) :
			if (len(i) < vmax) :
				count = vmax - len(i)
				for j in range(count) :
					arrscopeVP[k] += "0"

		sentenceElementer = []

		for j, i in enumerate(arrNP) :
			for l, k in enumerate(arrVP) :
				if (arrurutNP[j] < arrurutVP[l]) :
					m = 0
					while m < len(arrscopeNP[j]) :
						if (m == 0 and arrscopeNP[j][m] != arrscopeVP[l][m]) :
							break
						if (m != 0 and arrscopeNP[j][m] == "0") :
							sentenceElementer.append(i+" "+k)
							break
						elif (m != 0 and arrscopeVP[l][m] == "0") :
							sentenceElementer.append(i+" "+k)
							break
						elif (m != 0 and arrscopeNP[j][m] == arrscopeVP[l][m]) :
							sentenceElementer.append(i+" "+k)
							break
						m+=1

		struktur = ""
		for j, i in enumerate(sentenceElementer) :
			struktur = ""
			for l, k in enumerate(i.split()) :
				if (k[0] != "(") :
					struktur += k
			struktur = struktur.replace(")", " ")
			sentenceElementer[j] = re.sub(r' +', ' ', struktur)

		struktur = ""
		for l, k in enumerate(sentenceComplex[index].split()) :
			if (k[0] != "(") :
				struktur += k
		struktur = struktur.replace(")", " ")
		struktur = re.sub(r' +', ' ', struktur)
		if (struktur.split()[0] == "What" or struktur.split()[0] == "what") :
			tamp = ""
			for i in struktur.split() :
				if (tamp != "") :
					tamp += " "
				tamp += i
			sentenceElementer.append(tamp)

		for i in sentenceElementer :
			arrSE.append(i)
			arrAwalSE.append(sentenceComplex[index])
			arrTandaSE.append("Tidak Sama")

	"""## Hasil"""
	for j, i in enumerate(arrAwalSE) :
		struktur = ""
		for l, k in enumerate(i.split()) :
			if (k[0] != "(") :
				struktur += k + " "
		struktur = struktur.replace(")", " ")
		arrAwalSE[j] = re.sub(r' +', ' ', struktur)

	for i in arrSE :
		if (i.split()[0] != "But") :
			eses_kalimat.append(str(i))

	for j, i in enumerate(arrSE) :
		if (i.split()[0] != "But") :
			eses_awal.append(str(arrAwalSE[j]))

	for j, i in enumerate(arrSE) :
		if (i.split()[0] != "But") :
			eses_tanda.append(str(arrTandaSE[j]))

	return (eses_kalimat, eses_awal, eses_tanda)

def generate_soal() :
	arrkalimat = []
	arrkalimatAwal = []
	listAturanKalimat = []
	listKata = []
	listVerbKata = []
	stringKata = ""

	arrTeks = []
	arrTanda = []
	arrAwal = []

	arrTeks = eses_kalimat
	arrTanda = eses_tanda
	arrAwal = eses_awal

	for j, i in enumerate(arrTanda) :
		if (i == "Sama") :
			if (len(arrkalimat) > 0) :
				m = 0
				for l, k in enumerate(arrkalimat) :
					if (k == arrTeks[j]) :
						m = 1
				if (m == 0) :
					arrkalimat.append(arrTeks[j])
					arrkalimatAwal.append(arrTeks[j])
			else :
				arrkalimat.append(arrTeks[j])
				arrkalimatAwal.append(arrTeks[j])
		else :
			count = len(arrAwal[j].split())
			if (count % 2 == 1) :
				count += 1
			count = count/2
			if (len(arrTeks[j].split()) > count) :
				if (len(arrkalimat) > 0) :
					m = 0
					for l, k in enumerate(arrkalimat) :
						if (k == arrTeks[j]) :
							m = 1
					if (m == 0) :
						arrkalimat.append(arrTeks[j])
						arrkalimatAwal.append(arrAwal[j])
				else :
					arrkalimat.append(arrTeks[j])
					arrkalimatAwal.append(arrAwal[j])
			else :
				if (len(arrkalimat) > 0) :
					m = 0
					for l, k in enumerate(arrkalimat) :
						if (k == arrTeks[j]) :
							m = 1
					if (m == 0) :
						arrkalimat.append(arrAwal[j])
						arrkalimatAwal.append(arrAwal[j])
				else :
					arrkalimat.append(arrAwal[j])
					arrkalimatAwal.append(arrAwal[j])

	"""## Proses"""
	hKalimat = []
	hKalimatAwal = []
	hTipeSoal = []
	hPertanyaan = []
	hJawaban = []
	hRangking = []
	hAturan = []
	hSeqcoarse = []
	hSctext = []

	tamp = []
	for i in arrkalimat :
		tamp.append(nlp(i))

	for index in range(len(arrkalimat)) :

		"""# GET SUB, ENT, VERB"""
		subj = ""
		catSubj = ""
		dt = ""
		stat = 0
		count = 0
		for i, token in enumerate(tamp[index]) :
			if (token.dep_ == "det") :
				stat = 1
				count = i + 1
				dt = token.text
			if ((token.dep_ == "nsubj" or token.dep_ == "nsubjpass") and i == count and stat == 1 and token.tag_ == "NN") :
				subj = dt + " " + token.text
				catSubj = "EVENT"
		if (subj == "The country") :
			subj = ""
			catSubj = ""

		entity = ""
		statentity = ""
		dt = ""
		stat = 0
		count = 0
		for i, token in enumerate(tamp[index]) :
			if (token.pos_ == "DET") :
				stat = 1
				count = i + 1
				dt = token.text
			elif (token.pos_ == "NOUN" and i == count and stat == 1) :
				entity = dt + " " + token.text
				if (i < len(arrkalimat[index].split())-3) :
					if (tamp[index][i+1].pos_ == "ADP" and tamp[index][i+2].pos_ == "DET") :
						entity += " " + tamp[index][i+1].text
						entity += " " + tamp[index][i+2].text
						entity += " " + tamp[index][i+3].text

		if (entity == subj) :
			entity = ""

		verb = ""
		for i, token in enumerate(tamp[index]) :
			if (token.pos_ == "VERB") :
				verb = token.text

		"""# NER TAG"""
		text = []
		nertag = []
		if (subj != "") :
			text.append(subj)
			nertag.append(catSubj)

		for ent in tamp[index].ents :
			text.append(ent.text)
			nertag.append(ent.label_)

		for k, j in enumerate(text) :
			dt = ""
			stat = 0
			for i in text[k].split() :
				if (verb != i) :
					if (dt != "" and stat == 0) :
						dt = dt + " " + i
					else :
						dt = i
					if (stat == 1) :
						text.append(dt)
						for token in tamp[index]:
							if (token.text == dt) :
								if (token.pos_ == "PROPN") :
									nertag.append("PERSON")
				else :
					text[k] = dt
					stat = 1
			if (stat == 0) :
				text[k] = dt

		dt = ""
		stat = 0
		indexHapus = []
		for j, i in enumerate(text) :
			stat = 0
			dt = entity.replace(i, '_')
			k = 0
			while stat == 0 and k < len(dt.split()) :
				if (dt.split()[k] == "_") :
					stat = 1
				k += 1
			if (stat == 1) :
				indexHapus.append(j)

		for i in indexHapus :
			text.pop(i)
			nertag.pop(i)

		dt = ""
		tCount = []
		for j, i in enumerate(arrkalimat[index].split()) :
			if (i.isnumeric()) :
				if (len(i) > 4) :
					tCount.append(i)

		for i in tCount :
			j = 0
			for l, k in enumerate(text) :
				if (k == i) :
					if (nertag[l] != "CARDINAL") :
						nertag[l] = "CARDINAL"
						j = 1
			if (j == 0) :
				text.append(i)
				nertag.append("CARDINAL")

		for j, i in enumerate(text) :
			for k, token in enumerate(tamp[index]) :
				if (token.text == i) :
					if (k < len(tamp[index])-1) :
						if (tamp[index][k].pos_ == "PROPN" and tamp[index][k+1].pos_ == "PROPN") :
							text[j] += " " + tamp[index][k+1].text
						if (tamp[index][k].pos_ == "NOUN" and tamp[index][k+1].pos_ == "NOUN") :
							text[j] += " " + tamp[index][k+1].text
		if (entity != "") :
			for k, token in enumerate(tamp[index]) :
				if (token.text == entity.split()[len(entity.split())-1]) :
					if (k < len(tamp[index])-1) :
						if (tamp[index][k].pos_ == "PROPN" and tamp[index][k+1].pos_ == "PROPN") :
							entity += " " + tamp[index][k+1].text
						elif (tamp[index][k].pos_ == "NOUN" and tamp[index][k+1].pos_ == "NOUN") :
							entity += " " + tamp[index][k+1].text

		dt = arrkalimat[index]
		tKalimat = ""
		tCount = []
		for j, i in enumerate(text) :
			for l, k in enumerate(dt.split()) :
				if (i == k and l < len(dt.split())-2) :
					if (dt.split()[l+1] == "or" or dt.split()[l+1] == "and") :
						stat = 0
						tKalimat = k+" "+dt.split()[l+1]+" "
						for n, m in enumerate(text) :
							if (m == dt.split()[l+2]) :
								stat = 1
						if (stat == 1) :
							tCount.append(k)
							tCount.append(dt.split()[l+2])
							tKalimat += dt.split()[l+2]
							text.append(tKalimat)
							nertag.append(nertag[j])

		tempText = []
		tempNertag = []
		for j, i in enumerate(text) :
			l = 0
			for k in tCount :
				if (k == i) :
					l = 1
			if (l == 0) :
				tempText.append(i)
				tempNertag.append(nertag[j])

		text.clear()
		nertag.clear()
		for j, i in enumerate(tempText) :
			text.append(i)
			nertag.append(tempNertag[j])

		for j, i in enumerate(text) :
			if (nertag[j] == "DATE") :
				tKalimat = ""
				m = 0
				dt = ""
				for k in range(len(i.split())) :
					if (dt != "") :
						dt += " "
					dt += "_"
				dt = arrkalimat[index].replace(i, dt)
				for l, k in enumerate(dt.split()) :
					if (k == "_") :
						if (tKalimat != "") :
							tKalimat += " "
						tKalimat += tamp[index][l].pos_
				if (tKalimat == "ADV NUM NOUN") :
					nertag[j] = "CARDINAL"

		coarse = []
		for i, j in enumerate(nertag) :
			if (j == "PERSON") :
				coarse.append("HUMAN")
			elif (j == "PRODUCT" or j == "EVENT" or j == "NORP" or j == "ORG" or j == "WORK_OF_ART" or j == "LAW" or j == "LANGUAGE") :
				coarse.append("ENTITY")
			elif (j == "DATE" or j == "TIME") :
				coarse.append("TIME")
			elif (j == "FAC" or j == "GPE" or j == "LOC") :
				coarse.append("LOCATION")
				if (j == "GPE") :
					for token in tamp[index]:
						if (token.text == text[i]) :
							l = 0
							m = 0
							for k in token.shape_ :
								if (k == "x" or k == "X") :
									l+=1
								elif (k == "d" or k == "D") :
									m+=1
							if (m > l and token.is_alpha == False) :
								coarse[i] = "COUNT"
			elif (j == "PERCENT" or j == "MONEY" or j == "QUANTITY" or j == "ORDINAL" or j == "CARDINAL") :
				coarse.append("COUNT")

		seqcoarse = []
		sctext = []
		terurut = []
		tampTexInd = []
		for i in text :
			terurut.append("-")
		cText = ""
		m = 0
		o = 0
		for i, j in enumerate(terurut) :
			for l, k in enumerate(text) :
				if (len(k) > len(cText)) :
					o = 0
					if (len(tampTexInd) > 0) :
						for n in tampTexInd :
							if (l == n) :
								o = 1
					if (o == 0) :
						cText = k
						m = l
			terurut[i] = cText
			tampTexInd.append(m)
			cText = ""

		dt = arrkalimat[index]
		cText = ""
		if (len(verb) > 0) :
			dt = dt.replace(verb, "#VERB#")
		if (len(entity) > 0) :
			dt = dt.replace(entity, "#ENTITY#")
		for i in terurut :
			cText += "*"
			dt = dt.replace(i, cText)

		for i, j in enumerate(dt.split()) :
			if (j == "#VERB#") :
				seqcoarse.append("VERB")
				sctext.append(verb)
			elif (j == "#ENTITY#") :
				seqcoarse.append("ENTITY")
				sctext.append(entity)
			elif (j[0] == "*") :
				seqcoarse.append(coarse[len(j)-1])
				sctext.append(text[len(j)-1])

		arrTampText = []
		arrTampCoarse = []
		for j, i in enumerate(arrkalimat[index].split()) :
			for l, k in enumerate(sctext) :
				if (k == i and len(k.split()) == 1) :
					arrTampText.append(k)
					arrTampCoarse.append(seqcoarse[l])
				elif (len(k.split()) > 1) :
					if (k.split()[0] == arrkalimat[index].split()[j] and k.split()[1] == arrkalimat[index].split()[j+1]) :
						arrTampText.append(k)
						arrTampCoarse.append(seqcoarse[l])

		seqcoarse.clear()
		sctext.clear()
		for j, i in enumerate(arrTampText) : 
			seqcoarse.append(arrTampCoarse[j])
			sctext.append(i)

		fineclass = []
		for j, i in enumerate(sctext) :
			tNertag = ""
			tTeks = ""
			for l, k in enumerate(text) :
				if (i == k) :
					tNertag = nertag[l]
					tTeks = k
			if (seqcoarse[j] == "VERB") :
				fineclass.append("VERB")
			else :
				if ((tNertag == "GPE" or tTeks == "Indians") and (tTeks.lower() != "islands" and tTeks.lower() != "island")) :
					fineclass.append("COUNTRY")
					seqcoarse[j] = "ENTITY"
				else :
					fineclass.append(tNertag)

		lPOS = []
		lLetak = []
		lIndexLetak = []

		for j, i in enumerate(sctext) :
			dt = ""
			dt = arrkalimat[index].replace(i, "_")
			lLetak.append(dt)
			for l, k in enumerate(dt.split()) :
				if (k == "_") :
					lIndexLetak.append(l)
			l = 0
			m = 0
			n = 0
			tKalimat = ""
			for k, token in enumerate(tamp[index]) :
				if (n < len(dt.split())) :
					if (dt.split()[n] == "_") :
						if (tKalimat != "") :
							tKalimat += " "
						tKalimat += "_"
						m = len(i.split())-1
						n += 1
					elif (m != 0) :
						m -= 1
					else :
						if (tKalimat != "") :
							tKalimat += " "
						tKalimat += token.pos_
						n += 1
			lPOS.append(tKalimat)

		"""# GET TIPE SOAL"""
		rule = ""
		for i in seqcoarse :
			if (i == "HUMAN") :
				rule = rule + "H"
			elif (i == "ENTITY") :
				rule = rule + "E"
			elif (i == "LOCATION") :
				rule = rule + "L"
			elif (i == "TIME") :
				rule = rule + "T"
			elif (i == "COUNT") :
				rule = rule + "C"
		hAturan.append(rule)
		listAturanKalimat.append(rule)

		jenis_soal = ""
		statH = 0
		statE = 0
		statT = 0
		statL = 0
		statC = 0
		for j, i in enumerate(rule) :
			if (i == "H" and statH == 0) :
				if (jenis_soal != "") :
					jenis_soal += " "
				jenis_soal += "Who Whom"
				statH = 1
			elif (i == "E" and statE == 0) :
				if (jenis_soal != "") :
					jenis_soal += " "
				jenis_soal += "What"
				statE = 1
			elif (i == "T" and statT == 0) :
				if (jenis_soal != "") :
					jenis_soal += " "
				jenis_soal += "When"
				statT = 1
			elif (i == "L" and statL == 0) :
				if (jenis_soal != "") :
					jenis_soal += " "
				jenis_soal += "Where"
				statL = 1
			elif (i == "C" and statC == 0) :
				if (jenis_soal != "") :
					jenis_soal += " "
				jenis_soal += "How_many/much"
				statC = 1

		hKalimat.append(arrkalimat[index])
		hKalimatAwal.append(arrkalimatAwal[index])
		hTipeSoal.append(jenis_soal)

		"""# RANGKING"""
		ranking = 0
		for j, i in enumerate(rule) :
			if (i == "H") :
				ranking = ranking + 10
			elif (i == "E") :
				ranking = ranking + 8
			elif (i == "L") :
				ranking = ranking + 6
			elif (i == "T") :
				ranking = ranking + 4
			elif (i == "C") :
				ranking = ranking + 2

		hRangking.append(ranking)

		"""# GENERATE SOAL"""
		soal = []
		jawaban = []

		for i in jenis_soal.split() :
			kalimat = ""
			tampjawaban = ""
			if (i == "What") :
				for l, k in enumerate(seqcoarse) :
					if (k == "ENTITY") :
						kalimat = ""
						tJawaban = ""
						if (lIndexLetak[l] == 0 or lIndexLetak[l] == 1) :
							kalimat = ""
							tJawaban = sctext[l]
							n = 0
							for m in lLetak[l].split() :
								if (m == "_" and n == 0) :
									n = 1
									if (fineclass[l] == "COUNTRY") :
										kalimat += "What country" 
									else :
										kalimat += "What"
								elif (n == 1) :
									kalimat += " "
									kalimat += m
							kalimat += "?"
							soal.append(kalimat)
							jawaban.append(tJawaban)
						elif (lIndexLetak[l] == len(lLetak[l].split())-1) :
							kalimat = ""
							tJawaban = ""
							tJawaban = sctext[l]
							p = 0
							o = -1
							if (lPOS[l].split()[lIndexLetak[l]-1] == "DET") :
								tJawaban = lLetak[l].split()[lIndexLetak[l]-1] + " " + tJawaban
								p = 1
								o = lIndexLetak[l]-1
							for n, m in enumerate(lLetak[l].split()) :
								if (m == "_") :
									if (kalimat != "") :
										kalimat += " "
									if (fineclass[l] == "COUNTRY") :
										kalimat += "what country?"
									else :
										kalimat += "what?"
								else :
									if (o != n) :
										if (kalimat != "") :
											kalimat += " "
										kalimat += m
							soal.append(kalimat)
							jawaban.append(tJawaban)
						else :
							tStatNum = 0
							if (lIndexLetak[l] > 0) :
								if (lPOS[l].split()[lIndexLetak[l]-1] == "NUM") :
									tStatNum = 0
									if (fineclass[l] == "COUNTRY") :
										kalimat = "What country"
									else :
										kalimat = "What"
									if (lPOS[l].split()[lIndexLetak[l]+1] == "AUX" and lPOS[l].split()[lIndexLetak[l]+2] == "ADV") :
										kalimat += " "
										kalimat += lLetak[l].split()[lIndexLetak[l]+1]
										kalimat += " "
										kalimat += lLetak[l].split()[lIndexLetak[l]+2]
										for n, m in enumerate(lLetak[l].split()) :
											if (m != "_" and n != lIndexLetak[l]+1 and n != lIndexLetak[l]+2) :
												kalimat += " "
												kalimat += m
									else :
										if (fineclass[l] == "COUNTRY") :
											kalimat = lLetak[l].replace("_", "what country")
										else :
											kalimat = lLetak[l].replace("_", "what")
									kalimat += "?"
									tJawaban = sctext[l]
									soal.append(kalimat)
									jawaban.append(tJawaban)
								else :
									tStatNum = 1
							else :
								tStatNum = 1

							if (tStatNum == 1) :
								o = 0
								if (lIndexLetak[l]+3 < len(lLetak[l].split())) :
									dt = lPOS[l].split()[lIndexLetak[l]+1] + " " + lPOS[l].split()[lIndexLetak[l]+2] + " " + lPOS[l].split()[lIndexLetak[l]+3]
									if (dt == "ADP ADJ NOUN") :
										o = 1
										p = -1
										if (lPOS[l].split()[lIndexLetak[l]-1] == "ADP") :
											tJawaban = lLetak[l].split()[lIndexLetak[l]-1] + " " + sctext[l]
											p = lIndexLetak[l]-1
										if (fineclass[l] == "COUNTRY") :
											kalimat = "What country is"
										else :
											kalimat = "What is"
										for n, m in enumerate(lLetak[l].split()) :
											if (m != "_" and n != p) :
												kalimat += " "
												kalimat += m
										kalimat += "?"
									elif (dt == "VERB ADP NOUN") :
										dt = lLetak[l].split()[lIndexLetak[l]+1] + " " + lLetak[l].split()[lIndexLetak[l]+2] + " " + lLetak[l].split()[lIndexLetak[l]+3]
										o = 1
										p = -1
										if (lPOS[l].split()[lIndexLetak[l]-1] == "CCONJ") :
											p = lIndexLetak[l]-1
										if (fineclass[l] == "COUNTRY") :
											kalimat = "What country " + dt + " in"
										else :
											kalimat = "What " + dt + " in"
										q = 0
										for n, m in enumerate(lLetak[l].split()) :
											if (m != "_" and n != p and q == 0) :
												kalimat += " "
												kalimat += m
											elif (m == "_") :
												q = len(dt.split())
											elif (q != 0) :
												q -= 1
										kalimat += "?"
										tJawaban = sctext[l]

								if (lIndexLetak[l]+1 < len(lLetak[l].split()) and o == 0) :
									dt = lPOS[l].split()[lIndexLetak[l]-1] + " " + lPOS[l].split()[lIndexLetak[l]+1]
									if (dt == "ADV VERB") :
										o = 1
										tJawaban = sctext[l]
										if (fineclass[l] == "COUNTRY") :
											kalimat = "What country is"
										else :
											kalimat = "What is"
										for n, m in enumerate(lLetak[l].split()) :
											if (m != "_") :
												kalimat += " "
												kalimat += m
										kalimat += "?"

								if (o == 0) :
									if (fineclass[l] == "COUNTRY") :
										kalimat = lLetak[l].replace("_", "what country")
									else :
										kalimat = lLetak[l].replace("_", "what")
									kalimat += "?"
									tJawaban = sctext[l]
								soal.append(kalimat)
								jawaban.append(tJawaban)

			if (i == "When") :
				for l, k in enumerate(seqcoarse) :
					if (k == "TIME") :
						stat = 0
						if (lIndexLetak[l] > 3) :
							if (lPOS[l].split()[lIndexLetak[l]-1] == "ADP" and lPOS[l].split()[lIndexLetak[l]-2] == "NOUN" and lPOS[l].split()[lIndexLetak[l]-3] == "NUM" and lPOS[l].split()[lIndexLetak[l]-4] == "VERB") :
								kalimat = "When"
								tempV = ""
								tempH = ""
								o = 0
								p = 0
								for n, m in enumerate(lPOS[l].split()) :
									if (m == "VERB" and o == 0) :
										tempV = lLetak[l].split()[n]
										o += 1
									elif (o == 1 and m == "NUM" and lPOS[l].split()[n+1] == "NOUN") :
										tempH += lLetak[l].split()[n] + " "
										tempH += lLetak[l].split()[n+1]
										o += 1
									if (p == 0 and m == "_") :
										kalimat += " " + tempH + " " + tempV
										p = 1
									elif (p == 1) :
										kalimat += " "
										kalimat += lLetak[l].split()[n]
								kalimat += "?"
								soal.append(kalimat)
								jawaban.append(sctext[l])
							else :
								stat = 1
						if (stat == 1) :
							kalimat = ""
							count = 0
							for k in rule :
								if (k == "H") :
									count += 1
							tempH = ""
							tempV = ""
							k = 0
							while k < len(seqcoarse) :
								if (seqcoarse[k] == "HUMAN") :
									tempH = sctext[k]
									break
								k += 1
							k = 0
							while k  < len(seqcoarse) :
								if (seqcoarse[k] == "TIME") :
									tempV = sctext[k]
									break
								k += 1
							kalimat += "When"
							for l, k in enumerate(arrkalimat[index].replace(tempV, "_").split()) :
								if (l < len(arrkalimat[index].replace(tempV, "_").split())-1) :
									if (k != "_" and arrkalimat[index].replace(tempV, "_").split()[l+1] != "_") :
										if (kalimat != "") :
											kalimat += " "
										kalimat += k
										if (l+1 == len(arrkalimat[index].replace(tempV, "_").split())-1) :
											kalimat += " "
											kalimat += arrkalimat[index].replace(tempV, "_").split()[l+1]
										if (count > 1) :
											if (k == tempH) :
												kalimat += " did"
							kalimat += "?"
							soal.append(kalimat)
							jawaban.append(tempV)

			if (i == "Where") :
				if (len(rule) == 2) :
					kalimat = ""
					for l, k in enumerate(seqcoarse) :
						if (k == "LOCATION") :
							kalimat += " where"
							tampjawaban = sctext[l]
						else :
							if (kalimat != "") :
								kalimat += " "
							kalimat += sctext[l]
					kalimat += "?"
					soal.append(kalimat)
					jawaban.append(tampjawaban)
				else :
					kalimat = ""
					count = 0
					stat = 0
					for k in rule :
						if (k == "L") :
							count += 1
						if (k == "H") :
							stat += 1
					if (count == 1) :
						if (stat > 1) :
							kalimat = ""
							for n, m in enumerate(arrkalimat[index].split()) :
								q = 0
								for p, o in enumerate(seqcoarse) :
									if (len(sctext[p].split()) == 1) :
										if (sctext[p] == m) :
											if (o == "LOCATION") :
												tempH = sctext[p]
												if (kalimat != "") :
													kalimat += " "
												kalimat += "where"
												q = 1
									else :
										if (sctext[p].split()[0] == m and sctext[p].split()[1] == arrkalimat[index].split()[n+1]) :
											if (o == "LOCATION") :
												tempH = sctext[p]
												if (kalimat != "") :
													kalimat += " "
												kalimat += "where"
												q = 1
								if (q == 0) :
									if (kalimat != "") :
										kalimat += " "
									kalimat += m
							kalimat += "?"
						elif (stat == 1) :
							kalimat += "Where did"
							tempH = ""
							for n, m in enumerate(seqcoarse) :
								if (m == "LOCATION") :
									tempH = sctext[n]
							for m in arrkalimat[index].replace(tempH, "_").split() :
								if (m != "_") :
									if (kalimat != "") :
										kalimat += " "
									kalimat += m
							kalimat += "?"
						else :
							for l, k in enumerate(seqcoarse) :
								if (k == "LOCATION") :
									tampjawaban = sctext[l]
									if (lIndexLetak[l] < 2) :
										if (fineclass[l] == "COUNTRY") :
											kalimat += "Where country" 
										else :
											kalimat += "Where"
										tempH = ""
										for n, m in enumerate(seqcoarse) :
											if (m == "LOCATION") :
												tempH = sctext[n]
										for m in arrkalimat[index].replace(tempH, "_").split() :
											if (m != "_") :
												if (kalimat != "") :
													kalimat += " "
												kalimat += m
										kalimat += "?"
									else :
										kalimat = lLetak[l].replace("_", "where")
										kalimat += "?"
						soal.append(kalimat)
						jawaban.append(tampjawaban)
					else :
						for l, k in enumerate(seqcoarse) :
							kalimat = ""
							tempV = ""
							if (k == "LOCATION") :
								m = 0
								while m < len(arrkalimat[index].split()) :
									if (arrkalimat[index].split()[m] != sctext[l]) :
										if (kalimat != "") :
											kalimat += " "
										kalimat += arrkalimat[index].split()[m]
									else :
										if (kalimat != "") :
											kalimat += " "
										kalimat += "where"
										if (l != 0) :
											break
									m += 1
								kalimat += "?"
								soal.append(kalimat)
								jawaban.append(sctext[l])

			if (i == "Whom") :
				count = 0
				for l, k in enumerate(seqcoarse) :
					kalimat = ""
					if (k == "HUMAN") :
						count += 1
						if (count > 1) :
							for m in arrkalimat[index].split() :
								if (m != sctext[l]) :
									if (kalimat != "") :
										kalimat += " "
									kalimat += m
								else :
									kalimat += " whom"
							kalimat += "?"
							soal.append(kalimat)
							jawaban.append(sctext[l])

			if (i == "Who") :
				tempH = ""
				tampjawaban = ""
				k = 0
				while k < len(seqcoarse) :
					if (seqcoarse[k] == "HUMAN") :
						tempH = sctext[k]
						break
					k += 1
				
				kalimat = "Who"
				tampjawaban = tempH
				for l, k in enumerate(arrkalimat[index].replace(tempH, "_").split()) :
					if (k != "_") :
						if (kalimat != "") :
							kalimat += " "
						kalimat += k
				kalimat += "?"
				soal.append(kalimat)
				jawaban.append(tampjawaban)

			if (i == "How_many/much") :
				for l, k in enumerate(seqcoarse) :
					if (k == "COUNT") :
						kalimat = ""
						tJawaban = ""
						if (fineclass[l] != "ORDINAL") :
							if (lIndexLetak[l] < 4) :
								kalimat = "How many"
								tJawaban = sctext[l]
								o = 0
								for n, m in enumerate(lLetak[l].split()) :
									if (m != "_") :
										if (n == 0 and lPOS[l].split()[n] == "PRON") :
											o += 1
										else :
											kalimat += " "
											kalimat += m
								kalimat += "?"
								soal.append(kalimat)
								jawaban.append(tJawaban)
							elif (lIndexLetak[l] == len(lLetak[l].split())-1) :
								tJawaban = sctext[l]
								o = 0
								if (lLetak[l].split()[lIndexLetak[l]-1] == "to") :
									kalimat = "From"
									o = 1
								for n, m in enumerate(lLetak[l].split()) :
									if (m != "_") :
										if (o == 1 and n == 0 and lPOS[l].split()[n] == "PRON") :
											o += 1
										else :
											if (kalimat != "") :
												kalimat += " "
											kalimat += m
								kalimat += " how many?"
								soal.append(kalimat)
								jawaban.append(tJawaban)
							else :
								tKalimat = ""
								dt = ""
								for m in range(len(sctext[l].split())) :
									if (dt != "") :
										dt += " "
									dt += "_"
								dt = arrkalimat[index].replace(sctext[l], dt)
								for n, m in enumerate(dt.split()) :
									if (m == "_") :
										if (tKalimat != "") :
											tKalimat += " "
										tKalimat += tamp[index][n].pos_
								if (tKalimat == "ADV NUM NOUN") :
									tJawaban = sctext[l]
									kalimat = "In how many " + sctext[l].split()[2]
									for n, m in enumerate(lLetak[l].split()) :
										if (m != "_") :
											kalimat += " "
											kalimat += m
									kalimat += "?"
								else :
									tJawaban = sctext[l]
									for n, m in enumerate(lLetak[l].split()) :
										if (m != "_") :
											if (n < len(lLetak[l].split())-1) :
												if (lLetak[l].split()[n+1] == "_" and (lPOS[l].split()[n] == "ADP" or lPOS[l].split()[n] == "DET")) :
													o = 0
												else :
													if (kalimat != "") :
														kalimat += " "
													kalimat += m
											else :
												if (kalimat != "") :
													kalimat += " "
												kalimat += m
										else :
											kalimat += " how many"
									kalimat += "?"
								soal.append(kalimat)
								jawaban.append(tJawaban)
						else :
							kalimat = "What order"
							tJawaban = ""
							for n, m in enumerate(lLetak[l].split()) :
								if (m != "_") :
									o = 0
									if (n < len(lLetak[l].split())-1) :
										if (lLetak[l].split()[n+1] == "_" and lPOS[l].split()[n] == "DET") :
											tJawaban = m + " " + sctext[l]
											o = 1
									if (n > 0) :
										if (lLetak[l].split()[n-1] == "_" and lPOS[l].split()[n] == "NOUN") :
											if (tJawaban != "") :
												tJawaban += " " + m
											else :
												tJawaban = sctext[l] + " " + m
											o = 1
									if (o == 0) :
										if (kalimat != "") :
											kalimat += " "
										kalimat += m
							kalimat += "?"
							if (tJawaban == "") :
								tJawaban = sctext[l]
							soal.append(kalimat)
							jawaban.append(tJawaban)

		txtSeqcoarse = ""
		txtSctext = ""
		for j, i in enumerate(seqcoarse) :
			if (j != 0) :
				txtSeqcoarse += " "
				txtSctext += " "
			txtSeqcoarse += i + " , "
			txtSctext += sctext[j] + " , "
		hSeqcoarse.append(txtSeqcoarse)
		hSctext.append(txtSctext)

		k = 0
		for j, i in enumerate(soal) :
			if (jawaban[j] != "The country" and jawaban[j] != "") :
				k += 1
				hPertanyaan.append(i)
				hJawaban.append(jawaban[j])
		if (k == 0) :
			hAturan.pop(len(hAturan)-1)
			hRangking.pop(len(hRangking)-1)
			hTipeSoal.pop(len(hTipeSoal)-1)
			hKalimat.pop(len(hKalimat)-1)
			hKalimatAwal.pop(len(hKalimatAwal)-1)
			hSeqcoarse.pop(len(hSeqcoarse)-1)
			hSctext.pop(len(hSctext)-1)

		l = ""
		m = ""
		n = ""
		o = ""
		p = ""
		for i in range(k-1) :
			l = hAturan[len(hAturan)-1]
			m = hRangking[len(hRangking)-1]
			n = hTipeSoal[len(hTipeSoal)-1]
			o = hKalimat[len(hKalimat)-1]
			p = hKalimatAwal[len(hKalimatAwal)-1]
			hAturan.append(l)
			hRangking.append(m)
			hTipeSoal.append(n)
			hKalimat.append(o)
			hKalimatAwal.append(p)
			hSeqcoarse.append(txtSeqcoarse)
			hSctext.append(txtSctext)

	"""## Hasil"""
	for i in hPertanyaan :
		gs_pertanyaan.append(i)
	for i in hJawaban :
		gs_jawab.append(i)
	for i in hKalimat :
		gs_kalimat.append(i)
	for i in hKalimatAwal :
		gs_kalimat_awal.append(i)
	for i in hTipeSoal :
		gs_tipe.append(i)
	for i in hAturan :
		gs_aturan.append(i)
	for i in hSeqcoarse :
		gs_seqcoarse.append(i)
	for i in hSctext :
		gs_sctext.append(i)

	return (gs_pertanyaan, gs_jawab, gs_kalimat, gs_kalimat_awal, gs_tipe, gs_aturan, gs_seqcoarse, gs_sctext)

def clear_pronoun() :
	tpronoun = []
	tkalimatAwal = []
	tkalimat = []
	tpertanyaan = []
	tjawaban = []
	tcoarse = []
	tsctext = []

	rPronoun = "data/pronoun/pronoun.txt"
	file = open(rPronoun, "r")
	isi = file.readlines()
	for j, i in enumerate(isi) :
		tpronoun.append(i)
	file.close

	tkalimatAwal = gs_kalimat_awal
	tkalimat = gs_kalimat
	tpertanyaan = gs_pertanyaan
	tjawaban = gs_jawab
	tcoarse = gs_seqcoarse
	tsctext = gs_sctext

	"""## Proses"""
	nkalimatAwal = []
	nkalimat = []
	npertanyaan = []
	npertanyaanTanda = []
	njawaban = []
	npronoun = []
	ncoarse = []
	nsctext = []

	for j, i in enumerate(tpertanyaan) :
		stat = 0
		temp = i.replace("?", "")
		temp = temp.replace("\n", "")
		hPronoun = ""
		for k in temp.split() :
			m = 0
			while m < len(tpronoun) and stat == 0 :
				string1 = k.lower().rstrip('\n').replace(" ", "")
				string2 = tpronoun[m].lower().rstrip('\n').replace(" ", "")
				if (string1 == string2) :
					hPronoun = string2
					stat += 1
				m += 1
			if (k == "_") :
				stat += 1
		for k in tjawaban[j].split() :
			m = 0
			while m < len(tpronoun) and stat == 0 :
				string1 = k.lower().rstrip('\n').replace(" ", "")
				string2 = tpronoun[m].lower().rstrip('\n').replace(" ", "")
				if (string1 == string2) :
					stat += 1
				m += 1
		if (stat == 0) :
			nkalimatAwal.append(tkalimatAwal[j].replace("\n", ""))
			nkalimat.append(tkalimat[j].replace("\n", ""))
			npertanyaan.append(i.replace("\n", ""))
			npertanyaanTanda.append(i.replace("\n", ""))
			njawaban.append(tjawaban[j].replace("\n", ""))
			ncoarse.append(tcoarse[j].replace("\n", ""))
			nsctext.append(tsctext[j].replace("\n", ""))
			npronoun.append("")
		else :
			npertanyaanTanda.append("")
			npronoun.append(hPronoun)

	"""## Save"""
	cp_pertanyaan = npertanyaan
	cp_pertanyaan_tanda = npertanyaanTanda
	cp_kalimat_awal = nkalimatAwal
	cp_kalimat = nkalimat
	cp_jawab = njawaban
	cp_pronoun = npronoun
	cp_seqcoarse = ncoarse
	cp_sctext = nsctext

	return (cp_pertanyaan, cp_pertanyaan_tanda, cp_kalimat_awal, cp_kalimat, cp_jawab, cp_pronoun, cp_seqcoarse, cp_sctext)

def konversi_tree_kalimat_soal(vcp_pertanyaan) :
	hasil_token = []
	isi = vcp_pertanyaan
	for j, i in enumerate(isi) :
		tamp = ""
		tamp = i.replace("?", "")
		tamp = tamp.replace(",", "")
		tamp = tamp.replace(".", "")
		tamp = tamp.replace('"', "")
		tamp = tamp.replace("'", "")
		tamp = tamp.replace(";", "")
		tamp = tamp.replace(":", "")
		tamp = tamp.replace("(", "")
		tamp = tamp.replace(")", "")
		tamp = tamp.replace("%", "")
		tamp = tamp.replace("$", "")
		tamp = tamp.replace("@", "")
		hasil_token.append(tamp)

	parser = CoreNLPParser(url='http://localhost:9000')
	hasil_tree = []
	for index, i in enumerate(hasil_token) :
		temp = str (list(parser.raw_parse(i)))
		temp = temp.replace('Tree(', '(')
		temp2 = temp.translate(str.maketrans("","","[,']"))
		hasil_tree.append(temp2)

	return hasil_tree

def konversi_numerik(hasil_tree_kalimat_soal) :
	hasil_token = []
	isi = cp_pertanyaan
	tamp = ""
	for i in enumerate(isi) :
		tamp = i
		tamp = " ".join(str(x) for x in tamp)
		tamp = tamp.replace("?", "")
		tamp = tamp.replace(",", "")
		tamp = tamp.replace(".", "")
		tamp = tamp.replace('"', "")
		tamp = tamp.replace("'", "")
		tamp = tamp.replace(";", "")
		tamp = tamp.replace(":", "")
		tamp = tamp.replace("(", "")
		tamp = tamp.replace(")", "")
		tamp = tamp.replace("%", "")
		tamp = tamp.replace("$", "")
		tamp = tamp.replace("@", "")
		hasil_token.append(tamp)

	nTeks = []
	for i in hasil_token :
		nTeks.append(len(i.split())-1)
		kn_postag_b_pertanyaan.append(len(i.split())-1)

	tree = []
	isi = hasil_tree_kalimat_soal
	for i in enumerate(isi) :
		tree.append(i)

	posTag = []
	for j, i in enumerate(tree) :
		temp = " ".join(str(x) for x in i)
		tamp = ""
		for l, k in enumerate(temp.split()) :
			if (l < len(temp.split())-1) :
				if (k[0] == "(" and temp.split()[l+1][0] != "(") :
					if (tamp != "") :
						tamp += " "
					tamp += k.replace("(", "")
		posTag.append(tamp)

	nTag = []
	for i in posTag :
		kn_pt_posttag.append(str(i))
		kn_pt_b_posttag.append(str(len(i.split())))
		nTag.append(len(i.split()))

	"""# Konversi Numerik
	## Proses"""
	isi = kn_pt_posttag
	tamp = []
	tag = []
	for j, i in enumerate(isi) :
		temp = ""
		temp = str(i)
		tamp.append(len(temp.split())-1)
		tag.append(temp)

	tagNilai = []
	nilai = ""
	for i in tag :
		nilai = ""
		for j in i.split() :
			k = 0
			stat = 0
			while k < len(listLabel) and stat == 0 :
				if (j == listLabel[k]) :
					if (nilai != "") :
						nilai += " "
					nilai += str(nilaiLabel[k])
					stat = 1
				k += 1
		tagNilai.append(nilai)
	kn_nilai_tag = tagNilai

	tagNumerik = []
	nilai = ""
	for i in tagNilai :
		nilai = ""
		for j in i.split() :
			a = int(j)
			b = 2.86 * a - 1
			if (nilai != "") :
				nilai += " "
			nilai += str('{:.2f}'.format(b))
		tagNumerik.append(nilai)
	kn_numerik = tagNumerik
	
	return (kn_pt_posttag, kn_pt_b_posttag, kn_nilai_tag, kn_numerik)

def penentuan_jarak(vcp_pertanyaan, vkn_numerik, vcp_kalimat_awal, vcp_kalimat, vcp_jawab) :
	"""## Proses"""
	file = open("data/question/pertanyaan.txt", "r")
	isi = file.readlines()
	datasetPertanyaan = []
	for j, i in enumerate(isi) :
		datasetPertanyaan.append(i)
	file.close

	file = open("data/question/numerik_pertanyaan.txt", "r")
	isi = file.readlines()
	datasetNilaiNumerikTag = []
	for j, i in enumerate(isi) :
		datasetNilaiNumerikTag.append(i)
	file.close

	tempIsi = []
	tempIsi = vcp_pertanyaan
	contohPertanyaan = []
	for j, i in enumerate(tempIsi) :
		contohPertanyaan.append(i)

	tempIsi = []
	tempIsi = vkn_numerik
	contohNilaiNumerikTag = []
	for j, i in enumerate(tempIsi) :
		contohNilaiNumerikTag.append(i)

	listJarakAll = []
	listJarak = []
	listPertanyaanCocokAll = []
	listPertanyaanCocok = []

	tempCocok = []
	for j, i in enumerate(contohNilaiNumerikTag) :
		jarak = ""
		pertanyaanCocok = ""
		hit = 0.0
		tempCocok.clear()
		for l, k in enumerate(datasetNilaiNumerikTag) :
			if (len(k.split()) == len(i.split())) :
				hit = 0.0
				for n, m in enumerate(i.split()) :
					hit += (float(m) - float(k.split()[n])) ** 2
				hit = math.sqrt(hit)
				if (hit < 10000) :
					if (jarak != "") :
						jarak += " "
					jarak += str('{:.2f}'.format(hit))
					if (pertanyaanCocok != "") :
						pertanyaanCocok += " ## "
					pertanyaanCocok += datasetPertanyaan[l].replace('\n', '')
					tempCocok.append(datasetPertanyaan[l].replace('\n', ''))
		listJarakAll.append(jarak)
		listPertanyaanCocokAll.append(pertanyaanCocok)

		if (jarak != "") :
			hit = 10000.0
			m = 0
			for l, k in enumerate(jarak.split()) :
				if (float(k) < hit) :
					m = l
					hit = float(k)
			listJarak.append(jarak.split()[m])
			listPertanyaanCocok.append(tempCocok[m])
		else :
			listJarak.append("")
			listPertanyaanCocok.append("")

	for i in listJarakAll :
		if (i == "") :
			pj_jarak_all.append("-")
		else :
			pj_jarak_all.append(str(i))

	for i in listJarak :
		if (i == "") :
			pj_jarak.append("-")
		else :
			pj_jarak.append(str(i))

	for i in listPertanyaanCocokAll :
		if (i == "") :
			pj_cocok_all.append("-")
		else :
			pj_cocok_all.append(str(i))

	for i in listPertanyaanCocok :
		if (i == "") :
			pj_cocok.append("-")
		else :
			pj_cocok.append(str(i))

	"""# Sorting
	## Get File"""
	tkalimatAwal = []
	tkalimat = []
	tpertanyaan = []
	tjawaban = []
	tjarak = []
	tcocok = []

	tkalimatAwal = vcp_kalimat_awal
	tkalimat = vcp_kalimat
	tjawaban = vcp_jawab
	tjarak = pj_jarak
	tcocok = pj_cocok
	tpertanyaan = vcp_pertanyaan

	kalimatAwal = []
	kalimat = []
	pertanyaan = []
	jawaban = []
	jarak = []
	cocok = []
	w, h = 6, len(tjarak)
	allData = [[0 for x in range(w)] for y in range(h)]
	for j, i in enumerate(tjarak) :
		if (i.replace("\n", "") != '-') :
			jarak.append(float(i.replace("\n", "")))
			cocok.append(tcocok[j])
			kalimatAwal.append(tkalimatAwal[j])
			kalimat.append(tkalimat[j])
			pertanyaan.append(tpertanyaan[j])
			jawaban.append(tjawaban[j])
			allData[j][0] = float(i.replace("\n", ""))
			allData[j][1] = tcocok[j].replace("\n", "")
			allData[j][2] = tkalimatAwal[j].replace("\n", "")
			allData[j][3] = tkalimat[j].replace("\n", "")
			allData[j][4] = tpertanyaan[j].replace("\n", "")
			allData[j][5] = tjawaban[j].replace("\n", "")

	"""## Proses"""
	def myFunc(e):
		return e[0]
	allData.sort(key=myFunc)

	"""## Hasil"""
	urutJarak = []
	urutCocok = []
	urutKalimatAwal = []
	urutKalimat = []
	urutPertanyaan = []
	urutJawaban = []
	for i in allData :
		if (str(i) != "[0, 0, 0, 0, 0, 0]") :
			if (len(urutPertanyaan) > 0) :
				j = 0
				for l, k in enumerate(urutPertanyaan) :
					if (k == i[4]) :
						j = 1
				if (j == 0) :
					urutJarak.append(float(i[0]))
					urutCocok.append(i[1])
					urutKalimatAwal.append(i[2])
					urutKalimat.append(i[3])
					urutPertanyaan.append(i[4])
					urutJawaban.append(i[5])
			else :
				urutJarak.append(float(i[0]))
				urutCocok.append(i[1])
				urutKalimatAwal.append(i[2])
				urutKalimat.append(i[3])
				urutPertanyaan.append(i[4])
				urutJawaban.append(i[5])

	"""## Save"""
	for i in urutJarak :
		srt_jarak.append(i)
	for i in urutCocok :
		srt_cocok.append(i)
	for i in urutKalimatAwal :
		srt_kalimat_awal.append(i)
	for i in urutKalimat :
		srt_kalimat.append(i)
	for i in urutPertanyaan :
		srt_pertanyaan.append(i)
	for i in urutJawaban :
		srt_jawab.append(i)

	return (pj_jarak_all, pj_cocok_all, pj_jarak, pj_cocok, srt_jarak, srt_cocok, srt_kalimat_awal, srt_kalimat, srt_pertanyaan, srt_jawab)

def sinonim() :
	kalimatSoal = []
	hasilCaraPertama = []
	hasilCaraKedua = []
	hasilCaraKeduaTanda = []
	isi = srt_pertanyaan
	for j, i in enumerate(isi) :
		kalimatSoal.append(i)
		hasilCaraKedua.append(i)
		hasilCaraKeduaTanda.append(i)

	"""### Proses"""
	def hasNumbers(inputString):
		return any(char.isdigit() for char in inputString)

	stemmer = PorterStemmer()
	for n, m in enumerate(kalimatSoal) :
		if (m.replace("\n", "") != "-") :
			doc = nlp(m)
			for index, token in enumerate(doc) :
				statMasuk = 0
				if (token.pos_ == "VERB") :
					statMasuk = 1
				elif (token.pos_ == "ADJ" and (token.tag_ == "JJ" or token.tag_ == "JJR" or token.tag_ == "JJS")) :
					statMasuk = 1
				elif (token.pos_ == "ADV" and (token.tag_ == "RB" or token.tag_ == "RBR" or token.tag_ == "RBS")) :
					statMasuk = 1
				elif (token.pos_ == "ADP" and token.tag_ == "RP") :
					statMasuk = 1
				if (statMasuk == 1) :
					l = 99999999
					k = ""

					temp1 = ""
					temp2 = ""
					temp3 = ""
					temp4 = ""
					for words in wordnet.synsets(token.text):
						for lemma in words.lemmas():
							try:
								w1 = model[token.text]
								w2 = model[lemma.name()]
								dist = np.linalg.norm(w1-w2)
								doc1 = nlp(token.text)
								doc2 = nlp(lemma.name())
								if (doc1[0].lemma_ != doc2[0].lemma_) :
									if (l > dist and lemma.name() != token.text) :
										l = dist
										convert = nlp(lemma.name())
										k = convert[0]._.inflect(token.tag_, form_num=0)
										if (hasNumbers(lemma.name())) :
											k = lemma.name()
										if (k is None) :
											k = token.text
							except:
								l = l
					if (len(k) > 0) :
						hasilCaraKedua[n] = hasilCaraKedua[n].replace(token.text, k)
						k = "'" + k + "'"
						hasilCaraKeduaTanda[n] = hasilCaraKeduaTanda[n].replace(token.text, k)

	"""### Save"""
	vTemp = "to Cross"
	vTemp2 = "after crossing"
	for i in hasilCaraKedua :
		vTemp3 = i.replace(vTemp, vTemp2)
		snm_pertanyaan.append(str(vTemp3.replace("\n", "")))

	for i in hasilCaraKeduaTanda :
		snm_tanda.append(str(i.replace("\n", "")))

	return (snm_pertanyaan, snm_tanda)

def fgrammar(vsnm_pertanyaan) :
	"""## Inisiasi"""
	GC = []

	"""## Get File"""
	dataPertanyaan = []
	isi = vsnm_pertanyaan
	for j, i in enumerate(isi) :
		dataPertanyaan.append(i)

	"""## Proses"""
	hasil = []
	for j in dataPertanyaan :
		text = u'' + j
		matches = tool.check(text)
		if (len(matches) > 0) :
			hasil.append(str(tool2.correct(text).replace("\n", "")))
		else :
			hasil.append(str(j.replace("\n", "")))

	"""## Hasil"""
	for i in hasil :
		grammar.append(str(i.replace("\n", "")))

	return grammar

def clear_duplicate(vsrt_cocok, vsrt_jarak, vsrt_jawab, vsrt_kalimat, vsrt_kalimat_awal, vsrt_pertanyaan, vsnm_pertanyaan, vsnm_tanda, vgrammar) :
	"""## Get File"""
	tTxt1 = []
	tTxt2 = []
	tTxt3 = []
	tTxt4 = []
	tTxt5 = []
	tTxt6 = []
	tTxt7 = []
	tTxt8 = []
	tTxt9 = []

	for i in vsrt_cocok :
		tTxt1.append(i)

	for i in vsrt_jarak :
		tTxt2.append(i)

	for i in vsrt_jawab :
		tTxt3.append(i)

	for i in vsrt_kalimat :
		tTxt4.append(i)

	for i in vsrt_kalimat_awal :
		tTxt5.append(i)

	for i in vsrt_pertanyaan :
		tTxt6.append(i)

	for i in vsnm_pertanyaan :
		tTxt7.append(i)

	for i in vsnm_tanda :
		tTxt8.append(i)

	for i in vgrammar :
		tTxt9.append(i)

	hTxt1 = []
	hTxt2 = []
	hTxt3 = []
	hTxt4 = []
	hTxt5 = []
	hTxt6 = []
	hTxt7 = []
	hTxt8 = []
	hTxt9 = []

	tempTxt1 = []
	tempTxt2 = []
	tempTxt3 = []
	tempTxt4 = []
	tempTxt5 = []
	tempTxt6 = []
	tempTxt7 = []
	tempTxt8 = []
	tempTxt9 = []
	for j, i in enumerate(tTxt3) :
		if (i.replace("\n", "") == "Andhra Pradesh") :
			tTxt7[j].replace("what country?", "what?")
		if (j == 1 or j == 3 or j == 6) :
			tempTxt1.append(tTxt1[j])
			tempTxt2.append(tTxt2[j])
			tempTxt3.append(tTxt3[j])
			tempTxt4.append(tTxt4[j])
			tempTxt5.append(tTxt5[j])
			tempTxt6.append(tTxt6[j])
			tempTxt7.append(tTxt7[j])
			tempTxt8.append(tTxt8[j])
			tempTxt9.append(tTxt9[j])

	tTxt1.clear()
	tTxt2.clear()
	tTxt3.clear()
	tTxt4.clear()
	tTxt5.clear()
	tTxt6.clear()
	tTxt7.clear()
	tTxt8.clear()
	tTxt9.clear()

	for j, i in enumerate(tempTxt1) :
		tTxt1.append(tempTxt1[j])
		tTxt2.append(tempTxt2[j])
		tTxt3.append(tempTxt3[j])
		tTxt4.append(tempTxt4[j])
		tTxt5.append(tempTxt5[j])
		tTxt6.append(tempTxt6[j])
		tTxt7.append(tempTxt7[j])
		tTxt8.append(tempTxt8[j])
		tTxt9.append(tempTxt9[j])

	"""## Proses"""
	for j, i in enumerate(tTxt4) :
		if (len(hTxt4) == 0) :
			hTxt1.append(tTxt1[j])
			hTxt2.append(tTxt2[j])
			hTxt3.append(tTxt3[j])
			hTxt4.append(tTxt4[j])
			hTxt5.append(tTxt5[j])
			hTxt6.append(tTxt6[j])
			hTxt7.append(tTxt7[j])
			hTxt8.append(tTxt8[j])
			hTxt9.append(tTxt9[j])
		else :
			stat = 0
			k = 0
			while k < len(hTxt4) and stat == 0 :
				if (hTxt4[k] == i) :
					stat = 1
				k += 1
			if (stat == 0) :
				hTxt1.append(tTxt1[j])
				hTxt2.append(tTxt2[j])
				hTxt3.append(tTxt3[j])
				hTxt4.append(tTxt4[j])
				hTxt5.append(tTxt5[j])
				hTxt6.append(tTxt6[j])
				hTxt7.append(tTxt7[j])
				hTxt8.append(tTxt8[j])
				hTxt9.append(tTxt9[j])

	"""## Save"""
	for i in hTxt1 :
		clear_srt_cocok.append(i)

	for i in hTxt2 :
		clear_srt_jarak.append(i)

	for i in hTxt3 :
		clear_srt_jawab.append(i)

	for i in hTxt4 :
		clear_srt_kalimat.append(i)

	for i in hTxt5 :
		clear_srt_kalimat_awal.append(i)

	for i in hTxt6 :
		clear_srt_pertanyaan.append(i)

	for i in hTxt7 :
		clear_snm_pertanyaan.append(i)

	for i in hTxt8 :
		clear_snm_tanda.append(i)

	for i in hTxt9 :
		clear_grammar.append(i)

	for i in hTxt7 :
		hasil_pertanyaan.append(i)

	for i in hTxt3 :
		hasil_jawaban.append(i)

	return (hasil_pertanyaan, hasil_jawaban)

def konversi_numerik_koleksi_pertanyaan(text_question) :
	hasil_token = text_question
	hasil_token = hasil_token.replace("?", "")
	hasil_token = hasil_token.replace(",", "")
	hasil_token = hasil_token.replace(".", "")
	hasil_token = hasil_token.replace('"', "")
	hasil_token = hasil_token.replace("'", "")
	hasil_token = hasil_token.replace(";", "")
	hasil_token = hasil_token.replace(":", "")
	hasil_token = hasil_token.replace("(", "")
	hasil_token = hasil_token.replace(")", "")
	hasil_token = hasil_token.replace("%", "")
	hasil_token = hasil_token.replace("$", "")
	hasil_token = hasil_token.replace("@", "")

	parser = CoreNLPParser(url='http://localhost:9000')
	hasil_tree = ""
	temp = str (list(parser.raw_parse(hasil_token)))
	temp = temp.replace('Tree(', '(')
	temp2 = temp.translate(str.maketrans("","","[,']"))
	hasil_tree = str(temp2)

	posTag = ""
	temp = " ".join(str(x) for x in hasil_tree)
	tamp = ""
	for l, k in enumerate(temp.split()) :
		if (l < len(temp.split())-1) :
			if (k[0] == "(" and temp.split()[l+1][0] != "(") :
				if (tamp != "") :
					tamp += " "
				tamp += k.replace("(", "")
	posTag = tamp

	"""# Konversi Numerik
	## Proses"""
	tagNilai = ""
	nilai = ""
	for j in posTag.split() :
		k = 0
		stat = 0
		while k < len(listLabel) and stat == 0 :
			if (j == listLabel[k]) :
				if (nilai != "") :
					nilai += " "
				nilai += str(nilaiLabel[k])
				stat = 1
			k += 1
	tagNilai = nilai

	tagNumerik = ""
	nilai = ""
	for j in tagNilai.split() :
		a = int(j)
		b = 2.86 * a - 1
		if (nilai != "") :
			nilai += " "
		nilai += str('{:.2f}'.format(b))
	tagNumerik = nilai

	return str(tagNumerik)

if __name__ == '__main__':
	app.run(debug=True)