import json
import random
import datetime

from django.http            import JsonResponse, HttpResponse
from django.views           import View
from django.db.models       import Q
from django.core.exceptions import ObjectDoesNotExist

from utils                  import login_decorator, login_check
from company.models         import Company, City, Foundation_year, Employee, Industry, Workplace, Position, \
                                Role, Position_workplace, Country, Tag, Company_tag, Bookmark, Image, Volunteers, Like , Theme
from user.models            import User, Matchup, Work_information, Matchup_skill

class CompanyRegister(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		print(data)
		try:
			user = request.user
			print(user.id)
			Company(
                user_id = user.id,
                name = data['name'],
                registration_number = data['registration_number'],
                revenue = data['revenue'],
                industry = Industry.objects.get(name=data['industry']),
                employee = Employee.objects.get(number=data['employee']),
                description = data['description'],
                foundation_year = Foundation_year.objects.get(name=data['foundation_year']),
                email = data['email'],
                contact_number = data['contact_number'],
                website = data['website'],
                keyword = data['keyword'],
                recommender = data['recommender'],
                image_url = data['image_url']
			).save()

			Workplace.objects.create(
                company_id = Company.objects.get(user_id=user.id).id,
                city = City.objects.get(name=data['city']),
                address = data['address'],
                lat = data['lat'],
                lng = data['lng'],
                represent = data['represent']
            )
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

	@login_decorator
	def get(self, request):
		user = request.user
		company = Company.objects.get(user_id=user.id)
		workplace = Workplace.objects.get(company_id=company.id)
		data = [
			{
				'name':company.name,
				'description':company.description,
				'website':company.website,
				'workplace':workplace.address,
                'city':workplace.city.name,
                'country':workplace.city.country.name,
                'registration_number':company.registration_number,
				'revenue':company.revenue,
				'industry':company.industry.name,
				'employee':company.employee.number,
				'foundation_year':company.foundation_year.name,
				'email':company.email,
				'contact_number':company.contact_number,
				'keyword':company.keyword,
				'image_url':company.image_url
			}
		]
		return JsonResponse({'company':data}, status=200)

class CompanyPosition(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		try:
			print(data)
			user = request.user
			company = Company.objects.get(user_id=user.id)
			is_entry_min = 0 if data['entry']==True else data['min_level']
			is_entry_max = 1 if data['entry']==True else data['max_level']
			is_always = None if data['always']==True else data['expiry_date']
			is_preferred = None if data['preferred']==True else data['preferred']

			Position.objects.create(
				company = company,
				role = Role.objects.get(name=data['role']),
				min_level = is_entry_min,
				max_level = is_entry_max,
				entry = data['entry'],
				mim_wage = data['mim_wage'],
				max_wage = data['mim_wage'],
                expiry_date = is_always,
				always = data['always'],
				workplace = Workplace.objects.get(company_id=company.id),
				name = data['name'],
				description = data['description'],
				responsibility = data['responsibility'],
				qualification = data['qualification'],
				preferred = is_preferred,
				benefit = data['benefit'],
				referrer = data['referrer'],
				volunteer = data['volunteer'],
				total = data['total']
			)
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class PositionList(View):
    @login_decorator
    def get(self, request):
        user = request.user
        company = Company.objects.get(user_id=user.id)
        positions = Position.objects.filter(company_id=company.id)
        data = [
                {
                    'name':position.name,
                    'expiry_date':position.expiry_date if position.expiry_date else position.always,
                } for position in positions
                ]
		
        return JsonResponse({'company':data}, status=200)

class LikedMatchupResume(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'matchup_id' in data:
                matchup_id = data['matchup_id']
                matchup = Matchup.objects.get(id=matchup_id)
                company = Company.objects.get(user_id=request.user.id)
                if Like.objects.filter(company_id=company.id, matchup_id=matchup_id, status=True).exists():
                    like = Like.objects.get(company_id=company.id, matchup_id=matchup_id, status=True)
                    like.status = False
                    like.save()
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                Like.objects.create(
                    company_id=company.id,
                    matchup_id=matchup_id,
                    status = True
                )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class LikedMatchupList(View):
    @login_decorator
    def get(self, request):
        try:
            user = request.user
            company = Company.objects.get(user_id=user.id)
            likes = Like.objects.filter(company_id=company.id, status=True)
            for like in likes:
                matchup = Matchup.objects.prefetch_related('matchup_skill_set','work_information_set').get(user_id=like.matchup.user.id)
                data = [
                    {
                        'id':like.user.id,
                        'name':like.matchup.user.name,
                        'description':like.matchup.description,
                        'role':like.matchup.role.name,
                        'career':like.matchup.matchup_career.year,
                        'work_info':[{work.name:[work.start, work.end]} for work in matchup.work_information_set.filter(matchup_id=matchup.id)],
                        'work_skills':[work.skill for work in matchup.matchup_skill_set.filter(matchup_id=matchup.id)],
                        'education':like.matchup.school,
                    }
                ]
                return JsonResponse({'liked_matchup':data}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)

class UnreadMatchup(View):
    @login_decorator
    def get(self, request):
        matchup = Matchup.objects.prefetch_related('matchup_skill_set','work_information_set') 
        data = [
            {
                'id':match.user.id,
                'user':match.user.name,
                'role':match.role.name,
                'career':match.matchup_career.year,
                'description':match.resume.description if match.resume.status == True else match.description,
                'skills':list(Matchup_skill.objects.filter(matchup_id=match.id).values('id', 'skill')),
                'work_info':list(Work_information.objects.filter(matchup_id=match.id).values('id', 'name', 'start', 'end', 'is_working')),
                'education':match.school
            } for match in matchup
        ]
        return JsonResponse({'unlead_matchup':data}, status=200)

class DetailView(View):
    @login_check
    def get(self, request, position_id):
        RECOMENDATION_LIMIT=8
        
        try: 
            user_id=request.user.id
        except:
            user_id=None
        
        position = Position.objects.select_related('company', 'role').prefetch_related('position_workplace_set').get(id=position_id)
        workplace =  position.position_workplace_set.get().workplace
        position_list = [{
            'detail_images':[image.image_url for image in position.company.image_set.all()],
            'name':position.name,
            'company':position.company.name,
            'city':workplace.city.name if workplace.city else None,
            'country':workplace.country.name,
            'tag':[tag_list.tag.name for tag_list in position.company.company_tag_set.all()],
            'bookmark':Bookmark.objects.filter(Q(user_id=user_id) & Q(position_id=position_id)).exists(),
            'reward' :{
                'referrer':position.referrer,
                'volunteer':position.volunteer,
            },
            'body':{
                'description':position.description,
                'main_task':position.responsibility,
                'qualification':position.qualification,
                'preffered':position.preferred,
                'benefit':position.benefit
            },
            'info':{
                'always':{
                    'value':position.always,
                    'expiry_date':position.expiry_date
                },
                'location':{
                    'full_location':workplace.address,
                    'lat':workplace.lat,
                    'lng':workplace.lng,
                },
                'company':{
                    'image':position.company.image_url,
                    'name':position.company.name,
                    'industry_name':position.company.industry.name
                }
            },
            'recommendation':[{
                'id':item.id,
                'image':item.company.image_set.all().first().image_url,
                'name':item.name,
                'company':item.company.name,
                'location':item.position_workplace_set.get().workplace.city.name if item.position_workplace_set.get().workplace.city else None,
                'country':item.position_workplace_set.get().workplace.country.name,
                'reward':item.total
                }for item in Position.objects.order_by('?') if item.role.job_category_id==position.role.job_category_id][:RECOMENDATION_LIMIT]
            }]
        return JsonResponse({'position':position_list}, status=200)

class PositionBookmarkView(View):
    @login_decorator
    def post(self, request, position_id):
        try:
            if Bookmark.objects.filter(Q(user_id=request.user.id) & Q(position_id=position_id)).exists():
                Bookmark.objects.filter(Q(user_id=request.user.id) & Q(position_id=position_id)).delete()
                return HttpResponse(status=200)
            Position.objects.get(id=position_id).bookmarks.add(User.objects.get(id=request.user.id))
            return HttpResponse(status=200)
        
        except Position.DoesNotExist:
            return JsonResponse({'message':'INVALID_POSITION'}, status=400)

class PositionApplyView(View):
    @login_decorator
    def get(self, request, position_id):
        user_id=request.user.id
        
        user=User.objects.prefetch_related('resume_set').filter(user_id=user_id)
        apply_info:{
            'name':user.name,
            'email':user.email,
            'resume':[{
                'title':resume.title,
                'created_at':resume.created_at,
                'status':True if status==1 else False
            }for resume in user.resume_set.all()]
        }
        return JsonResponse({'apply_info':apply_info}, status=200)
    
    @login_decorator
    def post(self, request, position_id):
        user_id=request.user.id
        
        Volunteers.objects.create(
            position_id=position_id,
            user_id=request.user.id,
        )
        return HttpResponse(status=200)

class ThemeTop(View):
    
    def get(self,request,theme_id):
        
        themes = Theme.objects.get(id=theme_id)
        
        themetop = {
			"theme_title"             : themes.title,
            "theme_description"       : themes.description,
            "theme_inner_image"       : themes.inner_image_url,
            "theme_inner_description" : themes.inner_description,
		}
        
        return JsonResponse({"theme_top" : themetop},status=200)

class ThemeList(View):
    
    def get(self,request,theme_id):
        
        offset = int(request.GET.get('offset'))
        limit  = int(request.GET.get('limit'))
        themes = Position.objects.filter(theme_id=theme_id)

        themelist = [{
            "item_id"       : position.id,
            "item_image"    : Image.objects.filter(company_id=position.company.id)[0].image_url,
			"item_title"    : position.name,
            "item_company"  : position.company.name,
            "item_location" : Workplace.objects.filter(company_id=position.company.id)[0].city.name,
            "item_country"  : Workplace.objects.filter(company_id=position.company.id)[0].city.country.name,
            "item_reward"   : position.total
		} for position in themes[offset:offset + limit-1]]
        
        return JsonResponse({"theme_list":themelist},status=200)

class HomeView(View):

    @login_check
    def get(self,request):
        
        user = request.user
        roles = Matchup.objects.get(user_id=user.id) if Matchup.objects.filter(user_id=user.id).exists() else None
        mathced_position = Position.objects.filter(role_id=roles.role_id) if roles != None else None
        themes = Theme.objects.prefetch_related('position_set').all()
        
        user_recomended_position = [{
			"item_id"       : position.id,
            "item_image"    : position.company.image_set.all().first().image_url,
            "item_name"     : position.name,
            "item_company"  : position.company.name,
            "item_location" : position.position_workplace_set.get().workplace.city.name,
            "item_country"  : position.position_workplace_set.get().workplace.city.country.name,
            "item_reward"   : position.total,
		}for position in mathced_position if position.role.job_category_id == roles.role.job_category_id][:4] if roles != None else None
        
        new_employment = [{
			"item_id"       : position.id,
            "item_image"    : position.company.image_set.all().first().image_url,
            "item_name"     : position.name,
            "itme_company"  : position.company.name,
            "item_location" : position.position_workplace_set.get().workplace.city.name,
            "item_country"  : position.position_workplace_set.get().workplace.city.country.name,
            "item_reward"   : position.total,
		}for position in Position.objects.order_by('created_at')[:4]]
        
        theme_list = [{
            "item_image"    : theme.image_url,
            "item_title"    : theme.title,
            "item_desc"     : theme.description,
            "item_logos"    : list(set([logos.company.image_url for logos in theme.position_set.all()]))
		}for theme in themes[:4]]
        
        recommendations_of_the_week = [{
            "item_image"    : recommend.company.image_set.all().first().image_url,
            "item_name"     : recommend.name,
            "item_company"  : recommend.company.name,
            "item_location" : recommend.position_workplace_set.get().workplace.city.name if recommend.position_workplace_set.get().workplace.city else None,
            "item_country"  : recommend.position_workplace_set.get().workplace.city.country.name if recommend.position_workplace_set.get().workplace.city else None,
            "item_reward"   : recommend.total,
		}for recommend in Position.objects.order_by('?')if recommend.created_at.isocalendar()[1] == datetime.date.today().isocalendar()[1]][:4]
        
        return JsonResponse({"position_recommend"  : user_recomended_position,
                             "new_employment"      : new_employment,
                             "theme_list"          : theme_list,
                             "Recommendation_week" : recommendations_of_the_week
                            },status=200)