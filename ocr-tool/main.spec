# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\wakib\\Desktop\\twsc\\document_classifier'],
    binaries=[],
    datas=[
        ('C:\\Users\\wakib\\Desktop\\twsc\\document_classifier\\templates', 'templates'),  # Include templates folder
        ('C:\\Users\\wakib\\Desktop\\twsc\\document_classifier\\uploads', 'uploads')  # Include uploads folder
    ],
    hiddenimports=[
        'flask', 'flask.request', 'flask.render_template', 'flask.redirect',
        'flask.url_for', 'flask.send_from_directory', 'flask.send_file',
        'pandas', 'werkzeug.utils.secure_filename', 'cv2', 'pytesseract',
        'joblib', 'shutil', 'zipfile', 'tempfile', 'os', 'sys', 'joblib.load',
        'sklearn.feature_extraction', 'scikit-learn', 'sklearn.ensemble',
        'sklearn', 'sklearn.pipeline', 'matplotlib.pyplot', 'nltk', 're',
        'nltk.corpus.stopwords', 'nltk.stem.WordNetLemmatizer',
        'nltk.stem.PorterStemmer', 'scipy.stats.randint',
        'sklearn.metrics.accuracy_score', 'sklearn.metrics.confusion_matrix',
        'sklearn.metrics.precision_score', 'sklearn.metrics.recall_score',
        'sklearn.metrics.ConfusionMatrixDisplay', 'sklearn.metrics.classification_report',
        'sklearn.model_selection.RandomizedSearchCV', 'sklearn.model_selection.StratifiedShuffleSplit',
        'sklearn.model_selection.train_test_split', 'sklearn.preprocessing.LabelEncoder',
        'sklearn.tree.export_graphviz', 'sklearn.feature_extraction.text.CountVectorizer',
        'sklearn.ensemble.RandomForestClassifier', 'graphviz', 'nltk.data'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[]
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
