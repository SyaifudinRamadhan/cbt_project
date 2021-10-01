from . import models
from loginSys import models as models_2
from django.db.models import Q
import random as rd
from datetime import datetime as today
from django.contrib.auth.models import User as main_user
import pandas as pd

def getSchedule (request, key, admin = False, teach = False, students = True):
	listData = ''

	if admin == True :
		try:
			# if request.method == "POST" :
			# 	query = request.POST['search']
			# 	listData = models.schedule_data.objects.filter(id_admin = key,
			# 	 (Q(date_icontains = query) | 
			# 	 Q(start_icontains = query) | 
			# 	 Q(state_icontains = query)))
			listData = models.schedule_data.objects.filter(id_admin = key).order_by('-date','-start')
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	elif teach == True :
		try:
			listData = models.schedule_data.objects.filter(id_teacher = key).order_by('-date','-start')
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	else :
		print('masuk',' ',key)
		keySch = models_2.students_user.objects.filter(no_induk = key)
		
		try:
			if request.method == "POST" :
				query = request.POST['search']
				listData = models.schedule_data.objects.filter(Q(id_teacher = keySch[0].guru_id), Q(date__contains = query) | Q(state__contains = query) | Q(token__contains = query) | Q(start__contains = query)).order_by('-date')
			else :
				listData = models.schedule_data.objects.filter(id_teacher = keySch[0].guru_id).order_by('-date','-start')
		except Exception as e:
			print( str(e))
			listData = ''
	print(len(listData))
	return listData

def viewResultTest (request, key, admin = False, teach = False, students = True):

	if admin == True :
		if request.method == "POST" and request.POST.get('search') != None :
			data = models.result_test.objects.filter(id_admin = key).order_by('-id')
			print(data)
			return data
		else:
			data = models.result_test.objects.filter(id_admin = key).order_by('-id')
			print(data)
			return data
	elif teach == True :
		if request.method == "POST" and request.POST.get('search') != None :
			data = models.result_test.objects.filter(id_teacher = key).order_by('-id')
			print(data)
			return data
		else:
			data = models.result_test.objects.filter(id_admin = key).order_by('-id')
			print(data)
			return data
	else :
		if request.method == "POST" and request.POST.get('search') != None :
			word = request.POST.get('search')
			data = models.result_test.objects.filter(Q(id_students = key), Q(date__contains = word)|Q(result__contains = word)|Q(id_teacher__contains = word)).order_by('-id')
			print(data)
			return data
		else:
			data = models.result_test.objects.filter(id_students = key).order_by('-id')
			print(data)
			return data

# def getDataStdn (request):
# 	mainData = User.objects.filter(username = request.user)
# 	print(len(mainData))
# 	return True

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
				quest = models.quest_data.objects.filter(id_course = course, id_teacher = id_teach)
				# print(quest.serial_quest)
				
				if len(quest) != 0 :
					for i in range(len(quest)) :
						list_quest.append(quest[i].serial_quest)
				else :
					confirm = 'Error, Mapel tidak tersedia.'

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


def getDataTch (request):
	return True

def getDataAdmin (request):
	return True

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
		tmp = [ID, file_quest, name_teacher, cour_name]
		listData.append(tmp)

	return listData

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

		id_admin = models_2.user_second.objects.get(
			no_induk = models_2.theachers_user.objects.get(
				no_induk = request.user).admin_id
			).id

	for x in range(len(obj_course)):
		tmp = [obj_course[x].id, obj_course[x].course_name]
		out_crs.append(tmp)

	return out_crs, out_tch, id_admin

def read_xls_online(request):
	file = request.FILES['xls']
	xls_list = []
	try:
		data_frame = pd.read_excel(file)
		xls_list = data_frame.values.tolist()
		del xls_list[0]
		confirm = ''
		return confirm, xls_list
	except Exception as e:
		print(e)
		confirm = 'Error file'
		return confirm, xls_list
