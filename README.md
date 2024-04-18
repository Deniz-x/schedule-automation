Automating schedule-making for my workplace using Selenium and BeautifulSoup. Time saved = ~30 mins per working day.

Test it by running the schedule_builder.py script. Might need to download the requirements.txt:

```
pip install -r requirements.txt
```

Given the power point template, the script extracts relevant data from the reservations website, makes the schedule according to extracted data by making changes to the template and saves it as "schedule_of_the_day.pptx".

The automator is only able to make the schedule for the current day, therefore if there is no schedule on the website on the day of running the code, it will not produce results. I will add the functionality to make the schedule for a given date or the next scheduled date in the future.

There is a bug where the data scraping doesn't work rarely, but rerunning the script fixes this.