import subprocess;
import unittest;
import hashlib;
import shutil;
import os;

from src import code_import;

# Test the code import
class TestCompile(unittest.TestCase):

    def setUp(self):
        # Get the base path
        self.test_base_path = os.path.dirname(__file__);

        # Build the path to the output file
        self.output_folder = os.path.join(
            self.test_base_path,
            '../../tmp/compile'
        );

        # Build path to the PDF we're expecting the compiling to generate
        self.output_file = os.path.join(
            self.output_folder,
            'before.pdf'
        );

        # Make output directory if it does not exist
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder);

        # Biuld the path to the compile.py file
        self.compile_path = os.path.join(
            self.test_base_path,
            '../../compile.py'
        );

    def tearDown(self):
        shutil.rmtree(self.output_folder);

    def test_compile(self):
        # Assert that the output PDF file does not exist
        self.assertFalse(os.path.exists(self.output_file));

        input_file = os.path.join(
            self.test_base_path,
            'fixtures/compile/before.tex'
        );

        # Run the preprocessor on the input file
        process = subprocess.Popen([
            'python',
            self.compile_path,
            input_file,
            '--destination',
            self.output_folder
        ], stdout=subprocess.PIPE);

        out, err = process.communicate();

        # Verify that the output PDF file exists
        self.assertTrue(os.path.exists(self.output_file));

if __name__ == '__main__':
    unittest.main()