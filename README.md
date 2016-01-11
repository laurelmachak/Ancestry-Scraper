Description:
This package of programs can be used to scrape the census data for New York City from Ancestry.com.
I developed these programs for research I did alongside Professor Don Davis and Sun Kyoung Lee of the
Columbia University Economics Department. This census data is not publically available in an OCR'd form,
but Ancestry.com used human readers to digitize the entirety of the records, which are available until 1940.
It would have been lovely to be able to package the scrapers for the different years in a single program,
but the data collected varies by year, so it was simpler to leave them in this form. There are a bunch of hard-
coded links in the program, but it should be fairly simple to change them if you require the data for a different
subdivision of the country. These programs output the data in CSV format, which is readable both by spreadsheet
applications and by data-analysis programs such as STATA.

Requirements:
These programs require the following libraries, which (except for Python 3) can be installed using PIP. 
Python 3
Mechanize
BeautifulSoup
pyexcel

To use:
Pick the appropriate program (there are only programs for 1850-1940 included since this was the data we collected).
Data from before 1850 exists, but no censuses after 1940 have been released in their entirety for privacy reasons.
Run using "python ____________" (with the path to the program in the blank). No arguments are needed.