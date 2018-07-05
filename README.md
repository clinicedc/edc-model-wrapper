# edc-model-wrapper
[![Build Status](https://travis-ci.org/clinicedc/edc-model-wrapper.svg?branch=develop)](https://travis-ci.org/clinicedc/edc-model-wrapper) [![Coverage Status](https://coveralls.io/repos/github/clinicedc/edc-model-wrapper/badge.svg?branch=develop)](https://coveralls.io/github/clinicedc/edc-model-wrapper?branch=develop)

Wrap a model instance with a custom wrapper to add methods needed for Edc Dashboards and Listboards.

    class ExampleModelWrapper(ModelWrapper):
        model = 'edc_model_wrapper.example'
        next_url_name = 'edc-model-wrapper:listboard_url'
        next_url_attrs = ['f1']
        querystring_attrs = ['f2', 'f3']
    
        def hello(self):
            return 'hello'
        
        def goodbye(self):
            return 'goodbye'

Instantiate with a model instance, persisted or not:

    model_obj = Example(f1=1, f2=2, f3=3) 
    wrapper = ExampleExampleModelWrapper(model_obj=model_obj)
    
Get the "admin" url with "next" for model objects in a Listboard, Dabsboard, etc,

    >>> wrapper.href
    '/admin/edc_model_wrapper/example/add/?next=edc-model-wrapper:listboard_url,f1&f1=1&f2=2&f3=3'

Get the admin url without the "next" querystring data:

    >>> wrapper.admin_url_name
    '/admin/edc_model_wrapper/example/add/'

Reverse the next_url:

    >>> wrapper.reverse()
    '/listboard/1/'


Attribute `model` is a model class regardless of how it was declared:

    >>> assert wrapper.model == Example
    True


All field attributes are converted to string and added to the wrapper, except foreign keys:

    >>> wrapper.f1
    1
    >>> wrapper.f2
    2

    
Custom methods/properties are, of course, available:

    >>> wrapper.hello()
    'hello'
    >>> wrapper.goodbye()
    'goodbye'


The original object is accessible, if needed:

    >>> wrapper.object
    <Example>

... for example to access original field values:

    >>> wrapper.report_datetime
    '2017-06-01 15:04:41.760296'
    
    >>> wrapper.object.report_datetime
    datetime.datetime(2017, 6, 1, 15, 4, 55, 594512)

    