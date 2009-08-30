import math
class SakaCalendar:
    JULIAN_EPOCH = 1721425.5
    SAKA_MONTH_NAMES= ["Chaitra", "Vaisakha", "Jyaishta", "Asadha", "Sravana", "Bhadra","Aswina", "Kartiak", "Agrahayana","Pausa","Magha","Phalguna"]
    SAKA_WEEK_NAMES= ["Ravivar", "Somavar", "Mangalvar", "Budhvar", "Sukhravar", "Guruvar","Sanivar"]
    IE = 0
    # The only practical difference from a Gregorian calendar is that years
    #are numbered since the Saka Era.  A couple of overrides will
    #take care of that....
    # Starts in 78 AD, 
    INDIAN_ERA_START = 78
    # The Indian year starts 80 days later than the Gregorian year.
    INDIAN_YEAR_START = 80
    def get_month_length(self, extendedYear,  month): 
        if  month < 0  or  month > 11:
            extendedYear += month/12 # floorDivide(month, 12, remainder)
            month =  month%12
        if self.is_gregorian_leap(extendedYear + self.INDIAN_ERA_START) and month == 0:
            return 31
        if month >= 1 and  month <=5 : 
            return 31
        return 30
    
    
    """
     This routine converts an Indian date to the corresponding Julian date
     @param year   The year in Saka Era according to Indian calendar.
     @param month  The month according to Indian calendar (between 1 to 12)
     @param date   The date in month 
    """
    def saka_to_julian_date(self,year,month, date):
        gyear = year + self.INDIAN_ERA_START
        if self.is_gregorian_leap(gyear) :
            leapMonth = 31
            start = self.gregorian_to_julian_date(gyear, 3, 21)
        else :
            leapMonth = 30
            start = self.gregorian_to_julian_date(gyear, 3, 22)
        if month == 1  : 
            jd = start + (date - 1)
        else:
            jd = start + leapMonth
            m = month - 2
            m = m if m <= 5 else 5
            jd += m * 31
            if  month >= 8  :
                m = month - 7
                jd += m * 30
            jd += date - 1
        return jd
    

    """
      The following function is not needed for basic calendar functioning.
      This routine converts a gregorian date to the corresponding Julian date"
      @param year   The year in standard Gregorian calendar (AD/BC) .
      @param month  The month according to Gregorian calendar (between 0 to 11)
      @param date   The date in month 
    """
    def gregorian_to_julian_date(self, year, month, date) :
        jd = ((self.JULIAN_EPOCH - 1) +
            (365 * (year - 1)) +
            math.floor((year - 1) / 4) +
            (-math.floor((year - 1) / 100)) +
            math.floor((year - 1) / 400) +
            math.floor((((367 * month) - 362) / 12) +
            ( 0 if (month <= 2) else -1 if self.is_gregorian_leap(year) else -2) ) +
            date)
            
        return jd


    """
       The following function is not needed for basic calendar functioning.
       This routine converts a julian day (jd) to the corresponding date in Gregorian calendar"
       @param jd The Julian date in Julian Calendar which is to be converted to Indian date"
    """
    def julian_date_to_gregorian(self, jd) :
        julianDate=[None, None,None]
        wjd = math.floor(jd - 0.5) + 0.5
        depoch = wjd - self.JULIAN_EPOCH
        quadricent = math.floor(depoch / 146097)
        dqc = depoch % 146097
        cent = math.floor(dqc / 36524)
        dcent = dqc % 36524
        quad = math.floor(dcent / 1461)
        dquad = dcent % 1461
        yindex = math.floor(dquad / 365)
        year = int((quadricent * 400) + (cent * 100) + (quad * 4) + yindex)
        if  not ((cent == 4)  or (yindex == 4)) :
            year+=1
        yearday = wjd - self.gregorian_to_julian_date(year, 1, 1)
        leapadj = ( 0 if (wjd < self.gregorian_to_julian_date(year, 3, 1)) else  1 if self.is_gregorian_leap(year) else 2) 
        month = int(math.floor((((yearday + leapadj) * 12) + 373) / 367))
        day = int((wjd - self.gregorian_to_julian_date(year, month, 1)) + 1)
        julianDate[0] = year
        julianDate[1] = month
        julianDate[2] = day
        return julianDate


    """
      The following function is not needed for basic calendar functioning.
      This routine checks if the Gregorian year is a leap year"
      @param year      The year in Gregorian Calendar
    """
    def is_gregorian_leap(self,year):
        return ((year % 4) == 0) and (not(((year % 100) == 0) and ((year % 400) != 0)))

    def gregorian_to_saka_date(self, gregorianDay):
        indDate=[None,None,None]
        IndianYear = gregorianDay[0] - self.INDIAN_ERA_START            # Year in Saka era
        jdAtStartOfGregYear = self. gregorian_to_julian_date(gregorianDay[0], 1, 1) # JD at start of Gregorian year
        julianDay = self.gregorian_to_julian_date( gregorianDay[0],  gregorianDay[1],  gregorianDay[2])
        yday = int(julianDay - jdAtStartOfGregYear)              # Day number in Gregorian year (starting from 0)
        if  yday < self.INDIAN_YEAR_START  :
            #  Day is at the end of the preceding Saka year
            IndianYear -= 1
            leapMonth = 31 if self.is_gregorian_leap(gregorianDay[0] - 1) else 30 # Days in leapMonth this year, previous Gregorian year
            yday += leapMonth + (31 * 5) + (30 * 3) + 10
        else:
            leapMonth =  31 if self.is_gregorian_leap(gregorianDay[0]) else 30 # Days in leapMonth this year
            yday -= self.INDIAN_YEAR_START
        if  yday < leapMonth  :
            IndianMonth = 0
            IndianDayOfMonth = yday + 1
        else :
            mday = yday - leapMonth
            if mday < (31 * 5) :
                IndianMonth = int(math.floor(mday / 31) + 1)
                IndianDayOfMonth = (mday % 31) + 1
            else :
                mday -= 31 * 5
                IndianMonth = int(math.floor(mday / 30)) + 6
                IndianDayOfMonth = (mday % 30) + 1
            
        #Month is 0 based.converting it to 1 based
        if  IndianMonth == 12  :
            IndianMonth = 1
        else :
            IndianMonth = IndianMonth +1  
        indDate[0]=IndianYear
        indDate[1]=IndianMonth
        indDate[2]=IndianDayOfMonth
        return indDate
    def get_month_name(month_index):
        return self.SAKA_MONTH_NAMES[month_index-1]
    def get_week_name(week_index)  :
        return self.SAKA_WEEK_NAMES[week_index-1]
