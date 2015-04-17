# Resource Rainbow
Resource Rainbow helps visually identify workload issues within your team, office, and company.

## Introduction

Resource Rainbow is a self-deployable webapp that allows team leaders to visually identify overworked and underworked staff members.
Staff can update their status on a regular basis and keep a history of their workload.  Team leaders can easily search for staff by name or by skillset
and visually identify overworked, underworked, and "just right" employees, organize them into work groups, and perform the necessary resource load balancing.

## Why?

In some industries, like the defense industry, employees work on various contracts.  In some cases, employees work on multiple
contracts and can quickly become overworked.  In other cases, employees are "undercovered" or do not have enough work to fulfill
their weekly hourly quota.  It isdifficult to ascertain employees who were underworked but had the skillsets that could alleviate
some of the workload from the overworked personnel.  It is also difficult to tell the workload coverage of each member of a team.
Resource Rainbow was developed to solve these problems.

## Dependencies

Examine the requirements.txt. If you use pip/virtualenv, just pip install -r requirements.txt


## Forking and Testing

Fork on GitHub: https://github.com/rbudhu/resource-rainbow

You can run tools/user-gen.py to generate random users (make sure to set your DJANGO_SETTINGS_MODULE=resource_rainbow.settings environment variable)

# Building

*Optional*: If you have virtualenv then create your desired environment.

    pip install -r requirements.txt
    cd resource_rainbow
    python manage.py migrate
    python manage.py loaddata web/initial_data.json


# Running

    cd resource_rainbow
    python manage.py runserver
