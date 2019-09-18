cd ./docs
sphinx-apidoc -f -o source/ ../search_engine_parser
if [ $? -ne 0 ]; then
   echo "Failed to run sphinx-apidoc"
   exit 1
fi
make html
if [ $? -ne 0 ]; then
   echo "Failed to make html"
   exit 1
fi
cd ..
git commit -am "make html"
git config --global push.default simple
git config --global user.email "travis@travis-ci.com"
git config --global user.name "Travis CI"


#remove existing files except html
shopt -s extglob
rm -r ./!(docs)/

#copy contents of html to root
cp -R ${TRAVIS_BUILD_DIR}/docs/build/html/. ${TRAVIS_BUILD_DIR}/

#remove html and accompanying docs  
rm -r ./docs
echo "Viewing current files in directory"
ls -lah
# Checkout to gh-pages
git checkout gh-pages
if [ $? -eq 1 ]; then
   echo "Checked out to existing gh-pages branch"
else
   git checkout -b gh-pages
   echo "Creating gh-pages branch"
fi 
git add .
git commit -am "rebuilt docs"
git remote add origin-pages https://${GITHUB_TOKEN}@github.com/bisoncorps/search_engine_parser.git
git push -u origin-pages gh-pages --force

# echo if docs was succesfully pushed
if [ $? -eq 0 ]; then
    echo "Docs successfully pushed to Github Pages"
else
    echo "Failed to push docs"
    exit 1
fi
