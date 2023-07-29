import os
import difflib

def test(test_folder, out_folder):
    test_directory_path = os.path.join(test_folder)
    result_directory_path = os.path.join(out_folder)
    test_files = os.listdir(test_directory_path)
    result_files = os.listdir(result_directory_path)
    errors = 0
    if len(test_files) != len(result_files):
        print(f"FILE GEN INCONSISTENT AMOUNT: Baseline has {len(test_files)} files, New has {len(result_files)} files")
        errors = errors + 1
    for file in test_files:
        test_file =  os.path.join(test_directory_path, file)
        result_file =  os.path.join(result_directory_path, file)
        if os.path.exists(result_file):
            test_file_str = ""
            result_file_str = ""
            with open(result_file, "r") as f:
                result_file_str = f.read()
            with open(test_file, "r") as f:
                test_file_str = f.read()
            if result_file_str != test_file_str:
                print(f"LINKING ERROR: {file} mismatch")
                errors = errors + 1
        else:
            print(f"FILE GEN INCONSISTENT FILENAME: New missing {file} file")
            errors = errors + 1
    for file in result_files:
        test_file =  os.path.join(test_directory_path, file)
        result_file =  os.path.join(result_directory_path, file)
        if os.path.exists(test_file):
            test_file_str = ""
            result_file_str = ""
            with open(result_file, "r") as f:
                result_file_str = f.read()
            with open(test_file, "r") as f:
                test_file_str = f.read()
            if result_file_str != test_file_str:
                print(f"LINKING ERROR: {file} mismatch")
                diff_str(result_file_str, test_file_str)
                errors = errors + 1

        else:
            print(f"FILE GEN INCONSISTENT FILENAME: Baseline missing {file} file")
            errors = errors + 1

    if errors == 0:
        print("ALL TESTS PASSED")

def diff_str(a, b):
    print('{} => {}'.format(a,b))  
    for i,s in enumerate(difflib.ndiff(a, b)):
        if s[0]==' ': 
            continue
        elif s[0]=='-':
            print(u'Delete "{}" from position {}'.format(s[-1],i))
        elif s[0]=='+':
            print(u'Add "{}" to position {}'.format(s[-1],i))
        print()   