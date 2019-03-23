|pypi| |travis| |codecov| |downloads|


edc-model-wrapper
-----------------

Wrap a model instance with a custom wrapper to add methods needed for Edc Dashboards and Listboards.

.. code-block:: python

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

.. code-block:: python

    model_obj = Example(f1=1, f2=2, f3=3) 
    wrapper = ExampleExampleModelWrapper(model_obj=model_obj)
    
Get the "admin" url with "next" for model objects in a Listboard, Dabsboard, etc,

.. code-block:: python

    >>> wrapper.href
    '/admin/edc_model_wrapper/example/add/?next=edc-model-wrapper:listboard_url,f1&f1=1&f2=2&f3=3'

Get the admin url without the "next" querystring data:

.. code-block:: python

    >>> wrapper.admin_url_name
    '/admin/edc_model_wrapper/example/add/'

Reverse the next_url:

.. code-block:: python

    >>> wrapper.reverse()
    '/listboard/1/'


Attribute `model` is a model class regardless of how it was declared:

.. code-block:: python

    >>> assert wrapper.model == Example
    True


All field attributes are converted to string and added to the wrapper, except foreign keys:

.. code-block:: python

    >>> wrapper.f1
    1
    >>> wrapper.f2
    2

    
Custom methods/properties are, of course, available:

.. code-block:: python

    >>> wrapper.hello()
    'hello'
    >>> wrapper.goodbye()
    'goodbye'


The original object is accessible, if needed:

.. code-block:: python

    >>> wrapper.object
    <Example>

for example to access original field values:

.. code-block:: python

    >>> wrapper.report_datetime
    '2017-06-01 15:04:41.760296'
    
    >>> wrapper.object.report_datetime
    datetime.datetime(2017, 6, 1, 15, 4, 55, 594512)

    
.. |pypi| image:: https://img.shields.io/pypi/v/edc-model-wrapper.svg
    :target: https://pypi.python.org/pypi/edc-model-wrapper
    
.. |travis| image:: https://travis-ci.org/clinicedc/edc-model-wrapper.svg?branch=develop
    :target: https://travis-ci.org/clinicedc/edc-model-wrapper
    
.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-model-wrapper/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-model-wrapper

.. |downloads| image:: https://pepy.tech/badge/edc-model-wrapper
   :target: https://pepy.tech/project/edc-model-wrapper
