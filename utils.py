import re
from datetime import datetime, timedelta

from dateutil.parser import parse as datetime_parse

class MangakakalotManga:
    last_updated_at_pattern = r"([A-Z][a-z]{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}\s+[AP]M)"
    view_count_pattern = r"([\d,]+)"
    ratings_pattern = r"([\d.]+)\s*/\s*5\s*-\s*(\d+)\s*votes"

    @staticmethod
    def get_alt_titles(alt_titles_raw):
        if alt_titles_raw:
            alt_titles_raw = alt_titles_raw.replace("Alternative : ", "")
            alt_titles = re.split(",|;", alt_titles_raw)
            return [alt_title.strip() for alt_title in alt_titles]

        return []

    @staticmethod
    def get_status(status_raw):
        if status_raw:
            return status_raw.replace("Status : ", "")
        return ""

    @staticmethod
    def get_page_num(num_pages_raw):
        if num_pages_raw:
            num_pages = re.search(r'\d+', num_pages_raw).group()
            num_pages = int(num_pages)

            return num_pages
        return 0

    @staticmethod
    def get_summary(summary_raw):
        summary = ''
        if summary_raw != None:
            summary = summary_raw.strip()
        return summary
    
    @staticmethod
    def get_last_updated_at_timestamp(last_updated_at_raw):
        timestamp = None
        if last_updated_at_raw != None:
            last_updated_at_raw = re.sub(r'(Last updated :| PM| AM)', '', last_updated_at_raw).strip()
            timestamp = datetime_parse(last_updated_at_raw).timestamp()
        else:
            print("No match found.")

        return timestamp

    @staticmethod
    def get_view_count(view_count_raw):
        view_count = 0
        if view_count_raw != None:
            if 'K' in view_count_raw:
                view_count = int(float(view_count_raw[:-1]) * 1000)
            elif 'M' in view_count_raw:
                view_count = int(float(view_count_raw[:-1]) * 100000)
            else:
                view_count_raw = view_count_raw.replace("View : ", "")
                match = re.search(MangakakalotManga.view_count_pattern, view_count_raw)

                if match:
                    view_count_str = match.group(1)
                    view_count = int(view_count_str.replace(",", ""))
                else:
                    print("No match found.")

        return view_count

    @staticmethod
    def get_ratings(ratings_raw):
        rating = 0
        num_votes = 0
        if ratings_raw != None:
            ratings_raw = ratings_raw.replace("rate : ", "")
            match = re.search(MangakakalotManga.ratings_pattern, ratings_raw)


            if match:
                rating = float(match.group(1))
                num_votes = int(match.group(2))
            else:
                print("No match found.")

        return rating, num_votes

class MangakakalotChapter:
    title_pattern = r'Chapter\s+(\d+)(?::\s+(.+))?'

    @staticmethod
    def get_title_info(title_raw):
        chap_num, title = 0,0
        if title_raw != None:
            match = re.search(MangakakalotChapter.title_pattern, title_raw)

            try:
                chap_num = int(match.group(1))
                title = match.group(2) if match.group(2) else ''
            except:
                pass

        return chap_num, title

    @staticmethod
    def get_pub_date(pub_date_raw):
        if pub_date_raw:
            try:
                # Try to parse as "X hour ago"
                time_interval = int(pub_date_raw.split()[0])
                return datetime.timestamp(datetime.now() - timedelta(hours=time_interval))
            except ValueError:
                return datetime_parse(pub_date_raw).timestamp()

        return None

    @staticmethod
    def get_view_count(view_count_raw):
        view_count = 0
        if view_count_raw != None:
            if 'K' in view_count_raw:
                view_count = int(float(view_count_raw[:-1]) * 1000)
            elif 'M' in view_count_raw:
                view_count = int(float(view_count_raw[:-1]) * 100000)
            else:
                view_count = int(view_count_raw.replace(',', ''))
        return view_count
