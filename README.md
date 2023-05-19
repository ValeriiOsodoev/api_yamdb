<h1>Автор</h1>
<p>Анна Котова, Валерий Осодоев, Валерия Федорова</p>

<h1>Описание</h1>
<p></p>

<h1>Установка</h1>
<p>Для начала работы с проектом, необходимо:</p>

<p>Клонировать репозиторий и перейти в него в командной строке:</p>

<p>git@github.com:ValeriiOsodoev/api_yamdb.git</p>
<p>cd api_yamdb</p>
<p>Cоздать и активировать виртуальное окружение:</p>

<p>python -m venv venv</p>
<p>source venv/Scripts/activate</p>

<p>Установить зависимости из файла requirements.txt:</p>

<p>python -m pip install --upgrade pip</p>
<p>pip install -r requirements.txt</p>

<p>Для работы с JWT установить библиотеки Djoser и Simple JWT:</p>

<p>pip install djoser djangorestframework-simplejwt==4.7.2</p>

<p>Установить библиотеку django-filter</p>

<p>pip install django-filter</p>

<p>Выполнить миграции:</p>

<p>python manage.py migrate</p>

<p>Запустить проект:</p>

<p>python manage.py runserver</p>