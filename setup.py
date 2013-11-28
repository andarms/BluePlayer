from distutils.core import setup
import py2exe

setup(
	windows=['rainbow.py'],
	data_files = [
	            ('phonon_backend', [
	                'C:\Python27\Lib\site-packages\PySide\plugins\phonon_backend\phonon_ds94.dll'
	                ]),
	            ('images', ['C:\Users\mesa\Desktop\\rainbow\images\\folder-add-2.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\expand-2.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\play.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\stop.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\pause.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\next.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\previous.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\repeat.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\revert.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\list.png',
	            			'C:\Users\mesa\Desktop\\rainbow\images\\shuffle.png'
	            			]
	            )
	],
	options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"]
        }
    }
)
