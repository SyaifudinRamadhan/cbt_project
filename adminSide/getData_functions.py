from . import models
from loginSys import models as models_2
from django.db.models import Q
import random as rd
from datetime import datetime as today
from django.contrib.auth.models import User as main_user
import pandas as pd

# ------ function get data untuk view list jadwal di table (Umum) ------------
def getSchedule (request, key, admin = False, teach = False, students = True):
	listData = []

	if admin == True or teach == True:
		obj = []
		try:
			if admin == True:
				id_admin = models_2.user_second.objects.get(no_induk = request.user).id
				obj = models.schedule_data.objects.filter(id_admin = id_admin).order_by('-date','-start')
			elif teach == True:
				obj = models.schedule_data.objects.filter(id_teacher = request.user)
		except Exception as e:
			print( str(e))
			listData = ''

		for x in range(len(obj)):
			ID = obj[x].id
			date = str(obj[x].date)
			start = str(obj[x].start)
			end = str(obj[x].end)
			drt = str(obj[x].duration)
			token = obj[x].token
			state = obj[x].state
			# Dari FK ke data real
			tch = models_2.user_second.objects.get(no_induk = obj[x].id_teacher)
			class_name = models.class_data.objects.get(id = obj[x].id_class).class_name
			course = models.course_data.objects.get(id = obj[x].id_course).course_name
			tmp = [date, start, end, drt, tch, class_name, course, token, state, ID]
			listData.append(tmp)
	elif students == True :
		# Evaluasi lagi bagian ini 
		# Bagian ini -> ambil jadwal harus didasarkan id admin dari guru yang diambil siswa dan kelas yang diambil siswa
		# print('masuk',' ',key)
		obj_stdn = models_2.students_user.objects.get(no_induk = key)
		id_admin = ''
		try:
			admin_no_induk = models_2.theachers_user.objects.get(no_induk = obj_stdn.guru_id).admin_id
			id_admin = models_2.user_second.objects.get(no_induk = admin_no_induk).id
		except Exception as e:
			print(e)

		if id_admin != '' and obj_stdn.id_class != None:
		# keySch = models_2.students_user.objects.filter(no_induk = )
			try:
				if request.method == "POST" :
					query = request.POST['search']
					listData = models.schedule_data.objects.filter(Q(id_admin = id_admin), Q(id_class = obj_stdn.id_class), Q(date__contains = query) | Q(state__contains = query) | Q(token__contains = query) | Q(start__contains = query)).order_by('-date')
				else :
					listData = models.schedule_data.objects.filter(id_admin = id_admin, id_class = obj_stdn.id_class).order_by('-date','-start')
			except Exception as e:
				print( str(e))
				listData = []
	print(len(listData))
	return listData

# ---- function get data untuk view table hasil ujian ----------------
def viewResultTest (request, key, has_eval = '' ,admin = False, teach = False, students = True):
	data = ''
	if admin == True :
		key = models_2.user_second.objects.get(no_induk = request.user).id
		if request.method == "POST" and request.POST.get('search') != None :
			if has_eval == '':
				data = models.result_test.objects.filter(id_admin = key).order_by('-id')
			elif has_eval == 'non':
				data = models.result_test.objects.filter(id_admin = key, state_eval = has_eval)
		else:
			if has_eval == '':
				data = models.result_test.objects.filter(id_admin = key).order_by('-id')
			elif has_eval == 'non':
				data = models.result_test.objects.filter(id_admin = key, state_eval = has_eval)
	elif teach == True :
		if request.method == "POST" and request.POST.get('search') != None :
			if has_eval == '':
				data = models.result_test.objects.filter(id_teacher = key).order_by('-id')
			elif has_eval == 'non':
				data = models.result_test.objects.filter(id_teacher = key, state_eval = has_eval)
		else:
			if has_eval == '':
				data = models.result_test.objects.filter(id_teacher = key).order_by('-id')
			elif has_eval == 'non':
				data = models.result_test.objects.filter(id_teacher = key, state_eval = has_eval)
	else :
		if request.method == "POST" and request.POST.get('search') != None :
			word = request.POST.get('search')
			data = models.result_test.objects.filter(Q(id_students = key), Q(date__contains = word)|Q(result__contains = word)|Q(id_teacher__contains = word)).order_by('-id')
		else:
			data = models.result_test.objects.filter(id_students = key).order_by('-id')
			
	if data != '':
			
			view = []
			obj = data
			# date, result, state_test, token, mapel, guru, no induk guru, siswa, no induk siswa
			for x in range(len(obj)):
				tmp = []
				tmp.append(str(obj[x].date))
				tmp.append(obj[x].id_students)
				try:
					tmp.append(models_2.user_second.objects.get(no_induk = obj[x].id_students).username)
				except Exception as e:
					tmp.append('Dihapus')
				tmp.append(obj[x].id_teacher)
				try:
					tmp.append(models_2.user_second.objects.get(no_induk = obj[x].id_teacher).username)
				except Exception as e:
					tmp.append('Dihapus')
				# Mendapatkan nama mapel
				try:
					tmp.append(models.course_data.objects.get(
						id = obj[x].id_quest
						).course_name)
				except Exception as e:
					print(e)
					tmp.append('Dihapus')
				tmp.append(obj[x].state_test)
				tmp.append(obj[x].token)
				tmp.append(obj[x].result)
				tmp.append(obj[x].id)
				try:
					tmp.append(models.class_data.objects.get(
						id = models_2.students_user.objects.get(
							no_induk = obj[x].id_students
							).id_class
						).class_name)
				except Exception as e:
					tmp.append('Dihapus')

				view.append(tmp)

			return view
	else:
			return ''

# def getDataStdn (request):
# 	mainData = User.objects.filter(username = request.user)
# 	print(len(mainData))
# 	return True

# ---------- function get data file xls dan batas waktu untuk memulai test -----------------
def getQuestFile (request) :
	directory = ''
	confirm = ''
	END_Time = ''
	s_time = [0]
	list_quest = []
	if request.method == 'POST' :
		token = request.POST['token']
		
		try:
			schedule = models.schedule_data.objects.get(token = token, date = today.now().date())
		except Exception as e:
			print('\n',e,'\n')
			confirm = 'Error, Token tidak tersedia.'

		if confirm == '' :
			# print(schedule.state,'\n')
			if schedule.state == 'active' :
				course = schedule.id_course
				id_teach = schedule.id_teacher
				id_class = schedule.id_class
				s_time = str(today.now().time()).split('.')

				time_now = str(today.now().time()).split('.')
				end_time = str(schedule.end)
				print(time_now)

				t_time_now = today.strptime(time_now[0], "%H:%M:%S")
				t_end_time = today.strptime(end_time, "%H:%M:%S")
				if t_time_now < t_end_time :
					tmp = str(t_end_time - t_time_now).split(':')
					print(tmp,'\n')
					END_Time = int((int(tmp[0])*3600) + (int(tmp[1])*60) + int(tmp[2]))
					print(END_Time,'\n')
				else:
					END_Time = 0.001
						

				print(course)
				quest = models.quest_data.objects.filter(id_course = course, id_teacher = id_teach, id_class = id_class)
				# print(quest.serial_quest)
				
				if len(quest) != 0 :
					for i in range(len(quest)) :
						list_quest.append(quest[i].serial_quest)
				else :
					confirm = 'Error, Mapel / Soal tidak tersedia.'

			elif schedule.state == 'deactive' :
				confirm = 'Error, Token tidak aktif.'

		if len(list_quest) != 0 :
			print(list_quest)
			directory = rd.choice(list_quest)
			directory = 'media/'+directory
		else :
			confirm += 'Error, gagal mengambil direktori soal.'
		print(confirm,' ',directory,'\n')
	else :
		confirm = 'Tidak ada request POST.'

	return directory, confirm, END_Time, s_time[0]

#  ------- belum terdefinisi -------------------------------------
def getDataTch (request):
	return True

def getDataAdmin (request):
	obj_main = main_user.objects.get(username = request.user)
	obj_second = models_2.user_second.objects.get(no_induk = request.user)

	return obj_main, obj_second

# ----- function get data untuk view di dalam tabel ----------------
def get_quest_table (request, pss = 'admin'):
	obj_quest_data = ''
	listData = []
	if pss == 'admin':
		obj_quest_data = models.quest_data.objects.filter(id_admin = models_2.user_second.objects.get(no_induk = request.user).id)
	elif pss == 'teacher':
		obj_quest_data = models.quest_data.objects.filter(id_teacher = request.user)

	print(models_2.user_second.objects.get(no_induk = request.user).id,'\n')

	for x in range(len(obj_quest_data)):
		ID = obj_quest_data[x].id
		file_quest = obj_quest_data[x].serial_quest
		name_teacher = models_2.user_second.objects.get(no_induk = obj_quest_data[x].id_teacher).username
		cour_name = models.course_data.objects.get(id = obj_quest_data[x].id_course).course_name
		class_name = models.class_data.objects.get(id = obj_quest_data[x].id_class).class_name
		tmp = [ID, file_quest, name_teacher, cour_name, class_name]
		listData.append(tmp)

	return listData

# ------- function get data untuk mendapat data di modal add soal dan add jadwal serta data view kelas dan guru----------------
def for_add_quest(request, pss = 'admin'):
	obj_course = ''
	obj_tch = ''
	id_admin = ''
	out_tch = []
	out_crs = []
	if pss == 'admin':
		# Bagian membentuk filter array
		key0 = models_2.theachers_user.objects.filter(admin_id = request.user)
		for x in range(len(key0)):
			obj_tch = models_2.user_second.objects.get(no_induk = key0[x].no_induk)
			out_tch.append([obj_tch.no_induk, obj_tch.username])
			
		obj_course = models.course_data.objects.filter(id_admin = int(models_2.user_second.objects.get(no_induk = request.user).id))
		
		id_admin = models_2.user_second.objects.get(no_induk = request.user).id
	elif pss == 'teacher':
		obj_course = models.course_data.objects.filter(id_teacher = request.user)
		obj_tch = models_2.user_second.objects.filter(no_induk = request.user)
		for x in range(len(obj_tch)):
			tmp = [obj_tch[x].no_induk, obj_tch[x].username]
			out_tch.append(tmp)

		try:
			id_admin = models_2.user_second.objects.get(
			no_induk = models_2.theachers_user.objects.get(
				no_induk = request.user).admin_id
			).id
		except Exception as e:
			print(e)

	for x in range(len(obj_course)):
		tch_name = models_2.user_second.objects.get(no_induk = obj_course[x].id_teacher)
		tmp = [obj_course[x].id, obj_course[x].course_name, tch_name, obj_course[x].id_teacher]
		out_crs.append(tmp)

	return out_crs, out_tch, id_admin

# ------ Function get data list untuk umum admin dan teacher --------------
def get_list_class(request, pss = 'admin', for_ = 'view'):
	view = []
	data = ''
	if pss == 'admin':
		data = models.class_data.objects.filter(
			id_admin = models_2.user_second.objects.get(no_induk = request.user).id
			)
	elif pss == 'teacher':
		if for_ == 'view':
			data = models.class_data.objects.filter(id_teacher = request.user)
		elif for_ == 'select':
			try:
				data = models.class_data.objects.filter(
					id_admin = models_2.user_second.objects.get(
						no_induk = models_2.theachers_user.objects.get(
							no_induk = request.user).admin_id
						).id
					)
			except Exception as e:
				print(e)
	for x in range(len(data)):
		tch_name = models_2.user_second.objects.get(no_induk = data[x].id_teacher).username
		tmp = [data[x].id, data[x].class_name, tch_name, data[x].id_teacher]
		view.append(tmp)
	return view

# ------------- function get data untuk membaca xls online (umum) -----
def read_xls_online(request):
	file = request.FILES['xls']
	xls_list = []
	try:
		data_frame = pd.read_excel(file)
		xls_list = data_frame.values.tolist()
		# del xls_list[0]
		confirm = ''
		for x in range(len(xls_list)):
			for y in range(len(xls_list[0])):
				if pd.isna(xls_list[x][y]) == True:
					xls_list[x][y] = ''
		return confirm, xls_list
	except Exception as e:
		print(e)
		confirm = 'Error file'
		return confirm, xls_list

# ------------ function get data read xls in media (kontrol data membuat soal) -----------
def read_xls_storage(request, data_id):
	id_data = data_id
	file_name = ''
	xls_list = []
	try:
		file_name = models.quest_data.objects.get(id = id_data).serial_quest
		data_frame = pd.read_excel('media/'+file_name)
		xls_list = data_frame.values.tolist()
		del xls_list[0]
	except Exception as e:
		print(e,'\n')

	for x in range(len(xls_list)):
		for y in range(len(xls_list[0])):
			if pd.isna(xls_list[x][y]) == True:
				xls_list[x][y] = ''
			elif str(type(xls_list[x][y])) == "<class 'float'>" or str(type(xls_list[x][y])) == "<class 'int'>":
				xls_list[x][y] = str(int(xls_list[x][y]))

	return xls_list, file_name

# ------------- Function get data untuk view table guru --------------------
def view_tch_data(request, pss = 'admin'):
	obj = ''
	view = []

	if pss == 'admin':
		obj = models_2.theachers_user.objects.filter(admin_id = request.user)
	elif pss == 'teacher':
		obj = models_2.theachers_user.objects.filter(no_induk = request.user)

	if obj != '':
		for x in range(len(obj)):
			v = models_2.user_second.objects.get(no_induk = obj[x].no_induk)
			v1 = main_user.objects.get(username = obj[x].no_induk)
			view.append([
				v.id, v1.id, obj[x].id, v.no_induk, v.username, obj[x].agency, 
				v1.first_name, v1.last_name, v1.email, v.profile
				])
	return view

# ----------- Function untuk view data table sisswa (admin - teacher) -----------------
def view_stdn_data(request, pss = 'admin'):
	obj = ''
	view = []

	if pss == 'admin':
		arr_key = []
		obj_key = models_2.theachers_user.objects.filter(admin_id = request.user)
		for x in range(len(obj_key)):
			arr_key.append(obj_key[x].no_induk)

		obj = models_2.students_user.objects.filter(guru_id__in = arr_key)
	elif pss == 'teacher':
		obj = models_2.students_user.objects.filter(guru_id = request.user)

	if obj != '':
		print(len(obj))
		for x in range(len(obj)):
			v = models_2.user_second.objects.get(no_induk = obj[x].no_induk)
			v1 = main_user.objects.get(username = obj[x].no_induk)
			tch = ''
			Class = ''
			try:
				tch = models_2.user_second.objects.get(no_induk =  obj[x].guru_id).username
			except Exception as e:
				print(e)
				tch = 'Belum di set'
			
			try:
				Class = models.class_data.objects.get(id = obj[x].id_class).class_name
			except Exception as e:
				print(e)
				Class = 'Belum di Set'
			view.append([
				v.id, v1.id, obj[x].id, v.no_induk, v.username, obj[x].guru_id, tch, obj[x].id_class, Class,
				v1.first_name, v1.last_name, v1.email, v.profile
				])
	return view


# def view_class_data(request, pss = 'admin'):
# 	obj = ''
# 	view = []

# 	if pss == 'admin':
# 		obj = models.class_data.objects.filter(id_admin)
# 	elif pss =='teacher':
# 		pass


def view_eval_data(request, view_for = 'admin'):
	all_data = []

	if view_for == 'admin' or view_for == 'teacher':
		obj = ''
		if view_for =='admin':
			teachers = []
			tchs = models_2.theachers_user.objects.filter(admin_id = 
					request.user)
			obj = []
			for x in range(len(tchs)):
				try:
					obj.append(models.evaluation_tch.objects.get(id_teacher = 
						tchs[x].no_induk, state = 'result'))
				except Exception as e:
					print(e)
		else:
			obj = models.evaluation_tch.objects.filter(id_teacher = request.user, state = 'result')
			
		for x in range(len(obj)):
			name = models_2.user_second.objects.get(no_induk = obj[x].id_teacher).username
			tmp = [obj[x].date, obj[x].id_teacher, name, obj[x].score, obj[x].state, obj[x].cat_1, obj[x].cat_2, obj[x].cat_3,
			obj[x].cat_4, obj[x].cat_5, obj[x].cat_6, obj[x].cat_7, obj[x].cat_8, obj[x].cat_9, obj[x].cat_10, 
			obj[x].cat_11, obj[x].cat_spec, obj[x].id]
			all_data.append(tmp)
		# print(all_data)
			# print(obj[x].date)
		
	elif view_for == 'student':
		obj = models.evaluation_stdn.objects.filter(id_students = request.user).order_by('-date')
		for x in range(len(obj)):
			tmp = [obj[x].date, obj[x].min_score, obj[x].max_score, obj[x].quote]
			all_data.append(tmp)
			
	return all_data




