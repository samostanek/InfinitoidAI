cd application.windows64/lib
mkdir tmp
cd tmp
jar -xvf ../core.jar
jar -xvf ../InfinitoidAI.jar
cd ..
jar -cvfm ../../Visualisation.jar tmp/META-INF/MANIFEST.MF -C tmp .
PAUSE