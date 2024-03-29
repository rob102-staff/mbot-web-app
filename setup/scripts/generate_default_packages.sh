
# build the app-base
echo "Building app-base"
cd ../../app
npm install
npm run build
cd build
cp -r * ../../setup/packages/app-skeleton

echo "Building mbot-settings-page"
cd ../../packages/default/mbot-settings-page
cd mbot-settings-page
npm install
npm run build
cp metadata.json build/metadata.json

cd ../
rm -rf setup/packages/settings-page
mkdir setup/packages/settings-page

cd mbot-settings-page/build
cp -r * ../../setup/packages/settings-page

echo "Building mbot-drive-and-map-package"
cd ../../
cd mbot-drive-and-map-package
npm install
npm run build
cp metadata.json build/metadata.json

cd ../
rm -rf setup/packages/drive-and-map-package
mkdir setup/packages/drive-and-map-package

cd mbot-drive-and-map-package/build
cp -r * ../../setup/packages/drive-and-map-package

echo "Building mbot-home-page"
cd ../../
cd mbot-home-page
npm install
npm run build
cp metadata.json build/metadata.json

cd ../
rm -rf setup/packages/home-page
mkdir setup/packages/home-page

cd mbot-home-page/build
cp -r * ../../setup/packages/home-page
