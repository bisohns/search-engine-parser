"""@desc
		Parser for coursera search results
"""

from search_engine_parser.core.base import BaseSearch
from urllib.parse import urljoin


class CourseraSearch(BaseSearch):
    """
    Searches Coursera for string
    """
    name = "Coursera"
    search_url = "https://www.coursera.org/search?query={query}&indices[prod_all_products_term_optimization_test][page]={page}"
    summary = "\tCoursera is an American online learning platform founded by Stanford professors Andrew Ng and " \
              "Daphne Koller that offers massive open online courses, specializations, and degrees."

    def parse_soup(self, soup):
        """
        Parses Coursera Search Soup for results
        """
        # find all class_='gs_r gs_or gs_scl' => each result
        return soup.find_all('li', class_='ais-InfiniteHits-item')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="gs_r gs_or gs_scl">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link, description, file link, result type of single result
        :rtype: dict
        """
        link = urljoin(
            'https://www.coursera.org',
            single_result.find('a', class_='rc-DesktopSearchCard anchor-wrapper').get('href')
        )

        title = single_result.find('h2').text

        partner_elem = single_result.find('span', class_='partner-name')
        partner = ''
        if partner_elem:
            partner = partner_elem.text

        rating_avg_elem = single_result.find('span', class_='ratings-text')
        rating_avg = None
        if rating_avg_elem:
            rating_avg = float(rating_avg_elem.text)

        enrollment_elem = single_result.find('span', class_='enrollment-number')
        enrolment_number = None

        if enrollment_elem:
            enr_cl_txt = enrollment_elem.text.lower().replace(',', '').replace('.', '').replace('m', '0' * 6).replace('k', '0' * 3)
            if enr_cl_txt.isdigit():
                enrolment_number = int(enr_cl_txt)

        difficulty_elem = single_result.find('span', class_='difficulty')
        difficulty = ''
        if difficulty_elem:
            difficulty = difficulty_elem.text

        rating_count_elem = single_result.find('span', class_='ratings-count').find('span')
        rating_count = None
        if rating_count_elem:
            rating_count_cl = rating_count_elem.text.replace(',', '')
            if rating_count_cl.isdigit():
                rating_count = int(rating_count_cl)

        rdict = {
            "titles": title,
            "links": link,
            "partners": partner,
            "ratings_avg": rating_avg,
            "ratings_count": rating_count,
            "enrolments_numbers": enrolment_number,
            "difficulties": difficulty,
        }
        return rdict
