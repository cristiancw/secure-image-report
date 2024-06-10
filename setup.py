from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='secure-image-report',
    version='0.0.1',
    description='It is a Python tool designed to generate XLS reports from vulnerability scan results of ECR (Elastic Container Registry) images on AWS. This tool facilitates the analysis and visualization of security data, enabling a more efficient approach to mitigating vulnerabilities in container environments.',
    author='Cristian C. Wolfram',
    license='Apache-2.0 license',
    long_description=readme,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.12',
    install_requires=[req for req in requirements if req[:2] != "# "],
    entry_points='''
        [console_scripts]
        secure-image-report=secure_image_report:main
    ''',
    data_files=[
        'secure-image-report_bash.sh',
        'requirements.txt'
    ],
    include_package_data=True,
)
