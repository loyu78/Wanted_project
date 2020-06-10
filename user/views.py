import json
import bcrypt
import jwt
import re
import time

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from partial_date       import PartialDateField
from datetime           import datetime

from utils              import login_decorator
from insa.settings      import SECRET_KEY
from company.models     import Position, Company, Image, Country, City, Company_matchup, Proposal, Job_category, Role, Country
from .models            import User, Security, Resume, Career, Result, Education, Award, Language, Test, Link, Level, Linguistic, Resume_file, Want, Matchup_career, Job_text, Resume_role, Matchup_skill, Matchup_job

class UserEmailExists(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'True'}, status=200)
            return JsonResponse({'MESSAGE':'False'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class UserRegisterView(View):
    validation = {
		'password': lambda password: re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$", password)
	}

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 이메일입니다.'}, status=401)

			# 빈 문자열 검사
            for value in data.values():
                if value == '':
                    return JsonResponse({'MESSAGE':'입력 정보를 확인해주세요'}, status=401)

			# 비밀번호 숫자, 영문, 특수문자 조합으로 6자리 이상인지 검증
            for value, validator in self.validation.items():
                if not validator(data[value]):
                    return JsonResponse({'MESSAGE':'영문자, 숫자, 특수문자 사용하여 6자 이상 입력해주세요.'}, status=401)

            User.objects.create(
                email = data['email'],
                name = data['name'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
                agreement = data['agreement'],
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class AdminRegisterView(View):
    validation = {
        'password': lambda password: re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$", password)
    }

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 이메일입니다.'}, status=401)

			# 빈 문자열 검사
            for value in data.values():
                if value == '':
                    return JsonResponse({'MESSAGE':'입력 정보를 확인해주세요'}, status=401)

			# 비밀번호 숫자, 영문, 특수문자 조합으로 6자리 이상인지 검증
            for value, validator in self.validation.items():
                if not validator(data[value]):
                    return JsonResponse({'MESSAGE':'영문자, 숫자, 특수문자 사용하여 6자 이상 입력해주세요.'}, status=401)

            User.objects.create(
                name = data['name'],
                job_position = data['job_position'],
                contact = data['contact'],
                email = data['email'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
			)
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class AdminExists(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            user = User.objects.prefetch_related('company').get(email=data['email'])
            if user.job_position or user.company:
                return JsonResponse({'MESSAGE':'True'}, status=200)
            return JsonResponse({'MESSAGE': 'False'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'False'}, status=401)
        except User.company.RelatedObjectDoesNotExist:
            return JsonResponse({'MESSAGE': 'False'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')

                    Security.objects.create(
                        user_id = user.id,
                        user_ip = request.META['REMOTE_ADDR'],
                        browser = request.META['HTTP_USER_AGENT'],
                        date = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                    )
                    return JsonResponse({'token': token.decode('utf-8')}, status=200)
                return JsonResponse({'MESSAGE':'INVALID'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE':'USER INVALID'}, status=401)

class Profile(View):
    @login_decorator
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        data = [
            {
                'id':user.id,
                'name':user.name,
                'email':user.email,
                'contact':user.contact,
                'image':user.image_url
            }
        ]
        return JsonResponse({'user_profile':data}, status=200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        user.name = data['name']
        user.email = data['email']
        user.contact = data['contact']
        user.image_url = data['image']
        user.save()
        data = [
            {
                'id':user.id,
                'name':user.name,
                'email':user.email,
                'contact':user.contact,
                'image':user.image_url
            }
        ]
        return JsonResponse({'user_profile':data}, status=200)

class LikedCompanies(View):

    @login_decorator
    def get(self, request):
        companies = Want.objects.filter(user_id=request.user.id)
        data = [
            {
                'id':want.id,
                'company_id':want.company.id,
                'name':want.company.name,
                'logo':want.company.image_url,
                'date':want.created_at
            } for want in companies
        ]
        return JsonResponse({'companies':data}, status=200)

class ResumeMainView(View):

    @login_decorator
    def get(self, request):
        user = request.user
        resumeMain = Resume.objects.filter(user_id=user.id).values('id','title', 'created_at', 'status', 'is_matchup')
        for resume in resumeMain:
            if resume['title'] == None:
                resume['title']=""
            if resume['status'] == False:
                resume['status']="작성 완료"
            else:
                resume['status']="작성 중"

        return JsonResponse({'data':list(resumeMain)}, status=200)

class ResumeView(View):

    @login_decorator
    def get(self, request):
        user = request.user
        resume = Resume.objects.create()
        resume.user_id = user.id
        resume.status = True
        resume.save()

        print(resume.id)

        data ={
                'id':resume.id,
                'user_id':user.id
        }
        return JsonResponse({'data':data}, status=200)

class UserResumeWriteView(View):

    @login_decorator
    def get(self, request, main_resume_id):
        user = request.user
        title_number = Resume.objects.filter(user_id=user.id)

        resume = Resume.objects.get(id=main_resume_id)

        def judgment(element, affiliation):
            if element == None:
                outcome=affiliation
            else:
                outcome=element
            return outcome

        resume_title = judgment(resume.title, "새로운 문서")
        resume_name = judgment(resume.name, user.name)
        resume_email = judgment(resume.email, user.email)
        resume_contact = judgment(resume.contact, user.contact)

        data = {
                'user_id':user.id,
                'resume_id':main_resume_id,
                'title':resume_title,
                'name':resume_name,
                'email':resume_email,
                'phone':resume_contact,
                'about':resume.description,
                'image':resume.image_url,
            }

        return JsonResponse({'resume':data}, status=200)

    @login_decorator
    def delete(self, request, main_resume_id):
        data = Resume.objects.get(id=main_resume_id)
        data.delete()

        return HttpResponse(status=200)

    @login_decorator
    def post(self, request, main_resume_id):
        try:
            data = json.loads(request.body)
            user = request.user

            resume = Resume.objects.get(id=main_resume_id)

            resume.id=main_resume_id
            resume.title=data['title']
            resume.name=data['name']
            resume.email=data['email']
            resume.contact=data['phone']
            resume.description=data['about']
            resume.image_url=data['image']
            resume.status=data['status']
            resume.save()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'keyerror'}, status=401)

class ResumeDetailView(View):

    @login_decorator
    def get(self, request, main_resume_id):

        category = request.GET.get('category', None)

        def classification(affiliation_method):
                class_list = affiliation_method.objects.create()
                class_list.resume_id = main_resume_id
                class_list.save()

                data={
                    'id':class_list.id,
                    'resume_id':int(main_resume_id)
                }

                return data

        if category == 'career':
            data = classification(Career)
        elif category == 'education':
            data = classification(Education)
        elif category == 'award':
            data = classification(Award)
        elif category == 'language':
            data = classification(Language)
        elif category == 'link':
            data = classification(Link)

        return JsonResponse({'data':data}, status=200)

    @login_decorator
    def delete(self, request, main_resume_id):

        data = json.loads(request.body)
        category = request.GET.get('category', None)

        def remove(kind):
            row = kind.objects.get(id=data['id'])
            row.delete()

        if category == 'career':
            remove(Career)
        elif category == 'education':
            remove(Education)
        elif category == 'award':
            remove(Award)
        elif category == 'language':
            remove(Language)
        elif category == 'link':
            remove(Link)
        return HttpResponse(status=200)

class ResumeDetailWriteView(View):

    @login_decorator
    def get(self, request, main_resume_id):
         user = request.user

         category = request.GET.get('category', None)

         def year_month(theme_set, theme):

             data=[]
             for index,element in enumerate(theme_set):
                 start_year = theme.objects.filter(resume_id=main_resume_id).values('start_year')[index]
                 start_month = theme.objects.filter(resume_id=main_resume_id).values('start_month')[index]
                 end_year = theme.objects.filter(resume_id=main_resume_id).values('end_year')[index]
                 end_month = theme.objects.filter(resume_id=main_resume_id).values('end_month')[index]
                 start = [start_year['start_year'], start_month['start_month']]
                 end = [end_year['end_year'], end_month['end_month']]

                 element['start']= start
                 element['end']= end
                 data.append(element)

             return data

         if category == 'career':
             data= []
             elements = Career.objects.filter(resume_id=main_resume_id).values('id', 'resume_id', 'is_working', 'company', 'position')
             datas = year_month(elements, Career)

             for data_list in datas:
                 result = Result.objects.filter(career_id=data_list['id']).values('id','career_id','title','content')

                 for index,element in enumerate(result):
                     start_year = Result.objects.filter(career_id=data_list['id']).values('start_year')[index]
                     start_month = Result.objects.filter(career_id=data_list['id']).values('start_month')[index]
                     end_year = Result.objects.filter(career_id=data_list['id']).values('end_year')[index]
                     end_month = Result.objects.filter(career_id=data_list['id']).values('end_month')[index]
                     start = [start_year['start_year'], start_month['start_month']]
                     end = [end_year['end_year'], end_month['end_month']]

                     element['start']= start
                     element['end']= end

                 data_list['result']=list(result)
                 data.append(data_list)

         elif category == 'award':
             data = []
             elements = Award.objects.filter(resume_id=main_resume_id).values('id','resume_id','name','content')

             for index,element in enumerate(elements):
                 year = Award.objects.filter(resume_id=main_resume_id).values('date_year')[index]
                 month = Award.objects.filter(resume_id=main_resume_id).values('date_month')[index]
                 date = [year['date_year'], month['date_month']]
                 element['date']=date
                 data.append(element)

         elif category == 'education':

             elements = Education.objects.filter(resume_id=main_resume_id).values('id','is_working','school','specialism','subject')
             data = year_month(elements, Education)

         elif category == 'language':
             data = Language.objects.filter(resume_id=main_resume_id).values()
         elif category == 'link':
             data = Link.objects.filter(resume_id=main_resume_id).values()

         return JsonResponse({'data':list(data)}, status=200)

    @login_decorator
    def post(self, request, main_resume_id):
        data = json.loads(request.body)
        user = request.user

        category = request.GET.get('category', None)

        if category == 'career':

            resumes = Resume.objects.get(id=main_resume_id)
            resumes.total_work = 0
            resumes.save()

            for index_data in data:

                careers = Career.objects.get(id=index_data['id'])
                careers.start_year = index_data['start'][0]
                careers.start_month = index_data['start'][1]
                careers.end_year = index_data['end'][0]
                careers.end_month = index_data['end'][1]
                careers.is_working = index_data['is_working']
                careers.company = index_data['company']
                careers.position = index_data['position']

                startMonth = int(index_data['start'][0])*12+int(index_data['start'][1])
                endMonth = int(insdex_data['end'][0])*12+int(index_data['end'][1])
                total_year = round((endMonth-startMonth)/12)

                resumes.total_work = resumes.total_work+total_year
                careers.save()
                resumes.save()

                for element in index_data['result']:
                    results = Result.objects.get(id=element['id'])
                    results.title = element['title']
                    results.content = element['content']
                    results.start_year = element['start'][0]
                    results.start_month = element['start'][1]
                    results.end_year = element['end'][0]
                    results.end_month = element['end'][1]
                    results.end = element['end']
                    results.save()

            if resumes.total_work<0 or resumes.total_work>100:
                resumes.total_work = 0
                resumes.save()

        elif category == 'award':
            for index_data in data:
                awards = Award.objects.get(id=index_data['id'])
                awards.date_year = index_data['date'][0]
                awards.date_month = index_data['date'][1]
                awards.name = index_data['name']
                awards.content = index_data['content']
                awards.save()

        elif category == 'education':
            for index_data in data:
                educations = Education.objects.get(id=index_data['id'])
                educations.start_year = index_data['start'][0]
                educations.start_month = index_data['start'][1]
                educations.end_year = index_data['end'][0]
                educations.end_month = index_data['end'][1]
                educations.end = index_data['end']
                educations.is_working = index_data['is_working']
                educations.school = index_data['school']
                educations.specialism = index_data['specialism']
                educations.subject = index_data['subject']
                educations.save()

        elif category == 'language':
            for index_data in data:
                 languages = Language.objects.get(id=index_data['id'])
                 languages.lingustic_id = index_data['lingustic_id']
                 languages.level_id = index_data['level_id']
                 languages.save()

        elif category == 'link':
            for index_data in data:
                links = Link.objects.get(id=index_data['id'])
                links.url = index_data['link']

        return HttpResponse(status=200)

class CareerResultView(View):

    @login_decorator
    def get(self, request, main_career_id):

        results = Result.objects.create()
        results.career_id = main_career_id
        results.save()

        data={
            'id':results.id,
            'career_id':int(main_career_id)
        }

        return JsonResponse({'data':data}, status=200)

    @login_decorator
    def delete(self, request, main_career_id):

        row = Result.objects.get(id=data['id'])
        row.delete()

        return HttpResponse(status=200)

# class CompanyRequestsResume(View):
#     @login_decorator
#     def get(self, request):
#         matchup = Matchup.objects.get(user_id=request.user.id)
#         requests_resume = Company_matchup.objects.filter(matchup_id=matchup.id)
#         data = [
#             {
#                 'name':request.company.name,
#                 'logo':request.company.image_url,
#                 'date':request.created_at
#             } for request in requests_resume
#         ]
#         return JsonResponse({'is_resume_request':data}, status=200)

# class CompanyInterviewResume(View):
#     @login_decorator
#     def get(self, request):
#         matchup = Matchup.objects.get(user_id=request.user.id)
#         interviews = Proposal.objects.filter(matchup_id=matchup.id)
#         data = [
#             {
#                 'name':interview.company.name,
#                 'logo':interview.company.image_url,
#                 'date':interview.created_at
#             } for interview in interviews
#         ]
#         return JsonResponse({'is_resume_request':data}, status=200)

class UserMatchUpView(View):
    @login_decorator
    def get(self, request):
        speclist=[]
        user_career = Job_category.objects.prefetch_related('role_set')
        user_year = Matchup_career.objects.all().values()
        for career in user_career:
            title = {'id':career.id, 'name':career.name}
            lists = list(career.role_set.values('id','name'))
            speclists={'title':title}
            speclists['lists']=lists
            speclist.append(speclists)
        year = []
        for years in user_year:
            year.append(years)

        return JsonResponse({'speclist':speclist,'year':year}, status=200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        resume_professional = Resume.objects.get(id=data['resume_id'])
        resume_professional.job_category_id = data['job_category']
        resume_professional.matchup_career_id = data['matchup_career']
        resume_professional.income = data['income']
        resume_professional.save()

        for role in data['role']:
            resume_role = Resume_role.objects.create()
            resume_role.resume_id = data['resume_id']
            resume_role.role_id = role
            resume_role.save()

        for sk in data['skill']:
            matchup_skill = Matchup_skill.objects.create()
            matchup_skill.resume_id = data['resume_id']
            matchup_skill.skill = sk
            matchup_skill.save()

        return HttpResponse(status=200)

class UserMatchUpDetailView(View):
    @login_decorator
    def get(self, request):
        data = json.loads(request.body)
        print(data)
        if Resume.objects.filter(id=data['resume_id']).exists():
            resume_infor = Resume.objects.select_related('job_category').prefetch_related('resume_resume_role').prefetch_related('matchup_skill_set').get(id=data['resume_id'])

            data ={
                'job_category':resume_infor.job_category.name,
                'role':[infor['name'] for infor in resume_infor.resume_resume_role.values('name')],
                'income':resume_infor.income,
                'skill':[infor['skill'] for infor in resume_infor.matchup_skill_set.values('skill')]
            }
            return JsonResponse({'data':data}, status=200)
        else:
            data={
                'job_category':"",
                'role':[],
                'income':"",
                'skill':[]
            }
            return JsonResponse({'data':data}, status=200)

class UserMatchUpResumeView(View):
    @login_decorator
    def get(self, request, main_resume_id):
        mainResume=Resume.objects.prefetch_related('education_set').prefetch_related('career_set').get(id=main_resume_id)

        if len(mainResume.education_set.values())!=0:
            if mainResume.education_set.values()[0]['school']==None or mainResume.education_set.values()[0]['school']=="":
                school = '학교 미입력'
            else:
                school = mainResume.education_set.values()[0]['school']

            if mainResume.education_set.values()[0]['specialism']==None or mainResume.education_set.values()[0]['specialism']=="":
                specialism = '전공 미입력'
            else:
                specialism = mainResume.education_set.values()[0]['specialism']
        else:
            school="학교 미입력"
            specialism="전공 미입력"

        if len(mainResume.career_set.values())!=0:
            if mainResume.career_set.values()[0]['company']==None or mainResume.career_set.values()[0]['company']=="":
                company = '직장 미입력'
            else:
                company = mainResume.career_set.values()[0]['company']
            if mainResume.career_set.values()[0]['position']==None or mainResume.career_set.values()[0]['position']=="":
                position = '직책 미입력'
            else:
                position = mainResume.career_set.values()[0]['position']
        else:
            company = '직장 미입력'
            position = '직책 미입력'

        if mainResume.description==None or mainResume.description=="":
            description="자기소개 미입력"
        else:
            description=mainResume.description
        data =[
            {
                'resume_id':mainResume.id
            },
            {
             'user_school':
                {
                    'school':school,
                    'specialism':specialism
                }
            },
            {
                'user_career':
                {
                    'company':company,
                    'position':position
                }
            },
            {
                'description':description
            }

        ]

        return JsonResponse({'data':data}, status=200)

class MatchupJobTextView(View):
    def get(self, request):
        job_text = Job_text.objects.all().values('id', 'is_working', 'text')

        return JsonResponse({'data':list(job_text)}, status=200)

class UserUpdateView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        userInfor = User.objects.get(id=user.id)

        if userInfor.contact==None:
            contact=""
        else:
            contact=userInfor.contact

        data ={
            'name':userInfor.name,
            'email':userInfor.email,
            'contact':contact,
            'country_id':userInfor.country_id
        }

        return JsonResponse({'data':data}, status=200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        userInfor = User.objects.get(id=user.id)
        userInfor.name = data['name']
        userInfor.email = data['email']
        userInfor.contact = data['contact']
        userInfor.country_id = data['country_id']

        userInfor.save()

        return HttpResponse(status = 200)

class UserGlobalView(View):
    def get(self, request):
        country = Country.objects.all().values('id', 'name', 'number')

        return JsonResponse({'data':list(country)}, status=200)

class MatchUpRegistrationView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        if Resume.objects.filter(is_matchup=True).exists():
            non_matchup_resume = Resume.objects.get(is_matchup=True)
            non_matchup_resume.is_matchup=False

        matchupResume = Resume.objects.get(id=data['resume_id'])
        matchupResume.is_matchup=True
        matchupResume.save()

        if Matchup_job.objects.filter(resume_id=data['resume_id']).exists():
            matchupjob = Matchup_job.objects.get(resume_id=data['resume_id'])
        else:
            matchupjob = Matchup_job.objects.create()
            matchupjob.resume_id = data['resume_id']
        matchupjob.job_text_id = data['job_text']
        matchupjob.save()

        return HttpResponse(status = 200)

def get_reward_currency(position_id):
            position=Position.objects.get(id=position_id)
            currency=position.country.english_currency
            reward=format(position.total, ',')

            if position.country.id==3 or position.country.id==4 or position.country.id==6:
                total_reward=reward+currency
                return total_reward
            else:
                total_reward=currency+reward
                return total_reward

class UserBookmark(View):
    @login_decorator
    def get(self, request):
        position_list=Position.objects.filter(bookmark__user_id=request.user.id)
        is_bookmarked=[{
            'image':position.company.image_set.first().image_url,
            'name':position.name,
            'company':position.company.name,
            'country':position.country.name,
            'city':position.city.name if position.city else None,
            'reward':get_reward_currency(position.id)
        }for position in position_list]

        return JsonResponse({'bookmark':is_bookmarked}, status=200)
