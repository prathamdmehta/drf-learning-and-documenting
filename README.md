DRF Learning and Documenting
This repository is a personal learning playground for Django REST Framework (DRF).
The goal is to build small APIs, try different DRF features, and document the code with clear comments so it can be used as a reference later.

Project Goals
Learn how to build APIs using Django REST Framework.

Practice different types of views: function-based, class-based, mixins, generics, and viewsets.

Experiment with serializers, including nested serializers for related models.

Understand pagination (default, global, and custom pagination classes).

Keep the code well-commented so it works like a mini DRF guide.

Features Implemented
1. Basic Django Setup
Django project initialized with DRF installed and configured.

Apps created for different learning areas (for example: students, employees, blogs, api).
​

2. Function-Based Views (Students)
Simple function-based API views for Student:

List and create students.

Retrieve, update, and delete a single student.

Good for understanding the most basic way to build APIs before moving to class-based views.
​

3. Class-Based Views (Employees)
APIView-based views for Employee:

Employees for list and create.

EmployeeDetail for retrieve, update, and delete.

Shows how to manually handle HTTP methods (get, post, put, delete) while still using DRF tools like serializers and Response.
​

4. Mixins + GenericAPIView (Employees)
Uses DRF mixins such as:

ListModelMixin, CreateModelMixin

RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

Combined with GenericAPIView to reduce boilerplate while keeping control over URLs and methods.
​

5. Generic Class-Based Views
Uses high-level generic views:

ListCreateAPIView

RetrieveUpdateDestroyAPIView

Implemented for resources like Employee and Blog to show how much code DRF can generate for standard CRUD patterns.

6. ViewSets and Routers
EmployeeViewset demonstrates:

list, create, retrieve, update, delete methods.

DefaultRouter is used in urls.py to auto-generate RESTful endpoints:

/employees/

/employees/<pk>/

This section shows how ViewSets + Routers can quickly build a full API with fewer explicit URL patterns.

7. Nested Serializers (Blogs and Comments)
Models: Blog and Comment with a one-to-many relationship (a blog has many comments).

CommentSerializer serializes individual comments.

BlogSerializer uses a nested serializer:

python
comments = CommentSerializer(many=True, read_only=True)
This returns a blog along with all its related comments in one response, which is useful for learning about relationships and nested data structures in DRF.

Views used:

BlogsView (ListCreateAPIView)

BlogDetailView (RetrieveUpdateDestroyAPIView)

Similar views for Comment.

8. Custom Pagination
CustomPagination class based on PageNumberPagination:

Custom query params (page-num, page_size).

Custom response structure with next, previous, count, page_size, and results.

Demonstrates how to:

Control page size.

Limit maximum page size.

Customize the pagination response returned to the client.

Tech Stack
Backend Framework: Django, Django REST Framework.
​

Language: Python.

Database: SQLite (for learning and quick setup).

Version Control: Git and GitHub.

How to Run the Project
Clone the repository

bash
git clone https://github.com/<your-username>/drf-learning-and-documenting.git
cd drf-learning-and-documenting
Create and activate a virtual environment

bash
python -m venv env
source env/bin/activate      # On macOS/Linux
# or
env\Scripts\activate        # On Windows
Install dependencies

bash
pip install -r requirements.txt
Apply migrations

bash
python manage.py migrate
Run the development server

bash
python manage.py runserver
Open the API in your browser

Go to http://127.0.0.1:8000/ and explore the different endpoints (students, employees, blogs, comments, etc.).

Learning Roadmap (What This Repo Covers)
Step 1: Basic Django + DRF setup.

Step 2: Function-based views for simple APIs.

Step 3: Class-based views using APIView.

Step 4: Mixins + GenericAPIView.

Step 5: Generic class-based views.

Step 6: ViewSets and Routers.

Step 7: Nested serializers (Blog–Comment relationship).

Step 8: Global and custom pagination.

Each step is committed with messages that explain what was added, so you can go through the Git history to see the progression.

How to Use This Repo for Learning
Read the code and comments in each app.

Run the server and hit endpoints with a tool like Postman, HTTPie, or the DRF browsable API.
​

Experiment:

Change serializers (e.g., make the nested serializer writable).

Modify pagination settings.

Add new fields or models and extend existing views.

Future Ideas
Add authentication and permissions.

Add filtering, searching, and ordering.

Add Swagger/OpenAPI documentation.

Write tests for views and serializers.
