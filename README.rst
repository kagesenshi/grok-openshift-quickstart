=====================
Grok on OpenShift!
=====================

Grok is a web application framework for Python developers. It is aimed at both
beginners and very experienced web developers. Grok has an emphasis on agile
development. Grok is easy and powerful.

You will likely have heard about many different web frameworks for Python as
well as other languages. Why should you consider Grok?

* Grok offers a lot of building blocks for your web application.
* Grok is informed by a lot of hard-earned wisdom.

Grok accomplishes this by using at its core the Zope Toolkit (ZTK), an
advanced object-oriented set of libraries intended for reuse by web
frameworks. While Grok uses the Zope Toolkit, and benefits a lot from
it, you can get started with Grok without any special knowledge of the
ZTK.

Visit http://grok.zope.org to learn more.

Running on OpenShift
=====================

Create an account at http://openshift.redhat.com/

Create a DIY application::
  
  rhc app create -a grok -t diy-0.1

Add this upstream Plone repo::
  
  cd grok
  git remote add upstream -m master git@github.com:kagesenshi/grok-openshift-quickstart
  git pull -s recursive -X theirs upstream master

Initialize your application and commit it::
  
  python initialize.py MyGrokApplication
  git commit

Then push the repo to OpenShift (this will take quite a while to finish)::
  
  git push

Thats it, you now can check out your application at::

  http://grok-$yournamespace.rhcloud.com

Notes
======

Virtual hosting
---------------

You may have multiple Grok applications per deployment and you may assign a 
domain to each of the applications. To setup virtual hosting for your
Grok application, you will need to configure ``deploy.ini`` with some
rewrite rules. Follow the steps below:

Edit ``etc/deploy.ini.in``. Find a section called ``pipeline:main``, and add
``rewrite`` as the first item in the pipeline. The section should appear like
this now::
  
  [pipeline:main]
  pipeline = rewrite accesslogging evalexception fanstatic grok

At the bottom of the file, add these lines. Replace ``examplesite`` 
with an identifier for the entry, replace ``app`` with your application ID,
and replace ``www.example.com`` with the virtual hosting domain::

  [filter:rewrite]
  use = egg:WSGIRewrite
  rulesets = examplesite-http examplesite-https
  
  [wsgirewrite:examplesite-http]
  cond1 = %{HTTP_HOST} ^www.example.com$
  cond2 = %{HTTPS} off
  rule1 = ^/(.*) app/++vh++http:www.example.com/++/$1
  
  [wsgirewrite:examplesite-https]
  cond1 = %{HTTP_HOST} ^www.example.com$
  cond2 = %{HTTPS} on
  rule1 = ^/(.*) app/++vh++https:www.example.com/++/$1
  

To add multiple domains, add them as additional rulesets in 
``[filter:rewrite]``

Commit and push to apply
