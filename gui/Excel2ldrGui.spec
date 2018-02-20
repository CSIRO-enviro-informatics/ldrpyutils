# -*- mode: python -*-

block_cipher = None


a = Analysis(['Excel2ldrGui.py'],
             binaries=[],
             datas=[( '../config.json', '.' ), 
					( 'csiro.ico', '.' ),
			        ('../ldrpyutils/data/*.ttl', 'ldrpyutils/data' )],
             hiddenimports=['rdflib.plugins','rdflib.plugins','rdflib.plugins.memory','rdflib','urllib3','ldrpyutils','validators','rdflib.plugins.parsers.notation3','rdflib.plugins.serializers.turtle'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Excel2ldrGui',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='csiro.ico')
