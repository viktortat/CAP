from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BillTest(models.Model):
	class Meta():
		db_table = 'billtest'
		verbose_name = "Тест"
		verbose_name_plural = "Тесты"
		
	TIME_T = (
		('ONE_T', 'Доступно всем каждые 24 часа'),
		('TWO_T', '30 секунд + 0.15 руб.'),
	)
	
	VID_T = (
		('ONE_T', 'Нет'),
		('TWO_T', 'Выделить тест среди других + 0.02 руб.'),
	)
	
	AIDIT = (
		('VSE', 'Все пользователи'),
		('ONE_TWO', '1/2 польователей'),
		('ONE_THREE', '1/3 польователей'),
		('ONE_FOUR', '1/4 польователей'),
		('MEDL', 'Очень медленный серфинг'),
		('SUPM', 'Супер медленный серфинг'),
		('CHEREP', 'Черепаший серфинг'),
	)
	
	PO_ROD = (
		('VSEPOLZOV', 'Все пользователи'),
		('UCH', 'Учится в школе'),
		('STUDENT', 'Студент'),
		('PRED', 'Предприниматель'),
		('RAB_P', 'Работники на предприятиях'),
		('SLUG_P', 'Служащие на предприятиях'),
		('BOMR', 'Без основного места работы'),	
	)
	
	PO_FAMALY = (
		('MARRIED', 'Женат\замужем, есть дети'),
		('MARRIEDS', 'Женат\замужем, нет детей'),
		('NOMARRIED', 'Не женат\Не замужем, есть дети'),
		('NOMARRIEDS', 'Не женат\Не замужем, нет детей'),
		('DIVORCED', 'Разведен\разведена, есть дети'),
		('DIVORCEDS', 'Разведен\разведена, нет детей'),
	)
	
	PO_SEX = (
		('MEN_SEX', 'Мужчина'),
		('WOOMEN_SEX', 'Женщина'),
	)
	
	PO_AGE = (
		('LUB_AGE', 'Любой возраст'),
		('SIXT_AGE', 'От 16 до 18'),
		('EIGHT_AGE', 'От 18 до 20'),
		('TWENT_AGE', 'От 20 до 25'),
		('TWENTF_AGE', 'От 25 до 30'),
		('THIRT_AGE', 'От 30 до 40'),
		('FORTY_AGE', 'От 40 до 50'),
		('FIVETY_AGE', 'От 50 до 70'),
	)
	
	user = models.ForeignKey('auth.User')	
	title = models.CharField("Заголовок теста", max_length=50)
	opisan = models.TextField("Инструкции для тестирования", max_length=1000)	
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	url_admin = models.URLField("Укажите, (URL) вы представляете в задании. (максимум 200 символов)", blank = True)
	price = models.FloatField("Вознаграждение исполнителю", default=0.4)
	price_test = models.FloatField("Укажите сумму баланса теста", default=0)
	time_t = models.CharField("Технология тестирования", 
							max_length=30, choices=TIME_T, default="Выбор")
	
	price_u = models.FloatField("Вознограждение пользователю", default=0)
	price_s = models.FloatField("Вознограждение сайту", default=0)
	price_t = models.FloatField("Списание с баланса теста", default=0)
	vid_t = models.CharField("Выделить тест среди других", 
							max_length=30, choices=VID_T, default="Выбор")
	'''audit = models.CharField("Аудитория смотрящих",
							max_length=10, choices=AIDIT, default="Выбор")'''
	quest_1 = models.CharField("Содержание вопроса №1", max_length=300)
	quest_1_ans_1 = models.CharField("Вариант ответа №1", max_length=30)
	quest_1_ans_2 = models.CharField("Вариант ответа №2", max_length=30)
	quest_1_ans_3 = models.CharField("Вариант ответа №3", max_length=30)
	quest_2 = models.CharField("Содержание вопроса №2", max_length=300)
	quest_2_ans_1 = models.CharField("Вариант ответа №1", max_length=30)
	quest_2_ans_2 = models.CharField("Вариант ответа №2", max_length=30)
	quest_2_ans_3 = models.CharField("Вариант ответа №3", max_length=30)
	quest_3 = models.CharField("Содержание вопроса №3", max_length=300)
	quest_3_ans_1 = models.CharField("Вариант ответа №1", max_length=30)
	quest_3_ans_2 = models.CharField("Вариант ответа №2", max_length=30)
	quest_3_ans_3 = models.CharField("Вариант ответа №3", max_length=30)
	var_one = models.IntegerField("Укажите номер ответа на вопрос №1", default=1)
	var_two = models.IntegerField("Укажите номер ответа на вопрос №2", default=1)
	var_three = models.IntegerField("Укажите номер ответа на вопрос №3", default=1)
	'''porod = models.CharField("По роду деятельности",
							max_length=10, choices=PO_ROD, default="Выбор")
	pofamaly = models.CharField("По семейному положению",
							max_length=10, choices=PO_FAMALY, default="Выбор")
	posex = models.CharField("По половому признаку",
							max_length=10, choices=PO_SEX, default="Выбор")
	poage = models.CharField("По возрасту",
							max_length=10, choices=PO_AGE, default="Выбор")'''
	prosm = models.IntegerField("Количество выполнений", default=0 )
	prosm_ost = models.IntegerField("Количество выполнений осталось", default=0 )
	spis = models.BooleanField("Списание с 11р.", default=False)
	sum_spis = models.IntegerField("Сумма для списания", default=0 )
	com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
	moder = models.BooleanField("Модерация", default=False)
	odobren = models.BooleanField("Одобраить", default=False)
	pausa = models.BooleanField("Пауза", default=False)
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=True)
	
	def __str__(self):
		return self.title
	