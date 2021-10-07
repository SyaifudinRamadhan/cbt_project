from django.shortcuts import render, redirectfrom django.contrib.auth import login as loginSys, logout, authenticatefrom loginSys import functions, modelsfrom adminSide import models as models_2, getData_functions as f_getfrom django.contrib.auth.models import Userfrom django.core.paginator import EmptyPage, Paginator, PageNotAnIntegerfrom . import controller_test as C_Tfrom .pool import quest_data, list_valfrom django.http import HttpRequestimport json as simplejsonfrom datetime import datetime as today# from django.utils import simplejson# Deklarasi class untuk mengambil dan menyimpan soal sementaradataView = quest_data()ans_list = list_val()# Halaman depan (Umum)def index (request):		return render(request, 'index.html')def cek (request):	print('Cek sek broo !!!\n')	if request.GET.get('out') != None :		print('Pernah keluar halaman\n')		ans_list.add_out()		return redirect('/cek')	print('Out ke - ',ans_list.get_out(),'\n')	context = {		'out_count':ans_list.get_out(),	}	return render(request, 'cek.html', context)# Semua di bawah halaman setelah logindef dashboard (request):	# Cek kondisi login user	nextStep = functions.loginCheck(request)	if nextStep != 'None' :		return redirect(nextStep)	state = functions.getState(request.user)	name = functions.getName(request.user)	context = {		'status':state,		'name':name,	}	return render(request, 'dashboard_siswa.html', context)def schedule (request):	# Cek kondisi login user	nextStep = functions.loginCheck(request)	if nextStep != 'None' :		return redirect(nextStep)	page = request.GET.get('page')	print('cek saja \n',page,'\n')	listSchedule = f_get.getSchedule(request, request.user)	lisRes = []	view = []	for x in range(len(listSchedule)):		date = str(listSchedule[x].date)		time = str(listSchedule[x].start)		state = str(listSchedule[x].state)		token = str(listSchedule[x].token)		course = models_2.course_data.objects.filter(id = listSchedule[x].id_course)		class_ = models_2.class_data.objects.filter(id = listSchedule[x].id_course)		tmp = [date, time, state, course[0].course_name, class_[0].class_name, token]		lisRes.append(tmp)	paginate = Paginator(lisRes, 10)	print(paginate.page(1))	try:		view = paginate.page(page)	except PageNotAnInteger:		view = paginate.page(1)	except EmptyPage:		view = paginate.page(paginate.num_pages)	context = {		'name':functions.getName(request.user),		'schedule_list':lisRes,		'count':len(listSchedule),		'data':view,	}	return render(request, 'schedule_list.html', context)# Perlu di teliti lagi, keamanan setelah token di sumbit belum selesai (21-09-2021)def startTest (request):	# Cek kondisi login user	nextStep = functions.loginCheck(request)	if nextStep != 'None' :		return redirect(nextStep)	# Penanangan back page saat ujian berjalan	statuses = models_2.result_test.objects.filter(id_students = request.user, state_test = 'ongoing')	if len(statuses) != 0:		print('banyak ongoing ',len(statuses))		return redirect('/std_test_run')	directory = '' 	inf_quest = ''	endTime = ''	sTime = ''	# C_T.run_test()	if request.method == "POST" :		directory, inf_quest, endTime, sTime = f_get.getQuestFile(request)		dataView.setInfo(inf_quest)		print('\n','Masuk start test',inf_quest,'\n')	if inf_quest == '' and request.method == "POST" :		# Penanganan terhadapa token yang sudah dikerjakan		check_token = models_2.result_test.objects.filter(id_students = request.user, token = request.POST['token'])		if len(check_token) != 0 :			context = {				'name':functions.getName(request.user),				'inf': 'SOAL SUDAH DIKERJAKAN !!! ( > - < )',			}			return render(request, 'start_test.html', context)		print(directory,'\n')		# Membuat session ujian		functions.set_resTest(request, models_2)		print('\n','Session dibuat gan','\n')		# Mengambil data untuk di ditampilkan		dic_quest, keys_quest, err_msg_quest = C_T.run_test(directory)		dataView.setter(dic_quest, keys_quest, err_msg_quest)		ans_list.initial(len(dataView.getKeys()), endTime, sTime)		return redirect('/std_test_run')			else :		context = {			'name':functions.getName(request.user),			'inf': inf_quest,		}		return render(request, 'start_test.html', context)def viewResTest (request):	# Cek kondisi login user	nextStep = functions.loginCheck(request)	if nextStep != 'None' :		return redirect(nextStep)	page = request.GET.get('page')	print('\n',page,'\n')	listData = []	view = []	res = f_get.viewResultTest(request, request.user)		for x in range(len(res)):		date = str(res[x].date)		result = str(res[x].result)		tmp = models_2.quest_data.objects.filter(id = res[x].id_quest)		course_obj = models_2.course_data.objects.filter(id = tmp[0].id_course)		course = str(course_obj[0].course_name)		id_teach = str(res[x].id_teacher)		tmp2 = [date, course, id_teach, result]		listData.append(tmp2)			paginate = Paginator(listData, 10)	try:		view = paginate.page(page)	except PageNotAnInteger :		view = paginate.page(1)	except EmptyPage :		view = paginate.page(paginate.num_pages)	context = {		'name':functions.getName(request.user),		'data': view,		'count': len(res),	}	return render(request, 'result_test_list.html', context)def evaluationView (request):	# Cek kondisi login user	nextStep = functions.loginCheck(request)	if nextStep != 'None' :		return redirect(nextStep)	context = {		'name':functions.getName(request.user)	}	return render(request, 'view_evaluation.html', context)def setAccount (request):	# Cek kondisi login user	nextStep = functions.loginCheck(request)	confirm = []	if nextStep != 'None' :		return redirect(nextStep)	if request.method == "POST":		confirm = functions.editStdAcc(request)	main = User.objects.filter(username = request.user)	spec = models.students_user.objects.filter(no_induk = request.user)	second = models.user_second.objects.filter(no_induk = request.user)	arr = ['dds','fdfdf','fdghfg']	context = {		'name':functions.getName(request.user),		'mainUser': main[0],		'std_user': spec[0],		'sec_user': second[0],		'confirm' : confirm,		'profile' : "/media/"+second[0].profile,	}	print(main[0].username)	return render(request, 'set_acc.html', context)def testMain (request):	# Cek kondisi login user		# looping untuk mengetahui kondisi pengaksesan	print('\n','Mulai dari awal','\n')	nextStep = functions.loginCheck(request)	if nextStep != 'None' :		return redirect(nextStep)	second = models.user_second.objects.filter(no_induk = request.user)	page = request.GET.get('page')	print('cek saja \n',page,'\n')	ans = request.GET.get('c')	print('cek jawab',' ',ans,'\n')	# ans_list = list_val(len(dataView.getKeys()))	context = {		'name':functions.getName(request.user),		'profile' : "/media/"+second[0].profile,	}		if dataView.getInfo() == '' :		print('Masuk info error kosong\n')		dic_quest, err_msg_quest = dataView.getter()		if err_msg_quest == True :			# Variabel untuk paginasi (type class Paginator) setiap variabel view test			text_quest = Paginator(dic_quest['text_quest'], 1)			ans_txt = Paginator(dic_quest['ans_txt'], 1)			val_ans = Paginator(dic_quest['val_ans'], 1)			type_quest = Paginator(dic_quest['type_quest'], 1)			max_check = Paginator(dic_quest['max_check'], 1)			img_quest = Paginator(dic_quest['img_quest'], 1)			videos_quest = Paginator(dic_quest['videos_quest'], 1)			audio_quest = Paginator(dic_quest['audio_quest'], 1)			if request.GET.get('out') != None :				ans_list.add_out()				print('Pernah keluar\n')				return redirect('/std_test_run')						print('Out ke : ',ans_list.get_out(),'\n')						p = ''			# Mengirim jawaban untuk di periksa			# Problrm baru saat simpan jawaban di memory jika berbeda type soal (20-09-2021)						# Periksa kembali karena masalah saat ini			if_checkbpx = []			if request.GET.get('finish') != None :				# Menambahkan jawaban yang terpilih sebelum submit				prev = ans_list.get_prev_pss()				if prev == '':					prev = 1				a = request.GET.get('c1')				b = request.GET.get('c2')				c = request.GET.get('c3')				d = request.GET.get('c4')				e = request.GET.get('c5')				if a != None or b != None or c != None or d != None or e != None :					if a != None :						if_checkbpx.append(a)					if b != None :						if_checkbpx.append(b)					if c != None :						if_checkbpx.append(c)					if d != None :						if_checkbpx.append(d)					if e != None :						if_checkbpx.append(e)					ans_list.set_list(prev, if_checkbpx)					print(if_checkbpx,' Masuk finish 2','\n')				elif request.GET.get('c') != None :					ans = request.GET.get('c')					ans_list.set_list(prev, ans)					# print(ans,' ',ans_list.get_list(4),' ',prev,' masuk finish 1','\n')				# Memeriksa, memberi nilai, dan input hasil ke dalam db				end_value = C_T.correctionAns(ans_list, dataView)				confirm = functions.change_resTest(request, models_2, end_value)				print(confirm,' ',end_value,'\n')				return redirect('/view_result_test')			# Mamasukkan jawaban ke models list_val			elif request.GET.get('page') == None :				ans_list.set_prev_pss(1)				p = 1				print('set page lama','\n')			# ini masalah saat ini			elif request.GET.get('page') != None :				p = int(request.GET.get('page'))				prev = ans_list.get_prev_pss()				# print(type(int(type_quest.page(1))))				if type_quest.page(p)[0] == 2:					if request.GET.get('c') != None :						ans = request.GET.get('c')						print('\n','masuk radio','\n')						ans_list.set_list(prev, ans)					else:						print('\n','masuk checkbox','\n')						a = request.GET.get('c1')						b = request.GET.get('c2')						c = request.GET.get('c3')						d = request.GET.get('c4')						e = request.GET.get('c5')						if a != None :							if_checkbpx.append(a)						if b != None :							if_checkbpx.append(b)						if c != None :							if_checkbpx.append(c)						if d != None :							if_checkbpx.append(d)						if e != None :							if_checkbpx.append(e)						if a == None and b == None and c == None and d == None and e == None :							if_checkbpx = ''						ans_list.set_list(prev, if_checkbpx)				elif type_quest.page(p)[0] == 1 :					if request.GET.get('c') != None :						ans = request.GET.get('c')						print('\n','masuk radio','\n')						ans_list.set_list(prev, ans)					else:						print('\n','masuk checkbox','\n')						a = request.GET.get('c1')						b = request.GET.get('c2')						c = request.GET.get('c3')						d = request.GET.get('c4')						e = request.GET.get('c5')						if a != None :							if_checkbpx.append(a)						if b != None :							if_checkbpx.append(b)						if c != None :							if_checkbpx.append(c)						if d != None :							if_checkbpx.append(d)						if e != None :							if_checkbpx.append(e)						if a == None and b == None and c == None and d == None and e == None :							if_checkbpx = ''						ans_list.set_list(prev, if_checkbpx)				ans_list.set_prev_pss(p)			# Variabel list untuk yang sudah di paginasi oleh class paginator			view_text_quest = []			view_ans_txt = []			view_val_ans = []			view_type_quest = []			view_max_check = []			view_img_quest = []			view_videos_quest = []			view_audio_quest = []			# Proses perubahan variabel type class paginator to type List			try:				view_text_quest = text_quest.page(page)				view_ans_txt = ans_txt.page(page)				view_val_ans = val_ans.page(page)				view_type_quest = type_quest.page(page)				view_max_check = max_check.page(page)				view_img_quest = img_quest.page(page)				view_videos_quest = videos_quest.page(page)				view_audio_quest = audio_quest.page(page)			except PageNotAnInteger:				view_text_quest = text_quest.page(1)				view_ans_txt = ans_txt.page(1)				view_val_ans = val_ans.page(1)				view_type_quest = type_quest.page(1)				view_max_check = max_check.page(1)				view_img_quest = img_quest.page(1)				view_videos_quest = videos_quest.page(1)				view_audio_quest = audio_quest.page(1)			except EmptyPage:				view_text_quest = text_quest.page(paginate.num_pages)				view_ans_txt = ans_txt.page(paginate.num_pages)				view_val_ans = val_ans.page(paginate.num_pages)				view_type_quest = type_quest.page(paginate.num_pages)				view_max_check = max_check.page(paginate.num_pages)				view_img_quest = img_quest.page(paginate.num_pages)				view_videos_quest = videos_quest.page(paginate.num_pages)				view_audio_quest = audio_quest.page(paginate.num_pages)			# print('\n',view_ans_txt[0],'\n')			# print('\n',ans_txt.page(1)[0],'\n')			elapsed = 0			t_d = str(today.now().time()).split('.')			t_now = today.strptime(t_d[0], "%H:%M:%S")			t_start = today.strptime(str(ans_list.get_start_time()), "%H:%M:%S")			limit = ans_list.get_limit_time()			if t_now > t_start:				t_ = str(t_now - t_start).split(':')				elapsed = (int(t_[0])*3600)+(int(t_[1])*60)+int(t_[2])			if elapsed < limit :				limit = limit - elapsed			elif elapsed > limit :				limit = 0			print(len(view_img_quest),'\n')			context = {				'name':functions.getName(request.user),				'confirm': '',				'text_quest' : view_text_quest,				'ans_txt' : view_ans_txt[0],				'val_ans' : view_val_ans,				'type_quest' : view_type_quest,				'max_check' : view_max_check,				'img_quest' : view_img_quest[0],				'videos_quest' : view_videos_quest[0],				'audio_quest' : view_audio_quest[0],				'profile' : "/media/"+second[0].profile,				'answeared' : simplejson.dumps(ans_list.get_list(p-1)),				'ans_all' : simplejson.dumps(ans_list.get_all()),				'end_time' : limit*1000,				'out_count' : ans_list.get_out(),				'page': p,			}			print('\n',ans_list.get_all(),'\n',p-1,' ',ans_list.get_list(p-1),'\n')			print(context)			return render(request, 'test_main.html', context)		elif err_msg_quest == False :			context = {				'name':functions.getName(request.user),				'confirm': dataView.getInfo()+" Error soal RUSAK",				'profile' : "/media/"+second[0].profile,			}			# Mengakhiri sesi token saat itu			models_2.result_test.objects.get(id_students = request.user, state_test = 'ongoing').delete()			# jika masuk sini harus di return render page lain			return render(request,'test_confirm.html', context)	else :		print('Masuk info error token kosong\n')		if request.GET.get('finish') != None or request.GET.get('out')!= None:			return redirect('/view_result_test')		context = {			'name':functions.getName(request.user),			'confirm': dataView.getInfo(),			'profile' : "/media/"+second[0].profile,		}		# jika masuk sini harus di return render page lain		return render(request,'test_confirm.html', context)	# print(err_msg_quest,' ',inf_quest,' ',context,'\n')	