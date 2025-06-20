from setuptools import setup, find_packages

setup(
    name='ocr-tool',
    version='0.1.0',
    description='OCR tool using Flask',
    author='wuhhkhie',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
        'pandas>=1.0.0',
        'opencv-python>=4.0.0',
        'pytesseract>=0.3.0',
        'joblib>=1.0.0',
        'Werkzeug>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'run_app=ocr-tool.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)