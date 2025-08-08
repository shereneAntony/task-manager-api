# task-manager-api

A RESTful API for managing projects, tasks, and user assignments. Built with Django REST Framework, supporting task filtering, sorting, pagination, and notifications.

Features:-

1.Create, read, update, and delete projects and tasks.

2.Assign tasks to users.

3.Filter, sort, and paginate tasks.

4.Send notifications on task updates.

5.Handle background jobs (e.g., reminders, status updates).




Tech Stack:-

1.Backend: Django, Django REST Framework

2.Database: MySQL

3.Background Jobs: Celery + Redis/Memurai

4.Authentication: Token-based




Setup Instructions:-

1. Install python,django,mysqlclient, rest framework, django filters,etc.
2. Create django project and app.
3. For background tasks install celery and redis (to handle email transmission).
4. Use JWT Token for authorization.






Database Schema:-
1. Project Model
  #	Name	        Type	
	1	id Primary	  bigint(20)			
	2	name	        varchar(100)		
	3	description	  longtext			
	4	created_at	  datetime(6)			
	5	updated_at	  datetime(6)			
	6	created_by_id Index	int(11)		


2. Task Model

  #	Name	       Type	
	1	id Primary	 bigint(20)				
	2	title	       varchar(100)			
	3	description	 longtext			
	4	status	     varchar(20)		
	5	priority	   int(11)		
	6	due_date	   date			
	7	created_at	 datetime(6)			
	8	updated_at	 datetime(6)			
	9	assigned_to_id Index	int(11)			
	10	project_id  Index	bigint(20)	
 
 
 
 
 
 
 Celery setup:-
 
 1. Install Celery
 2. Create and configure Celery app (e.g., in celery.py).
 3. Define tasks using  @shared_task.
 4. Run the worker (celery -A your_project_name worker --loglevel=info).
 5. Send tasks asynchronously using task.delay() or task.apply_async().

 

