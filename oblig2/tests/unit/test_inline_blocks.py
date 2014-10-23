import subprocess;
import unittest;
import os;

from src import code_import;

# Test execution of inline code
class TestInlineBlocks(unittest.TestCase):

    def setUp(self):
        # Get the base path
        self.test_base_path = os.path.dirname(__file__);

        # Build the path to the output file
        self.output_file = os.path.join(
            self.test_base_path,
            '../../tmp/inline_blocks.tex'
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

    def test_inline_blocks(self):
        input_file = os.path.join(
            self.test_base_path,
            'fixtures/inline_blocks/before.tex'
        );

        expected_file = os.path.join(
            self.test_base_path,
            'fixtures/inline_blocks/after.tex'
        );

        # Run the preprocessor on the input file
        subprocess.Popen([
            'python',
            self.prepro_path,
            input_file,
            self.output_file
        ]);

        # Verify that the output file is equal to the expected output
        self.assertTrue(open(expected_file).read() == open(self.output_file).read());

if __name__ == '__main__':
    unittest.main()