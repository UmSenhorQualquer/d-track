@echo off

setlocal enableextensions enabledelayedexpansion

rem set /A PYTHON_VERSION=2

IF /I "%PYTHON_VERSION%" EQU "2" (
	set "WINPYDIR=C:\Users\swp\Python\WinPython-32bit-2.7.10.3\python-2.7.10"
	set "WINPYVER=2.7.10.3"
) ELSE (
	set "WINPYDIR=C:\Users\swp\Python\WinPython-32bit-3.4.3.7\python-3.4.3"
	set "WINPYVER=3.4.3.7"
)

set "HOME=%WINPYDIR%\..\settings"
set "WINPYARCH=WIN32"

set "PATH=%WINPYDIR%\Lib\site-packages\PyQt4;%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%WINPYDIR%\..\tools;"

:: keep nbextensions in Winpython directory, rather then %APPDATA% default
set "JUPYTER_DATA_DIR=%WINPYDIR%\..\settings"

echo "PYTHON VERSION:"
python --version

set "PROJECTNAME=d-tracker"
set "BUILDSETTINGSDIR=%WORKSPACE%\build_settings\win"
set "MAINSCRIPT=%WORKSPACE%\dolphintracker\singlecam_tracker\singlecam_tracker\singlecam_tracker.py"
set "BUILDOUTDIR=%WORKSPACE%\build"
set "DISTOUTDIR=%WORKSPACE%\dist"
set "ICONNAME=cf_icon_128x128.ico"

python setup.py --version > software_version.txt
"C:\Program Files\Git\bin\git.exe" rev-list  --all --count > git_version.txt
SET /p DEV_VERSION= < software_version.txt
SET /p GIT_VERSION= < git_version.txt
SET DEV_VERSION=%DEV_VERSION%_git%GIT_VERSION%_build%BUILD_NUMBER%
DEL software_version.txt
DEL git_version.txt

:: clean workspace
@RD /S /Q %BUILDOUTDIR%
@RD /S /Q %DISTOUTDIR%


:: echo "Running pyinstaller --additional-hooks-dir %BUILDSETTINGSDIR%\hooks --name %PROJECTNAME% --icon %BUILDSETTINGSDIR%\%ICONNAME% --onefile %MAINSCRIPT%"
IF %COMPILE_2_FOLDER% EQU true (
	echo pyinstaller --additional-hooks-dir "%BUILDSETTINGSDIR%\hooks" --name "%PROJECTNAME%_v%DEV_VERSION%_DEV" --icon "%BUILDSETTINGSDIR%\%ICONNAME%" --onedir --debug "%MAINSCRIPT%"
	pyinstaller --additional-hooks-dir "%BUILDSETTINGSDIR%\hooks" --name "%PROJECTNAME%_v%DEV_VERSION%_DEV" --icon "%BUILDSETTINGSDIR%\%ICONNAME%" --onedir --debug "%MAINSCRIPT%"
	IF %SOURCEFORGE_UPLOAD% EQU true (
		echo cd "%WORKSPACE%\dist\" & python c:\Users\swp\Python\zip.py "%PROJECTNAME%_v%DEV_VERSION%_DEV" "%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%_DEV.zip"
		cd "%WORKSPACE%\dist\" & python c:\Users\swp\Python\zip.py "%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%_DEV" "%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%_DEV.zip"
		echo "Uploading to SourceForge..."
		echo c:\curl\curl.exe --progress-bar --netrc-file c:\curl_auth\bitbucket_auth.txt -X POST https://api.bitbucket.org/2.0/repositories/fchampalimaud/pythonvideoannotator/downloads -F files=@"%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%_DEV.zip"
		c:\curl\curl.exe --progress-bar --netrc-file c:\curl_auth\bitbucket_auth.txt -X POST https://api.bitbucket.org/2.0/repositories/fchampalimaud/pythonvideoannotator/downloads -F files=@"%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%_DEV.zip" > curl_output.log
	) ELSE (
		echo "Skipping upload to SourceForge"
	)
) ELSE (
	echo pyinstaller --additional-hooks-dir "%BUILDSETTINGSDIR%\hooks" --name "%PROJECTNAME%_v%DEV_VERSION%_DEV" --icon "%BUILDSETTINGSDIR%\%ICONNAME%" --debug --onefile "%MAINSCRIPT%"
	pyinstaller --additional-hooks-dir "%BUILDSETTINGSDIR%\hooks" --name "%PROJECTNAME%_v%DEV_VERSION%_DEV" --icon "%BUILDSETTINGSDIR%\%ICONNAME%" --debug --onefile "%MAINSCRIPT%"
	IF %SOURCEFORGE_UPLOAD% EQU true (
		echo "Uploading to SourceForge..."
		echo c:\curl\curl.exe --progress-bar --netrc-file c:\curl_auth\bitbucket_auth.txt -X POST https://api.bitbucket.org/2.0/repositories/fchampalimaud/pythonvideoannotator/downloads -F files=@"%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%.exe"
		c:\curl\curl.exe --progress-bar --netrc-file c:\curl_auth\bitbucket_auth.txt -X POST https://api.bitbucket.org/2.0/repositories/fchampalimaud/pythonvideoannotator/downloads -F files=@"%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%.exe" > curl_output.log
	) ELSE (
		echo "Skipping upload to SourceForge"
	)
)




::c:\curl\curl.exe --progress-bar --netrc-file c:\curl_auth\bitbucket_auth.txt -X POST https://api.bitbucket.org/2.0/repositories/fchampalimaud/pythonvideoannotator/downloads -F files=@"%WORKSPACE%\dist\%PROJECTNAME%_v%DEV_VERSION%_DEV.zip" > curl_output.log