echo "Day number:"
read daynumber
if (($daynumber < 10))
then 
    daydir="day_0$daynumber"
else 
    daydir="day_$daynumber"
fi

git add $daydir
git commit -m "day $daynumber 2021"
git push
