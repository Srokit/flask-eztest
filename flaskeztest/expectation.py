"""Expectation objects defined here."""


class Expectation(object):

    def __init__(self):
        object.__init__(self)
        self.name = None


class FixtureExpectation(Expectation):

    def __init__(self, fixture_name, expected_models=None, unexpected_models=None):
        Expectation.__init__(self)
        self.name = fixture_name
        self.expecting_all_models = True
        self.expecting_specific_models = False
        self.not_expecting_specific_models = False
        self.expected_models = list()
        self.unexpected_models = list()
        if expected_models is not None:
            self.models(expected_models)
        if unexpected_models is not None:
            self.not_models(unexpected_models)

    def models(self, models):
        """Add a group of new expected model."""
        if not self.expecting_all_models:
            raise Exception("Cannot explicitly expect and ignore models in the same fixture expectation.")
        self.expecting_all_models = False
        self.expecting_specific_models = True
        for model in models:
            if isinstance(model, ModelExpectation):
                self.expected_models.append(model)
            else:  # str
                self.expected_models.append(ModelExpectation(model))
        # This way we can chaing a call to FixtureExpectation.models() to an assignment of a FixtureObject type
        return self

    def not_models(self, models):
        if not self.expecting_all_models:
            raise Exception("Cannot explicitly expect and ignore models in the same fixture expectation.")
        self.expecting_all_models = False
        self.not_expecting_specific_models = True
        self.unexpected_models.extend(models)
        # This way we can chaing a call to FixtureExpectation.models() to an assignment of a FixtureObject type
        return self


class ModelExpectation(Expectation):

    def __init__(self, model_name, index=None, expected_fields=None, unexpected_fields=None):
        Expectation.__init__(self)
        self.name = model_name
        self.index = index
        self.expecting_all_fields = True
        self.expecting_specific_fields = False
        self.not_expecting_specific_fields = False
        self.unexpected_fields = list()
        self.expected_fields = list()
        if expected_fields is not None:
            self.fields(expected_fields)
        if unexpected_fields is not None:
            self.not_fields(unexpected_fields)

    def fields(self, fields):
        for field in fields:
            if type(field) is not FieldExpectation:
                self.expected_fields.append(FieldExpectation(field))
            else:
                self.expected_fields.append(field)
        if not self.expecting_all_fields:
            raise Exception("Cannot explicitly expect and ignore fields in the same model expectation.")
        self.expecting_all_fields = False
        self.expecting_specific_fields = True
        # This allows for .fields to be used inline in a FixtureExpectation.models() call
        return self

    def not_fields(self, fields):
        if not self.expecting_all_fields:
            raise Exception("Cannot explicitly expect and ignore fields in the same model expectation.")
        self.expecting_all_fields = False
        self.not_expecting_specific_fields = True
        self.unexpected_fields.extend(fields)
        # This allows for .fields to be used inline in a FixtureExpectation.models() call
        return self


class FieldExpectation(Expectation):

    def __init__(self, field_name, check_visible=False, check_invisible=False):
        Expectation.__init__(self)
        if check_invisible and check_invisible:
            raise Exception("Cannot both check the visibility and check the invisiblity of a field.")
        self.name = field_name
        self.check_visible = check_visible
        self.check_invisible = check_invisible

    def visible(self):
        if self.check_invisible:
            raise Exception("Cannot both check the visibility and check the invisiblity of a field.")
        self.check_visible = True
        return self

    def invisible(self):
        if self.check_visible:
            raise Exception("Cannot both check the visibility and check the invisiblity of a field.")
        self.check_invisible = True
        return self


def expect_fixture(fixture_name):
    """Serves as a nice idiomatic short cut to using FixtureExpectation constructor for chaining the rest of the
    expectation statment."""
    return FixtureExpectation(fixture_name)
