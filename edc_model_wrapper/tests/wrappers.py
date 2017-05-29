from ..model_wrapper import ModelWrapper
from ..model_with_log_wrapper import ModelWithLogWrapper


class ExampleModelWrapper(ModelWrapper):

    model_name = 'edc_model_wrapper.example'
    next_url_attrs = {'edc_model_wrapper.example': ['f1']}
    extra_querystring_attrs = {'edc_model_wrapper.example': ['f2', 'f3']}
    url_instance_attrs = ['f1', 'f2', 'f3']
    url_namespace = 'edc-model-wrapper'


class ParentExampleModelWrapper(ModelWrapper):

    model_name = 'edc_model_wrapper.parentexample'
    next_url_attrs = {'edc_model_wrapper.parentexample': ['f1']}
    extra_querystring_attrs = {'edc_model_wrapper.parentexample': ['f2', 'f3']}
    url_instance_attrs = ['f1', 'f2', 'f3']
    url_namespace = 'edc-model-wrapper'


class ExampleLogEntryModelWrapper(ModelWrapper):

    model_name = 'edc_model_wrapper.examplelogentry'
    next_url_attrs = {'edc_model_wrapper.examplelogentry': [
        'example_identifier', 'example_log']}
    extra_querystring_attrs = {
        'edc_model_wrapper.examplelogentry': ['f2', 'f3']}
    url_instance_attrs = ['example_identifier', 'example_log']
    url_namespace = 'edc-model-wrapper'

    @property
    def example_identifier(self):
        return self._original_object.example_log.example.example_identifier

    @property
    def survey(self):
        return 'survey_one'


class ExampleModelWithLogWrapper(ModelWithLogWrapper):

    model_wrapper_class = ExampleModelWrapper
    log_entry_model_wrapper_class = ExampleLogEntryModelWrapper


class ParentExampleModelWithLogWrapper(ModelWithLogWrapper):

    model_wrapper_class = ParentExampleModelWrapper
    log_entry_model_wrapper_class = ExampleLogEntryModelWrapper

    parent_model_wrapper_class = ExampleModelWrapper
    parent_lookup = 'example'
