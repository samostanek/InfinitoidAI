ECHO OFF

ECHO Moving to lib directory...
cd application.windows64/lib


ECHO Making tmp directory...
mkdir tmp

ECHO.

ECHO Extracting core.jar to tmp directory...
cd tmp
jar -xf ../core.jar

ECHO Extracting InfinitoidAI.jar to tmp directory...
jar -xf ../InfinitoidAI.jar
cd ..

ECHO.

ECHO Compressing tmp directory to InfinitoidAI/Visualisation.jar with manifest from original InfinitoidAI.jar...
jar -cfm ../../Visualisation.jar tmp/META-INF/MANIFEST.MF -C tmp .

ECHO.

ECHO Deleting tmp directory...
rmdir /S /Q tmp

ECHO.

PAUSE