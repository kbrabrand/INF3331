import subprocess;
import unittest;
import os;

from src import code_import;

# Test the code import
class TestCodeImport(unittest.TestCase):

    def setUp(self):
        # Get the base path
        self.test_base_path = os.path.dirname(__file__);

        # Build the path to the output file
        self.output_file = os.path.join(
            self.test_base_path,
            '../../tmp/code_import.tex'
        );

        # Biuld the path to the prepro.py file
        self.prepro_path = os.path.join(
            self.test_base_path,
            '../../prepro.py'
        );

    def tearDown(self):
        # Remove output file when the test is run
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

        # Run the preprocessor on the input file
        process = subprocess.Popen([
            'python',
            self.prepro_path,
            input_file,
            self.output_file
        ], stdout=subprocess.PIPE);

        out, err = process.communicate();

        # Verify that the output file is equal to the expected output
        self.assertTrue(open(expected_file).read() == open(self.output_file).read());

if __name__ == '__main__':
    unittest.main()