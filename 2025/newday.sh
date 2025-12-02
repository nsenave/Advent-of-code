echo "Day number:"
read daynumber
if (($daynumber < 10))
then 
    daydir="day_0$daynumber"
else 
    daydir="day_$daynumber"
fi
mkdir $daydir

cp daily.py $daydir

cd $daydir
mv daily.py day$daynumber.py
touch sandbox.py
touch input.txt

touch input-example.txt

# https://www.reddit.com/r/adventofcode/comments/e7khy8/comment/fa13hb9
echo "input.txt" >> .gitignore

code .

echo "GLHF"
