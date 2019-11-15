# vim: expandtab tabstop=4 shiftwidth=4

import astroid
import pylint_beergarden
import pylint.testutils

class BeergardenCommandCheckerTests(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint_beergarden.checker.BeergardenCommandChecker

    def __init__(self):
        super(BeergardenCommandCheckerTests, self).setup_method()

    def test_parameter_without_command_decorator(self):
        func_node = astroid.extract_node("""
        @parameter(key='a', display_name='a', description='a', type='String')
        @parameter(key='b', display_name='b', description='b', type='String')
        @parameter(key='c', display_name='c', description='c', type='String')
        def foo(self, a, b, c): #@
            return
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='parameter-without-command-decorator',
                node=func_node
            )):
                self.checker.visit_functiondef(func_node)

    def test_parameter_before_command_decorator(self):
        func_node = astroid.extract_node("""
        @parameter(key='a', display_name='a', description='a', type='String')
        @parameter(key='b', display_name='b', description='b', type='String')
        @parameter(key='c', display_name='c', description='c', type='String')
        @command(output_type='JSON')
        def foo(self, a, b, c): #@
            return
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='parameter-before-command-decorator',
                node=func_node
            )):
                self.checker.visit_functiondef(func_node)

    def test_duplicate_parameter_keys(self):
        func_node = astroid.extract_node("""
        @command(output_type='JSON')
        @parameter(key='a', display_name='a', description='a', type='String')
        @parameter(key='b', display_name='b', description='b', type='String')
        @parameter(key='b', display_name='b', description='b', type='String')
        @parameter(key='c', display_name='c', description='c', type='String')
        def foo(self, a, b, c): #@
            return
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='duplicate-parameter-keys',
                node=func_node
            )):
                self.checker.visit_functiondef(func_node)

    def test_not_applicable(self):
        func_node = astroid.extract_node("""
        def foo(self, a, b, c): #@
            return
        """)

        with self.assertAddsMessages():
            self.checker.visit_functiondef(func_node)

    def test_decorator_key_parameter_name_mismatch(self):
        func_node = astroid.extract_node("""
        @command(output_type='JSON')
        @parameter(key='a', display_name='a', description='a', type='String')
        @parameter(key='b', display_name='b', description='b', type='String')
        @parameter(key='c', display_name='c', description='c', type='String')
        def foo(self, a, b, d): #@
            return
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='decorator-key-parameter-name-mismatch',
                node=func_node
            )):
                self.checker.visit_functiondef(func_node)

if __name__ == "__main__":
    checker = BeergardenCommandCheckerTests()
    checker.test_decorator_key_parameter_name_mismatch()
    checker.test_parameter_before_command_decorator()
    checker.test_parameter_without_command_decorator()
    checker.test_duplicate_parameter_keys()
    checker.test_not_applicable()
