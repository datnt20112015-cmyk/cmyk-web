x=int(input('nhap so klw'))
if x <= 50 :
    a=x*1700
elif x >= 51 and x <= 100 :
    b=50*1700+(x- 50)*1900
elif x >=101 and x <=200 :
    c=50*1700+50*1900+(x-100)*2100
else:
    d=50*1700+50*1900+100*2100+(x-200)*3000
print('So money can phai tra la:',d)