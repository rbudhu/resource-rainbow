# Resource Rainbow
Resource Rainbow helps visually identify workload issues within your team, office, and company.

![Screenshot](http://i.imgur.com/fUNTDbp.png)

## Introduction

Resource Rainbow is a self-deployable webapp that allows team leaders to visually identify overworked and underworked staff members.
Staff can update their status on a regular basis and keep a history of their workload.  Team leaders can easily search for staff by name or by skillset
and visually identify overworked, underworked, and "just right" employees, organize them into work groups, and perform the necessary resource load balancing.

## Why?

In some industries, like the defense industry, employees work on various contracts.  In some cases, employees work on multiple
contracts and can quickly become overworked.  In other cases, employees are "undercovered" or do not have enough work to fulfill
their weekly hourly quota.  It is sometimes difficult to determine employees who are underworked but have the skillsets to alleviate
some of the workload from the overworked personnel.  It is also difficult to tell the workload coverage of each member of a team.
Resource Rainbow was developed to solve these problems.

## Potential Use Case

Have team members update their Resource Rainbow status daily as part of a scrum activity.  Team lead monitors aggregate workgroup workload as well as individual workload to perform task scoping or resource balancing.

## Features

* Search for users by username, name, skillset
* Create workgroups and add users to workgroups
* Get aggregated workgroup workload status (i.e. the mode of the statuses of all members of a workgroup)
* Track user workload status history per day per user

## Dependencies

Examine the requirements.txt. If you use pip/virtualenv, just pip install -r requirements.txt


## Forking and Testing

Fork on GitHub: https://github.com/rbudhu/resource-rainbow

Generate test user data by:

    export DJANGO_SETTINGS_MODULE=resource_rainbow.settings
    cp test/user-gen.py ../
    python user-gen.py
    

# Building

*Optional*: If you have virtualenv then create your desired environment.

    pip install -r requirements.txt
    cd resource_rainbow
    python manage.py migrate
    python manage.py loaddata web/initial_data.json


# Running

    cd resource_rainbow
    python manage.py runserver
