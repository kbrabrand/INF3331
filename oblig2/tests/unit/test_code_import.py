import subprocess;
import unittest;
import os;

from src import code_import;

class TestCodeImport(unittest.TestCase):

    def setUp(self):
        self.test_base_path = os.path.dirname(__file__);

        self.output_file = os.path.join(
            self.test_base_path,
            '../../tmp/code_import.tex'
        );

        self.prepro_path = os.path.join(
            self.test_base_path,
            '../../prepro.py'
        );

    def tearDown(self):
        try:
            os.remove(self.output_file);
        except OSError as e:
            return;

    def test_code_import(self):
        input_file = os.path.join(
            self.test_base_path,
            'fixtures/code_import/before.tex'
        );

        expected_file = os.path.join(
            self.test_base_path,
            'fixtures/code_import/after.tex'
        );

        subprocess.Popen([
            'python',
            self.prepro_path,
            input_file,
            self.output_file
        ]);

        self.assertTrue(open(expected_file).read() == open(self.output_file).read());

if __name__ == '__main__':
    unittest.main()