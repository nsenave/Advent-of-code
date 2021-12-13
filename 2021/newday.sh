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

mkdir example
cd example/
touch input.txt

cd ..
code .

echo "GLHF"
